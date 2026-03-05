import streamlit as st
from openai import OpenAI
import docx
from io import BytesIO

st.title("AI Consulting Framework Generator")

query = st.text_area("Paste Client Query")

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

system_prompt = """
You are a senior strategy consulting research architect.

When a client query is given you must:

STEP 1 — Detect Industry
Identify the industry sector.

STEP 2 — Detect Project Type
Classify the project into:
Market Study
Market Entry
Technology Assessment
Competitive Intelligence
M&A Opportunity

STEP 3 — Build Consulting Framework

Create 6–8 consulting modules.

Each module must contain:

MODULE TITLE
Objective
Key Questions
Analysis Required
Deliverables

STEP 4 — Generate Structured Table of Contents

The framework must adapt depending on the industry.

Examples:

Healthcare → include regulatory and clinical workflow
Data Centers → include hyperscalers, GPUs, power demand
Chemicals → include value chain and feedstock
"""

if st.button("Generate Framework"):

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":query}
        ],
        temperature=0.7
    )

    result = response.choices[0].message.content

    st.write(result)

    # Create Word file
    doc = docx.Document()
    doc.add_heading("Consulting Framework", level=1)
    doc.add_paragraph(result)

    buffer = BytesIO()
    doc.save(buffer)

    st.download_button(
        label="Download Word",
        data=buffer.getvalue(),
        file_name="consulting_framework.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
