import streamlit as st
import json
import os
import difflib
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from dotenv import load_dotenv
from utils.file_utils import load_json, save_json, save_version, regenerate_content, summarize_changes, generate_module
from utils.database import (
    init_db, save_module_to_db, get_module_by_id, get_all_modules,
    update_section_content, approve_section, reject_section, publish_module,
    get_module_stats, export_module_to_json, get_section_versions
)

# Page config must be first
st.set_page_config(
    page_title="AI Copilot - Education Module Editor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Initialize database
init_db()

# Enhanced Custom CSS with modern design
dark_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1d35 100%);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #161b33 0%, #0d1117 100%);
        border-right: 1px solid rgba(88, 166, 255, 0.1);
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        padding-top: 2rem;
    }
    
    /* Main content area */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #E6EDF3;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    
    h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        font-size: 1.75rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        font-size: 1.25rem;
        color: #58A6FF;
    }
    
    /* Card-like containers */
    .stExpander {
        background: rgba(22, 27, 51, 0.6);
        border: 1px solid rgba(88, 166, 255, 0.15);
        border-radius: 12px;
        backdrop-filter: blur(10px);
        margin: 0.75rem 0;
        transition: all 0.3s ease;
    }
    
    .stExpander:hover {
        border-color: rgba(88, 166, 255, 0.3);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(88, 166, 255, 0.1);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #58A6FF 0%, #1F6FEB 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        letter-spacing: 0.02em;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(88, 166, 255, 0.2);
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(88, 166, 255, 0.35);
        background: linear-gradient(135deg, #6BB0FF 0%, #2F7FFC 100%);
    }
    
    .stButton>button:active {
        transform: translateY(-1px);
    }
    
    .stButton>button:disabled {
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        cursor: not-allowed;
        opacity: 0.5;
    }
    
    /* Text Areas */
    .stTextArea textarea {
        background: rgba(22, 27, 51, 0.8);
        color: #E6EDF3;
        border: 1px solid rgba(88, 166, 255, 0.2);
        border-radius: 10px;
        padding: 1rem;
        font-size: 0.95rem;
        line-height: 1.6;
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #58A6FF;
        box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.1);
        outline: none;
    }
    
    .stTextArea textarea:disabled {
        background: rgba(22, 27, 51, 0.4);
        opacity: 0.7;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background: rgba(22, 27, 51, 0.8);
        border: 1px solid rgba(88, 166, 255, 0.2);
        border-radius: 10px;
        color: #E6EDF3;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #58A6FF;
    }
    
    [data-testid="stMetricLabel"] {
        color: #8B949E;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Bloom Level Badges */
    .bloom-badge {
        display: inline-block;
        padding: 0.35rem 0.85rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    .bloom-apply {
        background: linear-gradient(135deg, #238636, #2ea043);
        color: white;
    }
    
    .bloom-understand {
        background: linear-gradient(135deg, #1F6FEB, #388bfd);
        color: white;
    }
    
    .bloom-evaluate {
        background: linear-gradient(135deg, #D29922, #e0a526);
        color: white;
    }
    
    /* Progress Section */
    .progress-container {
        background: linear-gradient(135deg, rgba(22, 27, 51, 0.8), rgba(13, 17, 35, 0.8));
        border: 1px solid rgba(88, 166, 255, 0.2);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .stProgress > div > div {
        background: linear-gradient(90deg, #58A6FF, #1F6FEB);
        border-radius: 10px;
        height: 12px;
    }
    
    /* Animated Header */
    .hero-header {
        background: linear-gradient(135deg, #58A6FF, #1F6FEB, #238636, #D29922);
        background-size: 300% 300%;
        animation: gradientShift 8s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin: 1rem 0 2rem 0;
        letter-spacing: -0.03em;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Info/Warning/Success boxes */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid;
        backdrop-filter: blur(10px);
    }
    
    /* Tables */
    .stDataFrame {
        background: rgba(22, 27, 51, 0.6);
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(88, 166, 255, 0.3), transparent);
        margin: 2rem 0;
    }
    
    /* Code blocks */
    .stCode {
        background: rgba(13, 17, 35, 0.8);
        border: 1px solid rgba(88, 166, 255, 0.2);
        border-radius: 10px;
    }
    
    /* Footer */
    .custom-footer {
        text-align: center;
        margin-top: 4rem;
        padding: 2rem 0;
        color: #6E7681;
        font-size: 0.9rem;
        border-top: 1px solid rgba(88, 166, 255, 0.1);
    }
    
    /* Sidebar Navigation */
    .css-1d391kg {
        background-color: transparent;
    }
    
    /* Tab styling for better separation */
    .section-card {
        background: rgba(22, 27, 51, 0.6);
        border: 1px solid rgba(88, 166, 255, 0.15);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .section-card:hover {
        border-color: rgba(88, 166, 255, 0.3);
        box-shadow: 0 8px 24px rgba(88, 166, 255, 0.15);
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .status-approved {
        background: rgba(35, 134, 54, 0.2);
        color: #3fb950;
        border: 1px solid rgba(35, 134, 54, 0.4);
    }
    
    .status-rejected {
        background: rgba(248, 81, 73, 0.2);
        color: #f85149;
        border: 1px solid rgba(248, 81, 73, 0.4);
    }
    
    .status-pending {
        background: rgba(210, 153, 34, 0.2);
        color: #d29922;
        border: 1px solid rgba(210, 153, 34, 0.4);
    }
</style>
"""

# Load mock AI output
AI_OUTPUT_FILE = "AI Copilot_Human-in-the-Loop/sample_ai_output.json"
APPROVED_FILE = "ai_copilot_hil_edit/approved_lessons.json"
VERSIONS_DIR = "ai_copilot_hil_edit/versions"

# Ensure directories exist
os.makedirs(VERSIONS_DIR, exist_ok=True)

# Load data
ai_data = load_json(AI_OUTPUT_FILE)
approved_data = load_json(APPROVED_FILE) if os.path.exists(APPROVED_FILE) else {}

# Session state for edits and approvals
if 'edits' not in st.session_state:
    st.session_state.edits = {}
if 'approvals' not in st.session_state:
    st.session_state.approvals = {}
if 'rejections' not in st.session_state:
    st.session_state.rejections = {}
if 'last_saved' not in st.session_state:
    st.session_state.last_saved = None
if 'rejection_comments' not in st.session_state:
    st.session_state.rejection_comments = {}
if 'diff_summaries' not in st.session_state:
    st.session_state.diff_summaries = {}
if 'editor_module_id' not in st.session_state:
    st.session_state.editor_module_id = None

# Helper functions
def bloom_badge(level):
    colors = {
        'Apply': 'bloom-apply',
        'Understand': 'bloom-understand',
        'Evaluate': 'bloom-evaluate'
    }
    return f'<span class="bloom-badge {colors.get(level, "")}">{level}</span>'

def show_progress():
    total_sections = len(ai_data['sections'])
    approved_count = sum(st.session_state.approvals.values())
    progress = approved_count / total_sections
    st.progress(progress)
    st.write(f"Progress: {approved_count}/{total_sections} sections approved")

def animated_header():
    st.markdown('<div class="hero-header">🎓 AI Copilot: Smart Module Editor</div>', unsafe_allow_html=True)

def footer():
    st.markdown("""
    <div class="custom-footer">
        <p>✨ Powered by AI & Streamlit | Built for Modern Educators</p>
    </div>
    """, unsafe_allow_html=True)

def modules_page():
    animated_header()
    st.markdown("### 📚 Module Library")
    
    modules = get_all_modules()
    
    if not modules:
        st.info("🎯 No modules in the database yet. Generate your first module to get started!")
        return
    
    # Stats at top
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📦 Total Modules", len(modules))
    with col2:
        draft_count = sum(1 for m in modules if m['status'] == 'draft')
        st.metric("📝 Drafts", draft_count)
    with col3:
        published_count = sum(1 for m in modules if m['status'] == 'published')
        st.metric("✅ Published", published_count)
    
    st.markdown("---")
    
    # Display modules in a styled dataframe
    module_df = pd.DataFrame([
        {
            'ID': m['id'],
            'Title': m['module_title'],
            'Status': m['status'].upper(),
            'Created': m['created_at'][:10],
            'Updated': m['updated_at'][:10]
        }
        for m in modules
    ])
    
    st.dataframe(module_df, use_container_width=True, height=300)
    
    # Select module to view details
    st.markdown("---")
    st.markdown("### 🔍 Module Details")
    
    module_titles = {m['id']: m['module_title'] for m in modules}
    selected_module_id = st.selectbox(
        "Select a module:",
        options=list(module_titles.keys()),
        format_func=lambda x: f"[ID: {x}] {module_titles[x]}"
    )
    
    if selected_module_id:
        module = get_module_by_id(selected_module_id)
        stats = get_module_stats(selected_module_id)
        
        # Stats cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📄 Total Sections", stats['total_sections'])
        with col2:
            st.metric("✅ Approved", stats['approved_count'])
        with col3:
            st.metric("❌ Rejected", stats['rejected_count'])
        with col4:
            st.metric("⏳ Pending", stats['pending_count'])
        
        st.markdown("---")
        
        # Display sections
        st.markdown("### 📋 Sections")
        for idx, section in enumerate(module['sections'], 1):
            with st.expander(f"{idx}. {section['title']} • {section['type'].replace('_', ' ').title()}", expanded=False):
                st.markdown(f"**ID:** `{section['section_id']}`")
                st.markdown(f"**Type:** {section['type']}")
                if section['bloom_level']:
                    st.markdown(f"**Bloom Level:** {section['bloom_level']}")
                
                st.markdown("**Content:**")
                st.text_area("", value=section['content'], height=100, disabled=True, key=f"view_{section['id']}")
                
                # Status badge
                if section['is_approved']:
                    st.markdown('<span class="status-badge status-approved">✅ Approved</span>', unsafe_allow_html=True)
                elif section['is_rejected']:
                    st.markdown(f'<span class="status-badge status-rejected">❌ Rejected</span>', unsafe_allow_html=True)
                    if section['rejection_comments']:
                        st.caption(f"💬 {section['rejection_comments']}")
                else:
                    st.markdown('<span class="status-badge status-pending">⏳ Pending</span>', unsafe_allow_html=True)
                
                # Version history
                versions = get_section_versions(section['id'])
                if versions and len(versions) > 0:
                    with st.expander(f"📜 Version History ({len(versions)} versions)"):
                        for v_idx, v in enumerate(versions, 1):
                            st.caption(f"**Version {v_idx}** • {v['created_at'][:16]}")
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.caption("Original:")
                                st.text(v['original_content'][:80] + "...")
                            with col_b:
                                st.caption("Edited:")
                                st.text(v['edited_content'][:80] + "...")
                            st.markdown("---")
        
        # Export option
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📥 Export as JSON", use_container_width=True):
                export_data = export_module_to_json(selected_module_id)
                st.json(export_data)
                st.download_button(
                    label="⬇️ Download JSON",
                    data=json.dumps(export_data, indent=2),
                    file_name=f"module_{selected_module_id}.json",
                    mime="application/json",
                    use_container_width=True
                )
    
    footer()

def generate_module_page():
    animated_header()
    st.markdown("### 🚀 Generate New Module")
    st.caption("Describe what you want to create and let AI build the module structure for you.")

    # Initialize session state
    if 'generated_module' not in st.session_state:
        st.session_state.generated_module = None
    if 'module_saved' not in st.session_state:
        st.session_state.module_saved = False

    # Input area
    user_prompt = st.text_area(
        "✍️ Module Description",
        height=150,
        placeholder="Example: Create a module about Python basics for beginners including variables, data types, and control flow..."
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("✨ Generate Module", use_container_width=True):
            if not user_prompt.strip():
                st.error("⚠️ Please provide a description for your module.")
            else:
                with st.spinner("🤖 AI is generating your module..."):
                    generated_data, error = generate_module("", "", user_prompt)

                if error:
                    st.error(f"❌ Generation failed: {error}")
                else:
                    st.success("🎉 Module generated successfully!")
                    st.session_state.generated_module = generated_data
                    st.session_state.module_saved = False

    # Preview section
    if st.session_state.generated_module:
        st.markdown("---")
        
        with st.expander("📋 Generated Module Preview", expanded=True):
            module_data = st.session_state.generated_module
            st.markdown(f"**Title:** {module_data.get('module_title', 'N/A')}")
            st.markdown(f"**Sections:** {len(module_data.get('sections', []))}")
            st.json(module_data)

        st.markdown("---")
        
        # Action buttons
        if not st.session_state.module_saved:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("📝 Load into Editor", use_container_width=True, type="primary"):
                    try:
                        module_id = save_module_to_db(
                            st.session_state.generated_module['module_title'], 
                            st.session_state.generated_module['sections']
                        )
                        save_json(AI_OUTPUT_FILE, st.session_state.generated_module)
                        st.session_state.module_saved = True
                        # Set the editor module id so Editor loads this module immediately
                        st.session_state.editor_module_id = module_id
                        st.success(f"✅ Module saved! (ID: {module_id})")
                        st.info("👉 Go to **Editor** to review and approve sections.")
                    except Exception as e:
                        st.error(f"❌ Error saving: {str(e)}")
        else:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.success("✅ Module is ready in the Editor!")
    
    footer()

def editor_page():
    animated_header()

    # Get latest module
    all_modules = get_all_modules()
    if not all_modules:
        st.info("🎯 No modules found. Generate a module first and load it into the editor.")
        return
    
    # all_modules is ordered by created_at DESC (newest first) in the DB helper
    # pick index 0 as the newest module
    latest_module_id = all_modules[0]['id']
    current_module = get_module_by_id(latest_module_id)
    
    if not current_module or 'sections' not in current_module:
        st.error("❌ Error loading module details.")
        return
    
    sections_data = current_module['sections']
    
    # Initialize session state safely for the current module and avoid KeyErrors
    if 'editor_module_id' not in st.session_state or st.session_state.editor_module_id != current_module['id']:
        st.session_state.editor_module_id = current_module['id']

        # Ensure core containers exist
        if 'approvals' not in st.session_state:
            st.session_state.approvals = {}
        if 'edits' not in st.session_state:
            st.session_state.edits = {}
        if 'rejections' not in st.session_state:
            st.session_state.rejections = {}
        if 'rejection_comments' not in st.session_state:
            st.session_state.rejection_comments = {}
        if 'diff_summaries' not in st.session_state:
            st.session_state.diff_summaries = {}

        # Populate defaults for all current sections and build valid id set
        valid_ids = set()
        for section in sections_data:
            # Prefer stable external section id; fallback to DB numeric id
            sec_key = section.get('section_id') or section.get('id')
            sec_key = str(sec_key)
            valid_ids.add(sec_key)

            # Populate missing entries
            if sec_key not in st.session_state.approvals:
                st.session_state.approvals[sec_key] = bool(section.get('is_approved', False))
            if sec_key not in st.session_state.edits:
                st.session_state.edits[sec_key] = section.get('content', '')
            if sec_key not in st.session_state.rejections:
                st.session_state.rejections[sec_key] = bool(section.get('is_rejected', False))
            if sec_key not in st.session_state.rejection_comments:
                st.session_state.rejection_comments[sec_key] = section.get('rejection_comments', '')
            if sec_key not in st.session_state.diff_summaries:
                st.session_state.diff_summaries[sec_key] = ''

        # Remove keys from previous modules that are no longer valid
        st.session_state.approvals = {k: v for k, v in st.session_state.approvals.items() if k in valid_ids}
        st.session_state.edits = {k: v for k, v in st.session_state.edits.items() if k in valid_ids}
        st.session_state.rejections = {k: v for k, v in st.session_state.rejections.items() if k in valid_ids}
        st.session_state.rejection_comments = {k: v for k, v in st.session_state.rejection_comments.items() if k in valid_ids}
        st.session_state.diff_summaries = {k: v for k, v in st.session_state.diff_summaries.items() if k in valid_ids}

    # Progress section with enhanced styling
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    st.markdown("### 📊 Module Progress")
    total_sections = len(sections_data)
    approved_count = sum(st.session_state.approvals.values())
    rejected_count = sum(st.session_state.rejections.values())
    progress = approved_count / total_sections if total_sections > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("✅ Approved", f"{approved_count}/{total_sections}")
    with col2:
        st.metric("❌ Rejected", rejected_count)
    with col3:
        st.metric("📈 Completion", f"{int(progress * 100)}%")
    
    st.progress(progress)
    st.markdown('</div>', unsafe_allow_html=True)

    # Check checkpoints
    checkpoints = [s for s in sections_data if s['type'] in ['learning_objective', 'assessment']]
    all_checkpoints_approved = all(st.session_state.approvals.get(s['section_id'], False) for s in checkpoints) if checkpoints else False

    if not all_checkpoints_approved:
        st.warning("⚠️ **Critical:** All Learning Objectives and Assessments must be approved before publishing.")

    # Publish button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Publish Module", disabled=not all_checkpoints_approved, use_container_width=True, type="primary"):
            try:
                publish_module(st.session_state.editor_module_id)
                st.session_state.last_saved = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.balloons()
                st.success("✅ Module published successfully! 🎉")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    if st.session_state.last_saved:
        st.info(f"📅 Last published: {st.session_state.last_saved}")

    st.markdown("---")

    # Two-column editor layout
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🤖 AI-Generated Content")
    with col2:
        st.markdown("### ✏️ Your Edits")

    # Sections
    for idx, section in enumerate(sections_data, 1):
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        
        badge = bloom_badge(section.get('bloom_level', '')) if 'bloom_level' in section else ''
        # Normalize section identifier to match session_state keys (prefer external section_id)
        section_id = str(section.get('section_id') or section.get('id'))
        
        # Header
        st.markdown(f"### {idx}. {section['title']} {badge}", unsafe_allow_html=True)
        st.caption(f"Type: {section['type'].replace('_', ' ').title()}")
        
        # Two columns for content
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_area(
                "AI Version",
                value=section['content'],
                height=180,
                disabled=True,
                key=f"ai_{section_id}",
                label_visibility="collapsed"
            )

        with col2:
            edited_text = st.text_area(
                "Your Edit",
                value=st.session_state.edits.get(section_id, section['content']),
                height=180,
                key=f"edit_{section_id}",
                label_visibility="collapsed"
            )
            st.session_state.edits[section_id] = edited_text

        # Action buttons
        btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
        
        with btn_col1:
            if st.button(f"✅ Accept", key=f"accept_{section_id}", use_container_width=True):
                st.session_state.approvals[section_id] = True
                st.session_state.rejections[section_id] = False
                try:
                    update_section_content(section['id'], edited_text)
                    approve_section(section['id'])
                    st.success("✅ Accepted!")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        with btn_col2:
            if st.button(f"❌ Reject", key=f"reject_{section_id}", use_container_width=True):
                st.session_state.approvals[section_id] = False
                st.session_state.rejections[section_id] = True
                comment = st.text_input(f"Reason for rejection:", key=f"comment_{section_id}")
                st.session_state.rejection_comments[section_id] = comment
                try:
                    reject_section(section['id'], comment)
                    st.warning("❌ Rejected")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        with btn_col3:
            if st.button(f"🔄 Reset", key=f"reset_{section_id}", use_container_width=True):
                st.session_state.edits[section_id] = section['content']
                st.info("🔄 Reset to AI version")
                st.rerun()
        
        with btn_col4:
            if st.button(f"✨ Regenerate", key=f"regenerate_{section_id}", use_container_width=True):
                try:
                    new_content = regenerate_content(edited_text)
                    st.session_state.edits[section_id] = new_content
                    st.success("✨ Regenerated!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

        # Show diff if edited
        if edited_text != section['content']:
            with st.expander("🔍 View Changes"):
                diff = difflib.unified_diff(
                    section['content'].splitlines(keepends=True),
                    edited_text.splitlines(keepends=True),
                    fromfile='AI',
                    tofile='Edited'
                )
                st.code(''.join(diff), language='diff')
                
                if st.button(f"🧠 AI Explain Changes", key=f"diff_{section_id}"):
                    if section_id not in st.session_state.diff_summaries:
                        try:
                            summary = summarize_changes(section['content'], edited_text)
                            st.session_state.diff_summaries[section_id] = summary
                        except Exception as e:
                            st.error(f"Summary failed: {str(e)}")
                    if section_id in st.session_state.diff_summaries:
                        st.info(st.session_state.diff_summaries[section_id])
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # Approval status summary
    st.markdown("---")
    st.markdown("### 📋 Approval Status Summary")
    
    status_data = []
    for section in sections_data:
        # Normalize section identifier to match session_state keys
        section_id = str(section.get('section_id') or section.get('id'))
        
        # Safe key lookup with default values
        is_approved = st.session_state.approvals.get(section_id, False)
        is_rejected = st.session_state.rejections.get(section_id, False)
        
        if is_approved:
            status = "✅ Approved"
            status_class = "status-approved"
        elif is_rejected:
            status = "❌ Rejected"
            status_class = "status-rejected"
        else:
            status = "⏳ Pending"
            status_class = "status-pending"
        
        status_data.append({
            "Section": section['title'],
            "Type": section['type'].replace('_', ' ').title(),
            "Status": status
        })

    status_df = pd.DataFrame(status_data)
    st.dataframe(status_df, use_container_width=True, height=300)

    footer()

def analytics_page():
    animated_header()
    st.markdown("### 📊 Analytics Dashboard")
    st.caption("Comprehensive insights into your module development process")

    # Calculate stats
    total_sections = len(ai_data['sections'])
    approved_count = sum(st.session_state.approvals.values())
    rejected_count = sum(st.session_state.rejections.values())
    pending_count = total_sections - approved_count - rejected_count

    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📄 Total Sections", total_sections)
    with col2:
        st.metric("✅ Approved", approved_count, delta=f"{int(approved_count/total_sections*100) if total_sections > 0 else 0}%")
    with col3:
        st.metric("❌ Rejected", rejected_count)
    with col4:
        st.metric("⏳ Pending", pending_count)

    st.markdown("---")

    # Charts
    col1, col2 = st.columns(2)

    bloom_counts = {}
    for section in ai_data['sections']:
        level = section.get('bloom_level', 'None')
        bloom_counts[level] = bloom_counts.get(level, 0) + 1

    with col1:
        st.markdown("#### 📊 Section Status Distribution")
        status_labels = ['Approved', 'Rejected', 'Pending']
        status_values = [approved_count, rejected_count, pending_count]
        fig_status = px.pie(
            values=status_values,
            names=status_labels,
            color_discrete_sequence=['#3fb950', '#f85149', '#d29922']
        )
        fig_status.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#E6EDF3'
        )
        st.plotly_chart(fig_status, use_container_width=True)

    with col2:
        st.markdown("#### 🌸 Bloom Level Distribution")
        bloom_labels = list(bloom_counts.keys())
        bloom_values = list(bloom_counts.values())
        fig_bloom = px.pie(
            values=bloom_values,
            names=bloom_labels,
            color_discrete_sequence=['#58A6FF', '#1F6FEB', '#238636', '#D29922']
        )
        fig_bloom.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#E6EDF3'
        )
        st.plotly_chart(fig_bloom, use_container_width=True)

    st.markdown("---")

    # Detailed statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Module Statistics")
        stats_df = pd.DataFrame({
            'Metric': ['Total Sections', 'Approved', 'Rejected', 'Pending', 'Completion'],
            'Value': [
                total_sections,
                approved_count,
                rejected_count,
                pending_count,
                f"{approved_count / total_sections * 100:.1f}%" if total_sections > 0 else "0%"
            ]
        })
        st.dataframe(stats_df, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("#### 🌸 Bloom Level Breakdown")
        bloom_df = pd.DataFrame(
            list(bloom_counts.items()),
            columns=['Bloom Level', 'Count']
        )
        st.dataframe(bloom_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Rejection log
    st.markdown("#### 📝 Rejection Log")
    rejection_data = []
    for section in ai_data['sections']:
        if st.session_state.rejections.get(section['id'], False):
            comment = st.session_state.rejection_comments.get(section['id'], 'No comment')
            rejection_data.append({
                'Section': section['title'],
                'Type': section['type'],
                'Reason': comment if comment else 'No reason provided'
            })
    
    if rejection_data:
        rejection_df = pd.DataFrame(rejection_data)
        st.dataframe(rejection_df, use_container_width=True, hide_index=True)
    else:
        st.info("✨ No rejections recorded. Great work!")

    footer()

# Main app
st.markdown(dark_css, unsafe_allow_html=True)

# Sidebar with enhanced styling
with st.sidebar:
    st.markdown("# 🎓 Navigation")
    st.markdown("---")
    
    page = st.radio(
        "Choose a page:",
        ["🚀 Generate Module", "📝 Editor", "📚 Module Library", "📊 Analytics"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 💡 Quick Tips")
    st.caption("• Generate modules with AI")
    st.caption("• Review & edit content")
    st.caption("• Track your progress")
    st.caption("• Publish when ready")

if page == "🚀 Generate Module":
    generate_module_page()
elif page == "📝 Editor":
    editor_page()
elif page == "📚 Module Library":
    modules_page()
elif page == "📊 Analytics":
    analytics_page()