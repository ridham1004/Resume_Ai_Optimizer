import streamlit as st
import os
from agent_tailor import run_agent_tailor, create_final_workspace

st.set_page_config(page_title="AI Resume Tailor", page_icon="🚀", layout="wide")

st.title("🚀 LaTeX AI Resume Tailor")
st.markdown("**Theme:** Innovate Beyond Boundaries — *Intelligently fitting your best experiences into strict spatial limits.*")

# --- Resume Upload ---
st.subheader("📄 Upload Your LaTeX Resume")
uploaded_file = st.file_uploader("Upload your master resume (.tex file):", type=["tex"])

candidate_name = "candidate"
data_pool_default = ""

if uploaded_file is not None:
    file_content = uploaded_file.read().decode("utf-8")
    # Derive candidate name from the uploaded filename (strip extension)
    candidate_name = os.path.splitext(uploaded_file.name)[0]
    data_pool_default = file_content
    st.success(f"✅ Loaded resume: `{uploaded_file.name}`")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. The Target")
    jd_input = st.text_area("Paste the Job Description here:", height=500, placeholder="Paste JD here...")

with col2:
    st.subheader("2. Your Data Pool (Source of Truth)")
    data_pool_input = st.text_area(
        "Your Master Data (auto-filled from uploaded resume, or paste manually):",
        value=data_pool_default,
        height=500,
        placeholder="Upload a .tex resume above, or paste your skills and experience here...",
    )

st.markdown("---")

if st.button("🎯 Generate Tailored Workspace", type="primary", use_container_width=True):
    if not jd_input.strip():
        st.error("Please paste a Job Description first!")
    elif not data_pool_input.strip():
        st.error("Please upload a resume or paste your data pool first!")
    else:
        with st.spinner("🤖 Multi-Agent System is analyzing the JD and writing strict LaTeX code..."):
            
            result = run_agent_tailor(jd_input, data_pool_input)
            
            if result:
                st.success("✅ AI generation complete!")
                
                with st.spinner("📁 Compiling LaTeX files and creating workspace..."):
                    create_final_workspace(result, jd_input, candidate_name)
                
                st.balloons()
                st.success("🎉 Success! Your tailored `.tex` files have been generated in your workspace folder.")
                
                with st.expander("🔍 View Raw AI Output (JSON)"):
                    st.json(result)
            else:
                st.error("Generation failed. Check your terminal for errors.")