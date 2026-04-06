import vertexai
from vertexai.generative_models import GenerativeModel
import json
import os

# Initialize Vertex AI
vertexai.init(project="YOUR_GCP_PROJECT_ID", location="us-central1")

def load_prompt(filename):
    """Helper function to read the markdown prompt files."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Could not find {filename}. Make sure it is in your folder.")
        return ""

def run_agent_tailor(job_description, user_data_pool):
    model = GenerativeModel("gemini-2.5-pro")
    
    resume_sys_instruction = load_prompt("resume_prompt.md")
    cl_sys_instruction = load_prompt("coverletter_prompt.md")
    
    user_prompt = f"""
    JOB DESCRIPTION / COURSE DETAILS:
    {job_description}
    
    POOL OF DATA (Source of Truth):
    {user_data_pool}
    """

    final_data = {}

    print("Agent 1 (Resume) is tailoring...")
    try:
        resume_response = model.generate_content(
            resume_sys_instruction + "\n\n" + user_prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        resume_data = json.loads(resume_response.text)
        final_data.update(resume_data)
    except Exception as e:
        print(f"Agent 1 Error: {e}")
        return None

    print("Agent 2 (Cover Letter) is tailoring...")
    try:
        cl_response = model.generate_content(
            cl_sys_instruction + "\n\n" + user_prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        cl_data = json.loads(cl_response.text)
        final_data.update(cl_data)
    except Exception as e:
        print(f"Agent 2 Error: {e}")
        return None

    print("Both Agents successfully generated tailored content!\n")
    return final_data

def create_final_workspace(tailored_data, jd_text, candidate_name="candidate"):
    print("Injecting AI data into LaTeX templates...")
    
    try:
        with open("resume_tempelate.tex", "r", encoding="utf-8") as f:
            resume_tex = f.read()
            
        with open("coverletter_tempelate.tex", "r", encoding="utf-8") as f:
            cl_tex = f.read()
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: {e}")
        print("Please check that your template files are named exactly 'resume_tempelate.tex' and 'coverletter_tempelate.tex'")
        return

    resume_tex = resume_tex.replace("{{SUMMARY_PLACEHOLDER}}", tailored_data.get("summary", ""))
    resume_tex = resume_tex.replace("{{SKILLS_PLACEHOLDER}}", tailored_data.get("skills", ""))
    resume_tex = resume_tex.replace("{{COURSEWORK_PLACEHOLDER}}", tailored_data.get("coursework", ""))
    resume_tex = resume_tex.replace("{{EXPERIENCE_PLACEHOLDER}}", tailored_data.get("experience", ""))
    resume_tex = resume_tex.replace("{{LEADERSHIP_PLACEHOLDER}}", tailored_data.get("leadership", ""))

    cl_body = tailored_data.get("cover_letter_body", "")
    cl_tex = cl_tex.replace("{{COVER\\_LETTER\\_BODY}}", cl_body)
    
    company = tailored_data.get("company_name", "")
    if not company or company.lower() == "hiring":
        company = "The" 
        
    cl_tex = cl_tex.replace("{{COMPANY\\_NAME}}", company)
    cl_tex = cl_tex.replace("{{JOB\\_ROLE}}", tailored_data.get("job_role", "Software Engineer Intern"))

    role_clean = tailored_data.get("job_role", "Role").replace(" ", "_")
    company_clean = company.replace(" ", "_")
    folder_name = f"{role_clean}_{company_clean}"
    
    os.makedirs(folder_name, exist_ok=True)

    with open(os.path.join(folder_name, f"{candidate_name}_resume.tex"), "w", encoding="utf-8") as f:
        f.write(resume_tex)
        
    with open(os.path.join(folder_name, f"{candidate_name}_coverletter.tex"), "w", encoding="utf-8") as f:
        f.write(cl_tex)
        
    with open(os.path.join(folder_name, "job_description.txt"), "w", encoding="utf-8") as f:
        f.write(jd_text)

    print(f"\nSUCCESS! 🚀")
    print(f"Your tailored workspace has been created at: ./{folder_name}/")


if __name__ == "__main__":
    # Paste a job description here to test from the terminal
    target_jd = """
    [Paste your Job Description here]
    """
    
    my_data_pool = """
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
    - Delivered a reproducible top-level system with clock/reset handling and documented runbooks/state diagrams; integrated 4 core modules (Registers, Control Unit, ALU, Display) to meet the 2-week deliverable with deterministic sequencing across states 0-8.

    4. CUAI -- Custodial Management AI | DMZ Basecamp 2025 Cohort | July 2025 - August 2025
    - Led collaborative development of a custodial management AI MVP; coordinated milestones, aligned stakeholders, and delivered operational forecasts to support project decisions in a regulated, high-accountability environment.
    - Led discovery with operations staff; storyboarded Lighthouse API integration and mock dashboards to align value proposition and GTM.
    - Delivered a pitch forecasting 25% higher schedule accuracy, 40% fewer manual call-outs, 15% higher cleanliness, and 10% fewer urgent responses; outlined a roadmap for real-time sensor feedback, predictive alerting, and expansion across terminals.

    5. AppliFlow | JavaScript, Postman, Firebase, Next.js, Google APIs | January 2025 - August 2025
    - Delivered user-facing features for a Chrome extension by translating requirements into small, testable tasks, instrumenting edge cases, and refining UX with structured feedback loops in each sprint.
    - Integrated Google Drive and service APIs with attention to auth, error handling, and latency, documenting request/response contracts to streamline code reviews and future changes.
    - Built a Job Tracker panel to save roles and track which document versions were used, resulting in a 60% increase in organized follow-ups.

    6. Carpool Matching System | Python (NumPy, Pandas, Geopy), SQL | October 2024
    - Built a Python carpool matcher to reduce commute inefficiency by pairing drivers and riders by route/schedule, enforcing 4 constraints: non-smoking, same-gender, max detour, seating capacity, yielding valid groups.
    - Standardized inputs via parsing/validation across user, location (lat/long), time, preferences, and capacity fields, enabling consistent grouping and clear visualizations.
    - Added 2 evaluation modules, time-compatibility checks and carbon-footprint estimation to assess per-trip feasibility and sustainability.

    *** LEADERSHIP & VOLUNTEER EXPERIENCE ***
    1. International Commissioner | Metropolitan Undergraduate Engineering Society (MUES) | TMU | June 2025 - Present
    - Liaised for 200+ international engineering students; presented challenges to MUES Board, securing representation and timely issue resolution.
    - Launched tailored workshops for international students, increasing MUES event engagement 40% by adapting topics, schedules, and support resources.

    2. Engineering ACES Peer Tutor | FEAS | TMU | June 2025 - Present
    - Led weekly calculus and linear algebra tutoring for 40+ first year students; redesigned lessons, improving average exam scores by 15%.
    - Developed 10+ study guides and peer workshops, increasing repeat attendance 30% and raising course pass rates by 12 percentage points.

    3. VP of Events | Academic Integrity Office | Toronto Metropolitan University | May 2024 - August 2025
    - Led coordination of 11 workshops, attracting 300+ participants, integrating content into TMU's orientation program with a focus on student success.
    - Facilitated group discussions and presented data-driven insights, enhancing community participation by 80% through innovative event strategies.
    """
    
    result = run_agent_tailor(target_jd, my_data_pool)
    
    if result:
        create_final_workspace(result, target_jd)