//! ═══════════════════════════════════════════════════════════════════════════════
//! NEXUS PRIME Neural Spine Server
//! ═══════════════════════════════════════════════════════════════════════════════
//!
//! The central cognitive coordinator:
//! - Initializes shared memory (agent buffers + ring buffer)
//! - Runs GWT broadcast loop on dedicated thread
//! - Runs consolidation engine every 100 cycles
//! - Dispatches interrupts from ring buffer
//! - Bridges events to/from Redis (nexus:spine:*)
//! - Exposes HTTP health + metrics endpoints (port 8300)
//!
//! Adapted for 12-core single-NUMA AMD EPYC VM (Fix #1 cpuset: 0-2)
//! ═══════════════════════════════════════════════════════════════════════════════

use spine_core::agent_buffer::AgentMemoryRegion;
use spine_core::ring_buffer::InterruptRingBuffer;
use spine_core::gwt::GwtEngine;
use spine_core::consolidation::ConsolidationEngine;
use spine_core::shm::SharedMemoryRegion;
use spine_core::{NUM_AGENTS, BUF_PERCEPT};
use hyper::Response;
use http_body_util::Full;
use hyper::body::Bytes;

use tokio::sync::RwLock;
use std::sync::Arc;
use std::time::{Duration, Instant};
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};

/// Shared state accessible from all tasks
struct SpineState {
    /// Shared memory region handle (prevents drop/unmap)
    _shm: SharedMemoryRegion,
    /// Pointer to agent memory region in shared memory
    agent_region: *mut AgentMemoryRegion,
    /// Pointer to ring buffer in shared memory
    ring_buffer: *mut InterruptRingBuffer,
    /// GWT engine (behind lock for stats access from HTTP)
    gwt: RwLock<GwtEngine>,
    /// Consolidation engine
    consolidation: RwLock<ConsolidationEngine>,
    /// Total cognitive cycles
    cycle_count: AtomicU64,
    /// Average cycle time in nanoseconds
    avg_cycle_ns: AtomicU64,
    /// Running flag
    running: AtomicBool,
}

// Safety: the raw pointers point to mmap'd shared memory that lives
// as long as _shm. We ensure single-writer semantics via the GWT/consolidation locks.
unsafe impl Send for SpineState {}
unsafe impl Sync for SpineState {}

#[tokio::main]
async fn main() {
    eprintln!("═══════════════════════════════════════════════════════════════");
    eprintln!("     🧠 NEXUS PRIME Neural Spine — Starting...");
    eprintln!("═══════════════════════════════════════════════════════════════");

    // Configuration from environment
    let shm_name = std::env::var("SPINE_SHM_NAME").unwrap_or_else(|_| "/nexus_spine".to_string());
    let http_port: u16 = std::env::var("SPINE_HTTP_PORT")
        .unwrap_or_else(|_| "8300".to_string())
        .parse().unwrap_or(8300);
    let gwt_top_k: usize = std::env::var("SPINE_GWT_TOP_K")
        .unwrap_or_else(|_| "3".to_string())
        .parse().unwrap_or(3);
    let cycle_interval_us: u64 = std::env::var("SPINE_CYCLE_US")
        .unwrap_or_else(|_| "500".to_string())
        .parse().unwrap_or(500);
    let redis_url = std::env::var("REDIS_URL")
        .unwrap_or_else(|_| "redis://127.0.0.1:6379".to_string());

    // Calculate shared memory size
    let total_size = spine_core::shm::required_shm_size();
    eprintln!("[SPINE] Shared memory size: {} bytes ({:.2} MB)", total_size, total_size as f64 / 1048576.0);
    eprintln!("[SPINE] SHM name: {}", shm_name);
    eprintln!("[SPINE] GWT top-K: {}", gwt_top_k);
    eprintln!("[SPINE] Cycle interval: {}μs", cycle_interval_us);

    // Allocate shared memory
    let shm = SharedMemoryRegion::allocate(total_size, Some(&shm_name))
        .expect("Failed to allocate shared memory");

    let ptr = shm.ptr;

    // Initialize structures in shared memory
    let agent_region = ptr as *mut AgentMemoryRegion;
    unsafe { AgentMemoryRegion::init_at(agent_region); }

    let agent_size = std::mem::size_of::<AgentMemoryRegion>();
    let ring_buffer = unsafe { ptr.add(agent_size) } as *mut InterruptRingBuffer;
    unsafe { InterruptRingBuffer::init_at(ring_buffer); }

    eprintln!("[SPINE] Agent region at offset 0 ({} bytes)", agent_size);
    eprintln!("[SPINE] Ring buffer at offset {} ({} bytes)", agent_size, std::mem::size_of::<InterruptRingBuffer>());

    // Activate all 32 agents
    let region_ref = unsafe { &*agent_region };
    for i in 0..NUM_AGENTS {
        region_ref.activate_agent(i);
    }
    eprintln!("[SPINE] Activated {} agents", region_ref.active_count());

    let state = Arc::new(SpineState {
        _shm: shm,
        agent_region,
        ring_buffer,
        gwt: RwLock::new(GwtEngine::new(gwt_top_k)),
        consolidation: RwLock::new(ConsolidationEngine::new()),
        cycle_count: AtomicU64::new(0),
        avg_cycle_ns: AtomicU64::new(0),
        running: AtomicBool::new(true),
    });

    // Spawn the cognitive loop on a dedicated OS thread
    let state_cognitive = state.clone();
    let cognitive_handle = std::thread::Builder::new()
        .name("gwt-broadcast".to_string())
        .spawn(move || {
            cognitive_loop(state_cognitive, cycle_interval_us);
        })
        .expect("Failed to spawn cognitive thread");

    // Spawn Redis bridge task
    let state_redis = state.clone();
    let redis_handle = tokio::spawn(async move {
        redis_bridge(state_redis, &redis_url).await;
    });

    // Spawn HTTP server
    let state_http = state.clone();
    eprintln!("[SPINE] HTTP server starting on port {}", http_port);
    let http_handle = tokio::spawn(async move {
        http_server(state_http, http_port).await;
    });

    eprintln!("═══════════════════════════════════════════════════════════════");
    eprintln!("     🧠 NEXUS Neural Spine — ONLINE");
    eprintln!("═══════════════════════════════════════════════════════════════");

    // Wait for shutdown signal
    tokio::signal::ctrl_c().await.ok();
    eprintln!("[SPINE] Shutdown signal received");
    state.running.store(false, Ordering::Release);

    // Clean up
    redis_handle.abort();
    http_handle.abort();
    cognitive_handle.join().ok();

    eprintln!("[SPINE] Shutdown complete");
}

/// Main cognitive loop — runs on a dedicated OS thread
///
/// Cycle: GWT broadcast → interrupt dispatch → consolidation (every 100 cycles)
fn cognitive_loop(state: Arc<SpineState>, interval_us: u64) {
    let interval = Duration::from_micros(interval_us);
    let mut total_ns: u64 = 0;
    let mut count: u64 = 0;

    eprintln!("[GWT] Cognitive loop started (interval: {}μs)", interval_us);

    while state.running.load(Ordering::Acquire) {
        let cycle_start = Instant::now();

        // ═══ PHASE 1: GWT Broadcast ══════════════════════════════════════
        {
            let region = unsafe { &*state.agent_region };
            let mut gwt = state.gwt.blocking_write();
            gwt.broadcast_cycle(region);
        }

        // ═══ PHASE 2: Interrupt Dispatch ═════════════════════════════════
        {
            let ring = unsafe { &*state.ring_buffer };
            let region = unsafe { &*state.agent_region };

            // Process up to 64 interrupts per cycle
            for _ in 0..64 {
                match ring.pop() {
                    Some(entry) => {
                        // Write interrupt to target agent's PERCEPT buffer
                        if entry.target_agent == 0xFFFF {
                            // Broadcast interrupt: write to ALL agents
                            for i in 0..NUM_AGENTS {
                                region.agents[i].write_buffer(BUF_PERCEPT, &entry.payload);
                            }
                        } else if (entry.target_agent as usize) < NUM_AGENTS {
                            region.agents[entry.target_agent as usize]
                                .write_buffer(BUF_PERCEPT, &entry.payload);
                        }
                    }
                    None => break,
                }
            }
        }

        // ═══ PHASE 3: Consolidation (every 100 cycles) ══════════════════
        count += 1;
        if count % 100 == 0 {
            let region = unsafe { &*state.agent_region };
            let mut consolidation = state.consolidation.blocking_write();
            consolidation.consolidate(region);
        }

        // ═══ Timing ══════════════════════════════════════════════════════
        let elapsed = cycle_start.elapsed();
        total_ns += elapsed.as_nanos() as u64;
        state.cycle_count.store(count, Ordering::Relaxed);
        state.avg_cycle_ns.store(total_ns / count, Ordering::Relaxed);

        // Sleep for remaining interval
        if elapsed < interval {
            std::thread::sleep(interval - elapsed);
        }
    }

    eprintln!("[GWT] Cognitive loop stopped after {} cycles (avg: {:.1}μs)",
             count, (total_ns as f64) / (count.max(1) as f64) / 1000.0);
}

/// Redis event bridge — publishes spine events, subscribes to nexus commands
async fn redis_bridge(state: Arc<SpineState>, redis_url: &str) {
    eprintln!("[REDIS] Connecting to {}", redis_url);

    // Retry loop for Redis connection
    loop {
        match redis::Client::open(redis_url) {
            Ok(client) => {
                match client.get_multiplexed_async_connection().await {
                    Ok(mut conn) => {
                        eprintln!("[REDIS] Connected successfully");

                        // Publish spine status every 5 seconds
                        let mut interval = tokio::time::interval(Duration::from_secs(5));
                        loop {
                            interval.tick().await;

                            if !state.running.load(Ordering::Relaxed) {
                                break;
                            }

                            let cycle = state.cycle_count.load(Ordering::Relaxed);
                            let avg_us = state.avg_cycle_ns.load(Ordering::Relaxed) as f64 / 1000.0;

                            let gwt_stats = {
                                let gwt = state.gwt.read().await;
                                gwt.stats()
                            };
                            let consol_stats = {
                                let c = state.consolidation.read().await;
                                c.stats()
                            };

                            let ring = unsafe { &*state.ring_buffer };
                            let ring_stats = ring.stats();

                            let status = serde_json::json!({
                                "type": "spine_status",
                                "cycle": cycle,
                                "avg_cycle_us": avg_us,
                                "gwt": {
                                    "broadcast_count": gwt_stats.broadcast_count,
                                    "avg_broadcast_us": gwt_stats.avg_broadcast_us,
                                    "winners": gwt_stats.last_winners.len(),
                                },
                                "consolidation": {
                                    "active_agents": consol_stats.active_agents,
                                    "avg_staleness": consol_stats.avg_staleness,
                                    "prunable": consol_stats.prunable_count,
                                },
                                "ring_buffer": ring_stats,
                            });

                            let _: Result<(), _> = redis::cmd("PUBLISH")
                                .arg("nexus:spine:status")
                                .arg(status.to_string())
                                .query_async(&mut conn)
                                .await;
                        }
                    }
                    Err(e) => {
                        eprintln!("[REDIS] Connection failed: {}. Retrying in 5s...", e);
                    }
                }
            }
            Err(e) => {
                eprintln!("[REDIS] Client creation failed: {}. Retrying in 5s...", e);
            }
        }

        if !state.running.load(Ordering::Relaxed) {
            break;
        }
        tokio::time::sleep(Duration::from_secs(5)).await;
    }
}

/// HTTP health + metrics server
async fn http_server(state: Arc<SpineState>, port: u16) {
    use hyper::server::conn::http1;
    use hyper::service::service_fn;
    use hyper::Request;
    use hyper_util::rt::TokioIo;

    let addr = std::net::SocketAddr::from(([0, 0, 0, 0], port));
    let listener = tokio::net::TcpListener::bind(addr).await
        .expect(&format!("Failed to bind HTTP on port {}", port));

    eprintln!("[HTTP] Listening on port {}", port);

    loop {
        let (stream, _) = match listener.accept().await {
            Ok(conn) => conn,
            Err(e) => {
                eprintln!("[HTTP] Accept error: {}", e);
                continue;
            }
        };

        let state = state.clone();
        let io = TokioIo::new(stream);

        tokio::spawn(async move {
            let service = service_fn(move |req: Request<hyper::body::Incoming>| {
                let state = state.clone();
                async move {
                    let path = req.uri().path().to_string();
                    handle_request(&state, &path).await
                }
            });

            if let Err(e) = http1::Builder::new().serve_connection(io, service).await {
                // Connection errors are normal (client disconnect)
                let _ = e;
            }
        });
    }
}

async fn handle_request(
    state: &SpineState,
    path: &str,
) -> Result<Response<Full<Bytes>>, std::convert::Infallible> {

    let (status, body) = match path {
        "/health" => {
            let json = serde_json::json!({
                "status": "healthy",
                "service": "neural_spine",
                "version": "1.0.0",
                "cycles": state.cycle_count.load(Ordering::Relaxed),
            });
            (200, json.to_string())
        }

        "/status" => {
            let cycle = state.cycle_count.load(Ordering::Relaxed);
            let avg_us = state.avg_cycle_ns.load(Ordering::Relaxed) as f64 / 1000.0;
            let region = unsafe { &*state.agent_region };
            let ring = unsafe { &*state.ring_buffer };

            let gwt_stats = {
                let gwt = state.gwt.read().await;
                gwt.stats()
            };
            let consol_stats = {
                let c = state.consolidation.read().await;
                c.stats()
            };

            let json = serde_json::json!({
                "system": "NEXUS Neural Spine",
                "version": "1.0.0",
                "cognitive_cycles": cycle,
                "avg_cycle_us": format!("{:.1}", avg_us),
                "target_cycle_us": 500,
                "headroom_pct": format!("{:.1}", (1.0 - avg_us / 500.0) * 100.0),
                "agents": {
                    "active": region.active_count(),
                    "total": NUM_AGENTS,
                },
                "gwt": gwt_stats,
                "consolidation": consol_stats,
                "ring_buffer": ring.stats(),
            });
            (200, json.to_string())
        }

        "/metrics" => {
            let cycle = state.cycle_count.load(Ordering::Relaxed);
            let avg_us = state.avg_cycle_ns.load(Ordering::Relaxed) as f64 / 1000.0;
            let region = unsafe { &*state.agent_region };
            let ring = unsafe { &*state.ring_buffer };
            let ring_stats = ring.stats();

            let gwt_stats = {
                let gwt = state.gwt.read().await;
                gwt.stats()
            };

            // Prometheus format
            let metrics = format!(
                "# HELP spine_cycles_total Total cognitive cycles\n\
                 # TYPE spine_cycles_total counter\n\
                 spine_cycles_total {}\n\
                 # HELP spine_cycle_avg_us Average cycle time in microseconds\n\
                 # TYPE spine_cycle_avg_us gauge\n\
                 spine_cycle_avg_us {:.1}\n\
                 # HELP spine_agents_active Number of active agents\n\
                 # TYPE spine_agents_active gauge\n\
                 spine_agents_active {}\n\
                 # HELP spine_gwt_broadcasts_total Total GWT broadcast cycles\n\
                 # TYPE spine_gwt_broadcasts_total counter\n\
                 spine_gwt_broadcasts_total {}\n\
                 # HELP spine_gwt_avg_broadcast_us Average GWT broadcast time\n\
                 # TYPE spine_gwt_avg_broadcast_us gauge\n\
                 spine_gwt_avg_broadcast_us {:.1}\n\
                 # HELP spine_ring_buffer_len Current ring buffer entries\n\
                 # TYPE spine_ring_buffer_len gauge\n\
                 spine_ring_buffer_len {}\n\
                 # HELP spine_ring_buffer_pushed_total Total interrupts pushed\n\
                 # TYPE spine_ring_buffer_pushed_total counter\n\
                 spine_ring_buffer_pushed_total {}\n\
                 # HELP spine_ring_buffer_dropped_total Total interrupts dropped\n\
                 # TYPE spine_ring_buffer_dropped_total counter\n\
                 spine_ring_buffer_dropped_total {}\n",
                cycle,
                avg_us,
                region.active_count(),
                gwt_stats.broadcast_count,
                gwt_stats.avg_broadcast_us,
                ring_stats.current_len,
                ring_stats.total_pushed,
                ring_stats.total_dropped,
            );
            (200, metrics)
        }

        _ => {
            let json = serde_json::json!({"error": "not found"});
            (404, json.to_string())
        }
    };

    let response = Response::builder()
        .status(status)
        .header("Content-Type", if path == "/metrics" { "text/plain" } else { "application/json" })
        .header("Access-Control-Allow-Origin", "*")
        .body(Full::new(Bytes::from(body)))
        .unwrap();

    Ok(response)
}
