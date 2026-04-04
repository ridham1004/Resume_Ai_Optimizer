import streamlit as st
import os
from agent_tailor import run_agent_tailor, create_final_workspace

st.set_page_config(page_title="AI Resume Tailor", page_icon="🚀", layout="wide")

st.title("🚀 LaTeX AI Resume Tailor")
st.markdown("**Theme:** Innovate Beyond Boundaries — *Intelligently fitting your best experiences into strict spatial limits.*")

# --- Default Data Pool (Your Master Resume Data) ---
default_data_pool = """
*** TECHNICAL SKILLS ***
- Languages & Scripting: C, Kotlin, JavaScript/TypeScript, Java, Bash, VHDL, JavaCC
- AI & Machine Learning: Python (PyTorch, Pandas, NumPy), LLM APIs (Gemini, OpenAI, Perplexity)
- Full-Stack Development: React, Node.js, Git, Docker, CI/CD (GitHub Workflows), Kubernetes, Firebase, Postman
- Network & Data Analysis: Zeek, Elasticsearch, Logstash, Kibana (ELK Stack), Wireshark; data visualization for operational readouts

*** PROJECT EXPERIENCE ***
1. Vector-Matrix DSL Compiler | Java, JavaCC, JJTree, Bash | September 2025 - December 2025
- Built a custom language interpreter using JavaCC, implementing a recursive-descent parser that processed 4 types of control structures (loops, conditionals) and complex linear algebra syntax with 100% grammar compliance.
- Engineered an optimized Abstract Syntax Tree (AST) using JJTree and the Visitor Pattern, decoupling parsing logic from execution to reduce runtime complexity for nested matrix operations.
- Developed a Bash-based regression testing pipeline that validated the interpreter against 50+ edge-case inputs, ensuring data integrity across integer arithmetic, boolean logic, and recursive function calls.

2. Mini SIEM | Zeek, Filebeat, Elasticsearch, Logstash, Kibana | July 2025 - August 2025
- Engineered and documented an end-to-end network monitoring solution using Zeek, Logstash, Elasticsearch, and Kibana; ensured system stability through detailed process management and permissions troubleshooting.
- Designed and implemented a SIEM using Zeek for network monitoring, Elasticsearch for log storage, Kibana for visualization, and Logstash for ingestion to analyze 1773 Zeek log documents.
- Implemented data ingestion and dashboards on Zeek/Elasticsearch/Kibana, then iterated detections and visuals to make findings actionable; validated changes with targeted tests and debug traces on Linux.

3. General Purpose Processor (ALU) | Quartus, VHDL, FPGA | September 2024 - December 2024
- Designed and verified an 8-bit ALU with 9 operations driven by a 16-bit OP microcode and a 9-state FSM; validated behavior via Quartus functional simulation and displayed results on two seven-segment hex outputs.
- Built two 8-bit registers with rising-edge capture and synchronous transfer; extended a prior 3x8 decoder into a 4x16 selector to route control signals, wiring named buses for clean, hierarchical integration.

4. CUAI -- Custodial Management AI | DMZ Basecamp 2025 Cohort | July 2025 - August 2025
- Led collaborative development of a custodial management AI MVP; coordinated milestones, aligned stakeholders, and delivered operational forecasts to support project decisions in a regulated, high-accountability environment.
- Led discovery with operations staff; storyboarded Lighthouse API integration and mock dashboards to align value proposition and GTM.

5. AppliFlow | JavaScript, Postman, Firebase, Next.js, Google APIs | January 2025 - August 2025
- Delivered user-facing features for a Chrome extension by translating requirements into small, testable tasks, instrumenting edge cases, and refining UX with structured feedback loops in each sprint.
- Integrated Google Drive and service APIs with attention to auth, error handling, and latency, documenting request/response contracts to streamline code reviews and future changes.

6. Carpool Matching System | Python (NumPy, Pandas, Geopy), SQL | October 2024
- Built a Python carpool matcher to reduce commute inefficiency by pairing drivers and riders by route/schedule, enforcing 4 constraints: non-smoking, same-gender, max detour, seating capacity, yielding valid groups.
- Standardized inputs via parsing/validation across user, location (lat/long), time, preferences, and capacity fields, enabling consistent grouping and clear visualizations.

*** LEADERSHIP & VOLUNTEER EXPERIENCE ***
1. International Commissioner | Metropolitan Undergraduate Engineering Society (MUES) | TMU | June 2025 - Present
- Liaised for 200+ international engineering students; presented challenges to MUES Board, securing representation and timely issue resolution.
- Launched tailored workshops for international students, increasing MUES event engagement 40% by adapting topics, schedules, and support resources.

2. Engineering ACES Peer Tutor | FEAS | TMU | June 2025 - Present
- Led weekly calculus and linear algebra tutoring for 40+ first year students; redesigned lessons, improving average exam scores by 15%.
- Developed 10+ study guides and peer workshops, increasing repeat attendance 30% and raising course pass rates by 12 percentage points.
"""

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. The Target")
    jd_input = st.text_area("Paste the Job Description here:", height=500, placeholder="Paste JD here...")

with col2:
    st.subheader("2. Your Data Pool (Source of Truth)")
    data_pool_input = st.text_area("Your Master Data:", value=default_data_pool, height=500)

st.markdown("---")

if st.button("🎯 Generate Tailored Workspace", type="primary", use_container_width=True):
    if not jd_input.strip():
        st.error("Please paste a Job Description first!")
    else:
        with st.spinner("🤖 Multi-Agent System is analyzing the JD and writing strict LaTeX code..."):
            
            result = run_agent_tailor(jd_input, data_pool_input)
            
            if result:
                st.success("✅ AI generation complete!")
                
                with st.spinner("📁 Compiling LaTeX files and creating workspace..."):
                    create_final_workspace(result, jd_input)
                
                st.balloons()
                st.success("🎉 Success! Your tailored `.tex` files have been generated in your workspace folder.")
                
                with st.expander("🔍 View Raw AI Output (JSON)"):
                    st.json(result)
            else:
                st.error("Generation failed. Check your terminal for errors.")