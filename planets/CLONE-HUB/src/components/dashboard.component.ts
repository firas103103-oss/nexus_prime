
import { Component, inject, ElementRef, ViewChild, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NexusEngineService } from '../services/nexus-engine.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="w-full flex flex-col gap-6 h-full justify-center animate-fade-in-up">
      
      <!-- Top Stats Row -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        <!-- Status Card -->
        <div class="bg-black/80 border border-white/10 rounded-sm p-6 relative overflow-hidden group shadow-[0_0_30px_rgba(0,0,0,0.5)]">
          <div class="absolute inset-0 bg-gradient-to-br from-fuchsia-900/20 to-cyan-900/20 opacity-0 group-hover:opacity-100 transition duration-700"></div>
          <div class="relative z-10">
            <div class="flex justify-between items-center mb-2">
                <div class="text-slate-500 text-[10px] tracking-[0.2em] uppercase font-bold">System Status</div>
                <div [class]="'w-2 h-2 rounded-full animate-pulse shadow-lg ' + getStatusColor(service.status().stage)"></div>
            </div>
            <div class="text-2xl font-bold text-slate-100 tracking-tight font-mono">
              {{ getStatusLabel(service.status().stage) }}
            </div>
          </div>
        </div>

        <!-- Word Count Card -->
        <div class="bg-black/80 border border-white/10 rounded-sm p-6 relative overflow-hidden group shadow-[0_0_30px_rgba(0,0,0,0.5)]">
          <div class="relative z-10">
            <div class="text-slate-500 text-[10px] tracking-[0.2em] uppercase mb-2 font-bold">Words Generated</div>
            <div class="font-mono text-4xl text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400 font-bold drop-shadow-sm">
              {{ service.generatedWordCount() | number }}
            </div>
          </div>
        </div>

        <!-- Engine Card -->
        <div class="bg-black/80 border border-white/10 rounded-sm p-6 relative overflow-hidden group shadow-[0_0_30px_rgba(0,0,0,0.5)]">
          <div class="relative z-10">
             <div class="text-slate-500 text-[10px] tracking-[0.2em] uppercase mb-2 font-bold">Active Neural Core</div>
             <div class="flex items-center gap-2">
               <span class="font-bold text-slate-200 text-sm font-mono tracking-wider">
                 {{ getEngineLabel(service.status().stage) }}
               </span>
             </div>
          </div>
        </div>
      </div>

      <!-- Main Progress & Message -->
      <div class="bg-[#0a0a0a] border border-white/10 rounded-sm p-8 shadow-[0_0_50px_rgba(192,38,211,0.05)] relative overflow-hidden">
        <!-- Grid Pattern -->
        <div class="absolute inset-0 opacity-[0.05]" style="background-image: linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px); background-size: 20px 20px;"></div>

        <div class="relative z-10">
          <div class="flex justify-between items-end mb-4">
             <h2 class="text-lg font-bold text-slate-300 tracking-widest uppercase">Protocol Execution</h2>
             <span class="font-mono text-5xl font-black text-white/90 drop-shadow-[0_0_10px_rgba(255,255,255,0.2)]">{{ service.status().progress }}<span class="text-lg align-top text-slate-600">%</span></span>
          </div>
          
          <!-- Progress Bar -->
          <div class="w-full bg-black rounded-full h-2 mb-8 overflow-hidden border border-white/5">
            <div class="h-full bg-gradient-to-r from-fuchsia-600 via-purple-600 to-cyan-500 transition-all duration-300 relative shadow-[0_0_20px_rgba(192,38,211,0.6)]" [style.width.%]="service.status().progress">
              <div class="absolute inset-0 bg-white/20 animate-[shimmer_2s_infinite]"></div>
            </div>
          </div>

          <div class="flex items-center gap-6">
             <div class="w-16 h-16 rounded-sm bg-black border border-white/5 flex items-center justify-center shrink-0 shadow-inner">
               <span class="text-3xl animate-pulse grayscale group-hover:grayscale-0 transition-all">
                 {{ getIconForStage(service.status().stage) }}
               </span>
             </div>
             <div class="flex-1">
                <div class="text-[10px] text-fuchsia-500 uppercase tracking-[0.25em] font-bold mb-1">
                   AGNT :: {{ service.status().agentName }}
                </div>
                <div class="text-slate-300 text-sm font-light leading-relaxed tracking-wide min-h-[3rem]">
                   {{ service.status().message }}
                </div>
             </div>
          </div>
        </div>
      </div>

      <!-- Console Log -->
      <div class="flex-1 min-h-[250px] max-h-[400px] bg-black border border-white/10 rounded-sm p-4 relative overflow-hidden flex flex-col shadow-inner">
        <div class="flex justify-between items-center mb-2 pb-2 border-b border-white/5">
           <span class="text-[9px] text-slate-600 uppercase tracking-[0.2em]">EVENT_LOG_STREAM</span>
           <div class="flex gap-1 opacity-30">
             <div class="w-1.5 h-1.5 rounded-full bg-red-500"></div>
             <div class="w-1.5 h-1.5 rounded-full bg-yellow-500"></div>
             <div class="w-1.5 h-1.5 rounded-full bg-green-500"></div>
           </div>
        </div>
        
        <div #logContainer class="flex-1 overflow-y-auto font-mono text-[11px] space-y-2 pr-2 scrollbar-thin scroll-smooth">
           @if (service.logs().length === 0) {
             <div class="text-slate-700 italic text-center mt-10">Waiting for stream...</div>
           }
           @for (log of service.logs(); track $index) {
             <div class="flex gap-3 text-slate-400 hover:text-white transition-colors pl-1 border-l-2 border-transparent hover:border-cyan-900/50">
               <span class="text-slate-600 shrink-0 select-none opacity-50">{{ log.timestamp | date:'HH:mm:ss' }}</span>
               <span [class]="getLogColor(log.type)">{{ log.message }}</span>
             </div>
           }
        </div>
      </div>

    </div>
  `,
  styles: [`
    .scrollbar-thin::-webkit-scrollbar { width: 4px; }
    .scrollbar-thin::-webkit-scrollbar-track { background: transparent; }
    .scrollbar-thin::-webkit-scrollbar-thumb { background: #222; border-radius: 2px; }
    .animate-fade-in-up { animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1); }
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes shimmer { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }
  `]
})
export class DashboardComponent {
  service = inject(NexusEngineService);
  @ViewChild('logContainer') private logContainer!: ElementRef;

  constructor() {
    effect(() => {
      const logs = this.service.logs();
      setTimeout(() => this.scrollToBottom(), 100);
    });
  }

  scrollToBottom() {
    if (this.logContainer) {
      this.logContainer.nativeElement.scrollTop = this.logContainer.nativeElement.scrollHeight;
    }
  }

  getStatusColor(stage: string) {
    if (stage === 'error') return 'bg-red-500';
    if (stage === 'complete') return 'bg-emerald-500';
    return 'bg-amber-400';
  }

  getStatusLabel(stage: string): string {
    const labels: Record<string, string> = {
      'idle': 'STANDBY',
      'analyzing_bg': 'SCANNING',
      'blueprint': 'ARCHITECTING',
      'expansion': 'GHOSTWRITING',
      'visuals': 'DESIGNING',
      'director': 'RENDERING',
      'analyst': 'ANALYZING',
      'finalizing': 'PACKAGING',
      'complete': 'COMPLETED',
      'error': 'SYSTEM ERROR'
    };
    return labels[stage] || stage.toUpperCase();
  }

  getEngineLabel(stage: string): string {
    if (['blueprint', 'analyst'].includes(stage)) return 'Gemini 2.5 Flash';
    if (['expansion'].includes(stage)) return 'Gemini 2.5 (Creative)';
    if (['visuals'].includes(stage)) return 'Imagen 4.0';
    if (['director'].includes(stage)) return 'Veo 2.0';
    return 'IDLE';
  }

  getLogColor(type: string): string {
    switch(type) {
      case 'success': return 'text-emerald-400 font-bold';
      case 'warn': return 'text-red-400 font-bold';
      case 'system': return 'text-amber-500 font-bold';
      default: return 'text-slate-300';
    }
  }

  getIconForStage(stage: string): string {
     switch(stage) {
       case 'expansion': return '✍️';
       case 'visuals': return '🎨';
       case 'director': return '🎬';
       case 'finalizing': return '📦';
       case 'complete': return '✅';
       case 'error': return '⚠️';
       default: return '⚙️';
     }
  }
}
