"""
🌐 NEXUS Memory Keeper - Web UI
═══════════════════════════════════════

واجهة ويب للتفاعل مع حارس الذاكرة المركزية

الصفحات:
• 🏠 Dashboard - نظرة عامة
• 💬 Chat - محادثة مباشرة
• 📊 Reports - تقارير شاملة
• 🤖 Agents - خريطة الوكلاء
• 📝 Timeline - سجل الأحداث
• 🚨 Incidents - الحوادث
• 🧠 Self-Awareness - الوعي الذاتي

المؤلف: MrF
"""

import streamlit as st
import httpx
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ═══════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════

st.set_page_config(
    page_title="NEXUS Memory Keeper",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://localhost:9000"

# CSS مخصص
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# Sidebar
# ═══════════════════════════════════════════════════════════

st.sidebar.markdown("# 🧠 NEXUS Memory Keeper")
st.sidebar.markdown("**حارس الذاكرة المركزية**")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "اختر الصفحة",
    [
        "🏠 Dashboard",
        "💬 Chat",
        "📊 Reports",
        "🤖 Agents",
        "📝 Timeline",
        "🚨 Incidents",
        "🧠 Self-Awareness"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔗 روابط سريعة")
st.sidebar.markdown("[📖 API Docs](http://localhost:9000/docs)")
st.sidebar.markdown("[🏥 Health Check](http://localhost:9000/health)")
st.sidebar.markdown("[📋 System Report](http://localhost:9000/reports/system)")

# ═══════════════════════════════════════════════════════════
# Helper Functions
# ═══════════════════════════════════════════════════════════

@st.cache_data(ttl=30)
def fetch_api(endpoint: str):
    """جلب البيانات من API مع caching"""
    try:
        response = httpx.get(f"{API_URL}{endpoint}", timeout=10.0)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"خطأ في الاتصال: {e}")
        return None

def post_api(endpoint: str, data: dict):
    """إرسال بيانات لـ API"""
    try:
        response = httpx.post(f"{API_URL}{endpoint}", json=data, timeout=30.0)
        if response.status_code == 200:
            return response.json()
        return {"error": response.text}
    except Exception as e:
        return {"error": str(e)}

# ═══════════════════════════════════════════════════════════
# 🏠 Dashboard Page
# ═══════════════════════════════════════════════════════════

if page == "🏠 Dashboard":
    st.markdown('<div class="main-header">🏠 System Overview</div>', unsafe_allow_html=True)
    
    # جلب البيانات
    root_data = fetch_api("/")
    health_data = fetch_api("/health")
    
    if root_data and health_data:
        # Metrics في صف واحد
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Status", health_data.get('status', 'N/A').upper())
        with col2:
            st.metric("🤖 Agents Tracked", health_data.get('agents_tracked', 0))
        with col3:
            st.metric("📝 Events Recorded", health_data.get('events_recorded', 0))
        with col4:
            health_score = root_data.get('system_health', {}).get('health_score', 0) if root_data.get('system_health') else 0
            st.metric("🏥 Health Score", f"{health_score}%")
        
        st.markdown("---")
        
        # Identity & Health
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🆔 System Identity")
            if root_data.get('identity'):
                identity = root_data['identity']
                st.write(f"**Name:** {identity.get('name', 'N/A')}")
                st.write(f"**Version:** {identity.get('version', 'N/A')}")
                st.write(f"**Role:** {identity.get('role', 'N/A')}")
                st.write(f"**Mission:** {identity.get('mission', 'N/A')}")
                st.write(f"**Consciousness Level:** {identity.get('consciousness_level', 0)}%")
        
        with col2:
            st.subheader("🏥 System Health")
            if root_data.get('system_health'):
                health = root_data['system_health']
                st.write(f"**Total Agents:** {health.get('total_agents', 0)}")
                st.write(f"**Agents Online:** {health.get('agents_online', 0)}")
                st.write(f"**Agents Offline:** {health.get('total_agents', 0) - health.get('agents_online', 0)}")
                st.write(f"**Unresolved Incidents:** {health.get('unresolved_incidents', 0)}")
                st.write(f"**Changes (24h):** {health.get('changes_last_24h', 0)}")
        
        # Capabilities
        st.markdown("---")
        st.subheader("🎯 Capabilities")
        if root_data.get('capabilities'):
            cols = st.columns(3)
            for idx, cap in enumerate(root_data['capabilities']):
                with cols[idx % 3]:
                    st.info(cap)
    
    else:
        st.error("❌ لا يمكن الاتصال بـ Memory Keeper API")

# ═══════════════════════════════════════════════════════════
# 💬 Chat Page
# ═══════════════════════════════════════════════════════════

elif page == "💬 Chat":
    st.markdown('<div class="main-header">💬 Chat with Memory Keeper</div>', unsafe_allow_html=True)
    
    st.markdown("تحدث مباشرة مع حارس الذاكرة واسأله عن النظام والوكلاء والأحداث")
    
    # Chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])
    
    # User input
    user_message = st.chat_input("اكتب رسالتك هنا...")
    
    if user_message:
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_message
        })
        
        with st.chat_message("user"):
            st.markdown(user_message)
        
        # Get response from API
        with st.spinner("جاري التفكير..."):
            response = post_api("/conversation", {
                "user_name": "MrF",
                "message": user_message,
                "context": {}
            })
            
            if response and 'response' in response:
                bot_message = response['response']
                response_time = response.get('response_time_ms', 0)
                
                # Add bot response to history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": bot_message
                })
                
                with st.chat_message("assistant"):
                    st.markdown(bot_message)
                    st.caption(f"⏱️ وقت الاستجابة: {response_time}ms")
            
            else:
                st.error("حدث خطأ في الاتصال")
    
    # Clear history button
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.chat_history = []
        st.rerun()

# ═══════════════════════════════════════════════════════════
# 📊 Reports Page
# ═══════════════════════════════════════════════════════════

elif page == "📊 Reports":
    st.markdown('<div class="main-header">📊 System Reports</div>', unsafe_allow_html=True)
    
    if st.button("🔄 Generate System Report"):
        with st.spinner("جاري إنشاء التقرير..."):
            report = fetch_api("/reports/system")
            
            if report:
                st.success("✅ تم إنشاء التقرير بنجاح")
                
                # Identity
                st.subheader("🆔 System Identity")
                if report.get('identity'):
                    st.json(report['identity'])
                
                # Health
                st.subheader("🏥 System Health")
                if report.get('health'):
                    health = report['health']
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Health Score", f"{health.get('health_score', 0)}%")
                    with col2:
                        st.metric("Total Agents", health.get('total_agents', 0))
                    with col3:
                        st.metric("Agents Online", health.get('agents_online', 0))
                
                # Active Agents
                st.subheader("🤖 Active Agents")
                if report.get('agents', {}).get('active'):
                    agents_df = pd.DataFrame(report['agents']['active'])
                    st.dataframe(agents_df, use_container_width=True)
                
                # Activity
                st.subheader("📈 Activity (Last 24h)")
                if report.get('activity'):
                    activity = report['activity']
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Changes", activity.get('changes_last_24h', 0))
                        st.metric("Conversations", activity.get('conversations_last_24h', 0))
                    with col2:
                        if activity.get('incidents_by_severity'):
                            st.write("**Incidents by Severity:**")
                            for severity, count in activity['incidents_by_severity'].items():
                                st.write(f"• {severity}: {count}")
                
                # Recent Deployments
                st.subheader("🚀 Recent Deployments")
                if report.get('recent_deployments'):
                    deployments_df = pd.DataFrame(report['recent_deployments'])
                    st.dataframe(deployments_df, use_container_width=True)
                
                # Download button
                st.download_button(
                    label="📥 Download Report (JSON)",
                    data=json.dumps(report, indent=2, ensure_ascii=False),
                    file_name=f"nexus_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
            else:
                st.error("❌ فشل إنشاء التقرير")

# ═══════════════════════════════════════════════════════════
# 🤖 Agents Page
# ═══════════════════════════════════════════════════════════

elif page == "🤖 Agents":
    st.markdown('<div class="main-header">🤖 Agents Map</div>', unsafe_allow_html=True)
    
    # Filter
    status_filter = st.selectbox("فلترة حسب الحالة", ["all", "online", "offline"])
    
    # Fetch agents
    if status_filter == "all":
        agents_data = fetch_api("/self/agents")
    else:
        agents_data = fetch_api(f"/self/agents?status={status_filter}")
    
    if agents_data:
        agents = agents_data.get('agents', [])
        stats = agents_data.get('stats', {})
        
        # Stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Agents", stats.get('total', 0))
        with col2:
            st.metric("Online", stats.get('online', 0), delta=f"+{stats.get('online', 0)}")
        with col3:
            st.metric("Offline", stats.get('offline', 0), delta=f"-{stats.get('offline', 0)}")
        
        st.markdown("---")
        
        # Agents table
        if agents:
            agents_df = pd.DataFrame(agents)
            
            # Add color based on status
            def status_color(status):
                if status == 'online':
                    return '🟢'
                return '🔴'
            
            agents_df['status_icon'] = agents_df['status'].apply(status_color)
            
            st.dataframe(
                agents_df[['status_icon', 'name', 'display_name', 'agent_type', 'status', 'endpoint']],
                use_container_width=True
            )
            
            # Pie chart: by type
            st.subheader("📊 Agents by Type")
            type_counts = agents_df['agent_type'].value_counts()
            fig = px.pie(
                values=type_counts.values,
                names=type_counts.index,
                title="نوع الوكلاء"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.info("لا توجد وكلاء متاحة")
        
        # Relationships graph
        st.markdown("---")
        st.subheader("🔗 Relationships Graph")
        graph_data = fetch_api("/relationships/graph")
        
        if graph_data and graph_data.get('edges'):
            st.write(f"**Nodes:** {graph_data['node_count']}")
            st.write(f"**Edges:** {graph_data['edge_count']}")
            
            # Create network diagram (simplified)
            edges_df = pd.DataFrame(graph_data['edges'])
            st.dataframe(edges_df, use_container_width=True)

# ═══════════════════════════════════════════════════════════
# 📝 Timeline Page
# ═══════════════════════════════════════════════════════════

elif page == "📝 Timeline":
    st.markdown('<div class="main-header">📝 Events Timeline</div>', unsafe_allow_html=True)
    
    # Time range selector
    hours = st.slider("عدد الساعات للخلف", min_value=1, max_value=168, value=24, step=1)
    
    if st.button("🔍 Load Timeline"):
        with st.spinner("جاري التحميل..."):
            timeline_data = fetch_api(f"/memory/timeline?hours={hours}")
            
            if timeline_data and timeline_data.get('timeline'):
                timeline = timeline_data['timeline']
                st.success(f"✅ تم تحميل {timeline_data['count']} حدث")
                
                # Timeline display
                for event in timeline:
                    source = event.get('source', 'unknown')
                    event_type = event.get('type', 'unknown')
                    component = event.get('component', 'N/A')
                    description = event.get('description', 'No description')
                    created_at = event.get('created_at', 'N/A')
                    
                    # Icon based on source
                    icon = {"change": "🔧", "event": "📢", "deployment": "🚀"}.get(source, "📌")
                    
                    with st.expander(f"{icon} [{event_type}] {component} — {created_at[:19]}"):
                        st.write(f"**Source:** {source}")
                        st.write(f"**Description:** {description}")
                        st.json(event)
            
            else:
                st.info("لا توجد أحداث في هذه الفترة")

# ═══════════════════════════════════════════════════════════
# 🚨 Incidents Page
# ═══════════════════════════════════════════════════════════

elif page == "🚨 Incidents":
    st.markdown('<div class="main-header">🚨 Incidents Tracking</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📋 View Incidents", "➕ Report Incident"])
    
    with tab1:
        severity_filter = st.selectbox("فلترة حسب الخطورة", ["", "info", "warning", "error", "critical", "fatal"])
        
        if severity_filter:
            incidents_data = fetch_api(f"/incidents/unresolved?severity={severity_filter}")
        else:
            incidents_data = fetch_api("/incidents/unresolved")
        
        if incidents_data and incidents_data.get('incidents'):
            incidents = incidents_data['incidents']
            st.write(f"**Total Unresolved:** {incidents_data['count']}")
            
            for incident in incidents:
                severity = incident.get('severity', 'info')
                # Color based on severity
                color = {
                    'info': '🔵',
                    'warning': '🟡',
                    'error': '🟠',
                    'critical': '🔴',
                    'fatal': '⚫'
                }.get(severity, '⚪')
                
                with st.expander(f"{color} [{severity.upper()}] {incident.get('incident_type', 'N/A')} — {incident.get('created_at', '')[:19]}"):
                    st.write(f"**Agent:** {incident.get('agent_name', 'N/A')}")
                    st.write(f"**Message:** {incident.get('message', 'N/A')}")
                    if incident.get('stack_trace'):
                        st.code(incident['stack_trace'], language='python')
                    st.json(incident)
        else:
            st.success("✅ لا توجد حوادث غير محلولة")
    
    with tab2:
        st.subheader("Report New Incident")
        
        with st.form("incident_form"):
            severity = st.selectbox("Severity", ["info", "warning", "error", "critical", "fatal"])
            agent_name = st.text_input("Agent Name (optional)")
            incident_type = st.selectbox("Incident Type", [
                "connection", "timeout", "crash", "security", "data", "performance"
            ])
            message = st.text_area("Message", placeholder="Describe the incident...")
            stack_trace = st.text_area("Stack Trace (optional)", placeholder="Paste stack trace if available...")
            
            submitted = st.form_submit_button("📤 Report Incident")
            
            if submitted and message:
                incident_data = {
                    "severity": severity,
                    "agent_name": agent_name if agent_name else None,
                    "incident_type": incident_type,
                    "message": message,
                    "stack_trace": stack_trace if stack_trace else None,
                    "context": {}
                }
                
                result = post_api("/incidents/report", incident_data)
                
                if result and result.get('reported'):
                    st.success(f"✅ Incident reported: {result.get('incident_id')}")
                else:
                    st.error("❌ Failed to report incident")

# ═══════════════════════════════════════════════════════════
# 🧠 Self-Awareness Page
# ═══════════════════════════════════════════════════════════

elif page == "🧠 Self-Awareness":
    st.markdown('<div class="main-header">🧠 Self-Awareness & Reflection</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🆔 Identity", "🎯 Capabilities", "🤔 Reflect"])
    
    with tab1:
        st.subheader("🆔 System Identity")
        identity_data = fetch_api("/self/identity")
        
        if identity_data and identity_data.get('identity'):
            identity = identity_data['identity']
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Name", identity.get('name', 'N/A'))
                st.metric("Version", identity.get('version', 'N/A'))
                st.metric("Consciousness Level", f"{identity.get('consciousness_level', 0)}%")
            with col2:
                st.metric("Health Score", f"{identity.get('health_score', 0)}%")
                st.metric("Total Agents", identity.get('total_agents', 0))
                st.metric("Total Events", identity.get('total_events', 0))
            
            st.write(f"**Role:** {identity.get('role', 'N/A')}")
            st.write(f"**Mission:** {identity.get('mission', 'N/A')}")
            st.write(f"**Environment:** {identity.get('deployment_environment', 'N/A')}")
    
    with tab2:
        st.subheader("🎯 System Capabilities")
        caps_data = fetch_api("/self/capabilities")
        
        if caps_data:
            st.write(f"**Total Capabilities:** {caps_data.get('total_capabilities', 0)}")
            st.write(f"**Active Agents:** {caps_data.get('active_agents', 0)}")
            
            all_caps = caps_data.get('all_capabilities', [])
            if all_caps:
                # Display as chips
                caps_html = " ".join([f'<span style="background-color:#e3f2fd;padding:5px 10px;border-radius:15px;margin:5px;display:inline-block;">{cap}</span>' for cap in all_caps])
                st.markdown(caps_html, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("🤔 Ask Me Anything")
        st.write("اسأل النظام عن نفسه - سيفكر ويرد بناءً على معرفته الذاتية")
        
        with st.form("reflection_form"):
            question = st.text_area("Your Question", placeholder="مثال: ما هي صحتك الحالية؟ ما هي نقاط قوتك؟")
            reflection_type = st.selectbox("Reflection Type", [
                "health", "performance", "purpose", "capability", "relationship", "forecast"
            ])
            
            submitted = st.form_submit_button("🧠 Reflect")
            
            if submitted and question:
                with st.spinner("جاري التfكير..."):
                    reflection_data = post_api("/self/reflect", {
                        "question": question,
                        "reflection_type": reflection_type
                    })
                    
                    if reflection_data and reflection_data.get('answer'):
                        st.success("✅ انتهى التأمل")
                        
                        st.write(f"**Question:** {reflection_data['question']}")
                        st.write(f"**Answer:**")
                        st.info(reflection_data['answer'])
                        
                        st.write(f"**Confidence:** {reflection_data.get('confidence', 0)}%")
                        st.write(f"**Type:** {reflection_data['reflection_type']}")
                        st.caption(f"Reflection ID: {reflection_data.get('reflection_id', 'N/A')}")
                    
                    else:
                        st.error("❌ فشل التأمل")

# ═══════════════════════════════════════════════════════════
# Footer
# ═══════════════════════════════════════════════════════════

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ معلومات")
st.sidebar.info("""
**NEXUS Memory Keeper**  
Version: 1.0.0  
حارس الذاكرة والأرشيف المركزي

المؤلف: MrF  
التاريخ: 20 فبراير 2026
""")
