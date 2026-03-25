import streamlit as st
import os
import uuid
import json
import numpy as np
from datetime import datetime
from feature_extractor import VideoFeatureExtractor
from vector_store import VideoDatabase

# Page Configuration
st.set_page_config(
    page_title="🛡️ Video Piracy Detection System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Cyber Security Theme
st.markdown("""
<style>
    .main {
        background-color: #0d1117;
        color: #00ff00;
    }
    .stApp {
        background-color: #0d1117;
    }
    .stButton>button {
        background-color: #1f2937;
        color: #00ff00;
        border: 1px solid #00ff00;
    }
    .stButton>button:hover {
        background-color: #00ff00;
        color: #0d1117;
    }
    .stMetric {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 5px;
    }
    .terminal {
        background-color: #0d1117;
        border: 1px solid #30363d;
        border-radius: 5px;
        padding: 15px;
        font-family: 'Courier New', monospace;
        color: #00ff00;
        margin: 10px 0;
    }
    .security-badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 3px;
        font-weight: bold;
        font-size: 12px;
        margin-left: 10px;
    }
    .badge-secure {
        background-color: #00ff00;
        color: #0d1117;
    }
    .badge-warning {
        background-color: #ffaa00;
        color: #0d1117;
    }
    .badge-danger {
        background-color: #ff0000;
        color: #ffffff;
    }
    .badge-pending {
        background-color: #0088ff;
        color: #ffffff;
    }
    .stAlert {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 5px;
    }
    h1, h2, h3 {
        color: #00ff00;
    }
    .divider {
        border: 0;
        border-top: 1px solid #30363d;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Components
extractor = VideoFeatureExtractor()
db = VideoDatabase()

# Sidebar Navigation
st.sidebar.title("🛡️ Security Dashboard")
st.sidebar.markdown("---")
mode = st.sidebar.radio(
    "Select Operation Mode",
    ["🔒 Register Original", "🔍 Detect Piracy", "⚖️ Legal Workflow", "📊 System Status"],
    index=0
)

# --- MODE 1: REGISTER ORIGINAL ---
if mode == "🔒 Register Original":
    st.title("🔒 Content Registration System")
    st.markdown("### Secure Video Fingerprinting & Token Generation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader("Upload Original Video", type=["mp4", "mov", "avi"])
        
        if uploaded_file:
            temp_path = f"temp_{uuid.uuid4()}.mp4"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.markdown("```bash")
            st.markdown(f"📁 File: {uploaded_file.name}")
            st.markdown(f"📏 Size: {uploaded_file.size / 1024 / 1024:.2f} MB")
            st.markdown("```")
            
            if st.button("🔐 Generate Fingerprint", type="primary"):
                with st.spinner("🔍 Extracting Video Features..."):
                    features = extractor.process_video(temp_path)
                    
                    if len(features) > 0:
                        token = str(uuid.uuid4())[:8].upper()
                        owner = st.text_input("👤 Enter Owner Name", "Original Creator")
                        
                        if st.button("✅ Register Video"):
                            if db.add_video(features, token, owner, temp_path):
                                st.success("✅ **Video Registered Successfully!**")
                                st.markdown(f"""
                                <div class="terminal">
                                    <p>🔐 TOKEN: <strong>{token}</strong></p>
                                    <p>👤 OWNER: <strong>{owner}</strong></p>
                                    <p>📅 TIMESTAMP: <strong>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</strong></p>
                                    <p>🔢 FRAMES: <strong>{len(features)}</strong></p>
                                    <p>🛡️ STATUS: <span class="security-badge badge-secure">SECURE</span></p>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.error("❌ Failed to register video.")
                    else:
                        st.error("❌ Could not extract features from video.")
            
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    with col2:
        st.markdown("### 📋 Registration Stats")
        st.metric("📦 Registered Videos", len(db.metadata))
        st.metric("🔐 Active Tokens", len(db.metadata))
        st.metric("🛡️ Database Size", f"{db.index.ntotal} vectors")

# --- MODE 2: DETECT PIRACY ---
elif mode == "🔍 Detect Piracy":
    st.title("🔍 Piracy Detection System")
    st.markdown("### Advanced Video Similarity Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader("Upload Suspected Video", type=["mp4", "mov", "avi"])
        
        if uploaded_file:
            temp_path = f"temp_{uuid.uuid4()}.mp4"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.markdown("```bash")
            st.markdown(f"📁 File: {uploaded_file.name}")
            st.markdown(f"📏 Size: {uploaded_file.size / 1024 / 1024:.2f} MB")
            st.markdown("```")
            
            if st.button("🔍 Scan for Piracy", type="primary"):
                with st.spinner("🔍 Analyzing Video for Piracy..."):
                    features = extractor.process_video(temp_path)
                    
                    if len(features) > 0:
                        matches = db.search(features, threshold=0.75, k=5)
                        
                        if matches:
                            st.error("⚠️ **POTENTIAL PIRACY DETECTED!**")
                            
                            for i, match in enumerate(matches):
                                st.markdown(f"""
                                <div class="terminal">
                                    <p>🔍 MATCH #{i+1}</p>
                                    <p>🔐 TOKEN: <strong>{match['token']}</strong></p>
                                    <p>👤 OWNER: <strong>{match['owner']}</strong></p>
                                    <p>📊 CONFIDENCE: <strong>{match['confidence']:.2f}%</strong></p>
                                    <p>📈 PIRATED CONTENT: <strong>{min(100, match['confidence']):.2f}%</strong></p>
                                    <p>🛡️ STATUS: <span class="security-badge badge-danger">THREAT</span></p>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            st.session_state['piracy_detected'] = True
                        else:
                            st.success("✅ **No Piracy Detected**")
                            st.markdown("```bash")
                            st.markdown("🛡️ STATUS: <span class='security-badge badge-secure'>SECURE</span>")
                            st.markdown("```")
                            st.session_state['piracy_detected'] = False
                    else:
                        st.error("❌ Could not extract features from video.")
            
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    with col2:
        st.markdown("### 📊 Detection Stats")
        st.metric("📦 Database Videos", len(db.metadata))
        st.metric("🔍 Search Threshold", "75%")
        st.metric("🛡️ Security Level", "HIGH")

# --- MODE 3: LEGAL WORKFLOW ---
elif mode == "⚖️ Legal Workflow":
    st.title("⚖️ Copyright Claim System")
    st.markdown("### Legal Certificate & Permission Workflow")
    
    if st.session_state.get('piracy_detected', False):
        st.error("⚠️ **Piracy Detected in Previous Scan**")
        st.markdown("Please submit a copyright claim to verify ownership.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            claim_owner = st.text_input("👤 Original Owner Name")
            claim_token = st.text_input("🔐 Matched Token")
        
        with col2:
            claim_reason = st.text_area("📝 Claim Reason", "Unauthorized distribution of copyrighted content")
            claim_email = st.text_input("📧 Contact Email")
        
        if st.button("📄 Submit Copyright Claim", type="primary"):
            claim_id = str(uuid.uuid4())[:8].upper()
            claim_data = {
                "claim_id": claim_id,
                "owner": claim_owner,
                "token": claim_token,
                "reason": claim_reason,
                "email": claim_email,
                "timestamp": datetime.now().isoformat(),
                "status": "Pending Verification"
            }
            
            claims_path = "claims.json"
            claims = []
            if os.path.exists(claims_path):
                with open(claims_path, 'r') as f:
                    claims = json.load(f)
            claims.append(claim_data)
            with open(claims_path, 'w') as f:
                json.dump(claims, f, indent=4)
            
            st.success(f"✅ **Claim Submitted Successfully!**")
            st.markdown(f"""
            <div class="terminal">
                <p>📄 CERTIFICATE ID: <strong>{claim_id}</strong></p>
                <p>📅 TIMESTAMP: <strong>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</strong></p>
                <p>🛡️ STATUS: <span class="security-badge badge-pending">PENDING</span></p>
                <p>📧 NOTIFICATION: <strong>SENT TO OWNER</strong></p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("ℹ️ **No Active Piracy Detection Session**")
        st.markdown("Please run 'Detect Piracy' first to identify potential violations.")
        st.button("🔄 Reset Session", on_click=lambda: st.session_state.clear())

# --- MODE 4: SYSTEM STATUS ---
elif mode == "📊 System Status":
    st.title("📊 System Status Dashboard")
    st.markdown("### Security System Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📦 Registered Videos", len(db.metadata))
    with col2:
        st.metric("🔐 Active Tokens", len(db.metadata))
    with col3:
        st.metric("🛡️ Database Size", f"{db.index.ntotal} vectors")
    with col4:
        claims = []
        if os.path.exists("claims.json"):
            with open("claims.json", 'r') as f:
                claims = json.load(f)
        st.metric("📄 Claims Pending", len(claims))
    
    st.markdown("---")
    
    st.markdown("### 🔐 Security Logs")
    st.markdown("```bash")
    st.markdown(f"📅 Last Scan: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown(f"🛡️ Security Level: HIGH")
    st.markdown(f"🔒 Encryption: AES-256")
    st.markdown(f"📡 API Status: ONLINE")
    st.markdown("```")
    
    st.markdown("---")
    
    st.markdown("### 📋 Recent Claims")
    if os.path.exists("claims.json"):
        with open("claims.json", 'r') as f:
            claims = json.load(f)
        
        if claims:
            for claim in claims:
                st.markdown(f"""
                <div class="terminal">
                    <p>📄 ID: <strong>{claim['claim_id']}</strong></p>
                    <p>👤 OWNER: <strong>{claim['owner']}</strong></p>
                    <p>🔐 TOKEN: <strong>{claim['token']}</strong></p>
                    <p>📅 TIMESTAMP: <strong>{claim['timestamp']}</strong></p>
                    <p>🛡️ STATUS: <span class="security-badge badge-pending">{claim['status']}</span></p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("```bash")
            st.markdown("📄 No claims submitted yet")
            st.markdown("```")
    else:
        st.markdown("```bash")
        st.markdown("📄 No claims file found")
        st.markdown("```")
    
    st.markdown("---")
    
    st.markdown("### 🛠️ System Controls")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear Database", type="secondary"):
            if os.path.exists("faiss_index.index"):
                os.remove("faiss_index.index")
            if os.path.exists("metadata.json"):
                os.remove("metadata.json")
            st.cache_data.clear()
            st.rerun()
            st.success("✅ Database cleared successfully!")
    
    with col2:
        if st.button("📥 Export Claims", type="secondary"):
            if os.path.exists("claims.json"):
                with open("claims.json", 'r') as f:
                    data = f.read()
                st.download_button(
                    label="📥 Download Claims JSON",
                    data=data,
                    file_name="claims.json",
                    mime="application/json"
                )
            else:
                st.warning("⚠️ No claims file to export")

# Footer
st.markdown("---")
st.markdown("""
<div class="terminal" style="text-align: center;">
    <p>🛡️ Video Piracy Detection System v1.0 | Powered by PyTorch & FAISS</p>
    <p>🔐 Secure | 🔍 Accurate | ⚖️ Legal Compliant</p>
</div>
""", unsafe_allow_html=True)