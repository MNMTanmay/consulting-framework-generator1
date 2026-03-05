import streamlit as st
from groq import Groq
from docx import Document

st.set_page_config(page_title="Consulting AI Framework Generator")

st.title("AI Consulting Framework Generator")

query = st.text_area("Paste Client Query")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])


# -----------------------------
# INDUSTRY DETECTION
# -----------------------------

def detect_industry(query):

    prompt = f"""
Extract the following from the client query.

Return JSON format.

Fields:
Industry
Product_or_Technology
Applications
Project_Type

Query:
{query}
"""

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content


# -----------------------------
# FRAMEWORK GENERATOR
# -----------------------------

def generate_framework(query):

    prompt = f"""
You are a senior strategy consulting architect.

Create a consulting research framework for the following client query.

The framework must include:

1. Industry Definition
2. Product / Technology Definition
3. Key Applications
4. Emerging Applications
5. Market Drivers
6. Technology Trends
7. Regulatory Landscape
8. Competitive Landscape (Key Manufacturers)
9. Market Size (2025) and Forecast (2030)
10. High Growth Opportunities
11. Research Methodology

Each section must contain:

Objective
Key Questions
Analysis Required
Deliverables

Query:
{query}
"""

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role":"user","content":prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content


# -----------------------------
# TOC GENERATOR
# -----------------------------

def generate_toc(query):

    prompt = f"""
Create a consulting style Table of Contents.

Include:

Industry definition
Product definition
Applications
Market size
Technology trends
Competitive landscape
Regulation
Opportunities
Forecast 2025–2030

Query:
{query}
"""

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content


# -----------------------------
# WORD EXPORT
# -----------------------------

def create_word(framework):

    doc = Document()
    doc.add_heading("Consulting Research Framework", level=1)

    for line in framework.split("\n"):
        doc.add_paragraph(line)

    doc.save("framework.docx")


# -----------------------------
# UI BUTTON
# -----------------------------

if st.button("Generate Framework"):

    st.subheader("Industry Detection")

    industry = detect_industry(query)

    st.write(industry)

    st.subheader("Dynamic Table of Contents")

    toc = generate_toc(query)

    st.write(toc)

    st.subheader("Consulting Framework")

    framework = generate_framework(query)

    st.write(framework)

    create_word(framework)

    with open("framework.docx", "rb") as file:
        st.download_button(
            label="Download Word Report",
            data=file,
            file_name="Consulting_Framework.docx"
        )
