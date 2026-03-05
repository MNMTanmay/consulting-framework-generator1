import streamlit as st
from groq import Groq
from docx import Document
import json

st.title("Consulting AI Intelligence Engine")

query = st.text_area("Paste Client Query")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

CURRENT_YEAR = 2025
FORECAST_YEAR = 2030


# ------------------------------------------------
# FRAMEWORK LIBRARY
# ------------------------------------------------

FRAMEWORK_LIBRARY = {

"market_opportunity":[
"Industry Overview",
"Product Definition",
"Application Landscape",
"Market Drivers",
"Technology Trends",
"Regulatory Landscape",
"Competitive Landscape",
"Market Size Analysis",
"Forecast Opportunities",
"High Growth Segments"
],

"technology_landscape":[
"Industry Overview",
"Technology Architecture",
"Key Applications",
"Emerging Use Cases",
"Innovation Trends",
"Technology Roadmap",
"Key Technology Companies"
],

"market_entry":[
"Industry Overview",
"Market Structure",
"Competitive Landscape",
"Customer Segments",
"Regulatory Barriers",
"Entry Strategy Options",
"Implementation Roadmap"
]

}


# ------------------------------------------------
# QUERY PARSER
# ------------------------------------------------

def parse_query(query):

    prompt=f"""
Extract structured data from the client query.

Return JSON format.

Fields:
Industry
Product
Applications
Geography
Project_Type
Keywords

Query:
{query}
"""

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content


# ------------------------------------------------
# PROJECT TYPE DETECTION
# ------------------------------------------------

def detect_project_type(query):

    prompt=f"""
Classify the consulting project type.

Options:
market_opportunity
technology_landscape
market_entry

Query:
{query}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content.strip()


# ------------------------------------------------
# TOC GENERATOR
# ------------------------------------------------

def build_toc(framework):

    toc=""

    for i,section in enumerate(framework,1):

        toc+=f"{i}. {section}\n"

    return toc


# ------------------------------------------------
# MODULE GENERATOR
# ------------------------------------------------

def generate_modules(query,framework):

    prompt=f"""
Create consulting research modules.

Sections:
{framework}

For each section include:

Objective
Key Questions
Analysis Required
Deliverables

Also include market sizing for {CURRENT_YEAR} and forecast to {FORECAST_YEAR} where relevant.

Query:
{query}
"""

    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content


# ------------------------------------------------
# KEY PLAYER DETECTION
# ------------------------------------------------

def detect_players(query):

    prompt=f"""
Identify leading manufacturers or companies relevant to this market.

Return 5–10 companies.

Query:
{query}
"""

    response=client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content


# ------------------------------------------------
# RESEARCH METHODOLOGY
# ------------------------------------------------

def research_methodology():

    return """
Research Methodology

• Secondary research across industry databases
• Patent and innovation analysis
• Competitive benchmarking
• Supply chain mapping
• Expert interviews with industry stakeholders
• Market sizing using top-down and bottom-up methods
"""


# ------------------------------------------------
# WORD REPORT
# ------------------------------------------------

def create_word(query,toc,modules,players):

    doc=Document()

    doc.add_heading("Consulting Research Framework",level=1)

    doc.add_heading("Client Query",level=2)
    doc.add_paragraph(query)

    doc.add_heading("Table of Contents",level=2)
    doc.add_paragraph(toc)

    doc.add_heading("Key Companies",level=2)
    doc.add_paragraph(players)

    doc.add_heading("Consulting Modules",level=2)
    doc.add_paragraph(modules)

    doc.add_heading("Research Methodology",level=2)
    doc.add_paragraph(research_methodology())

    doc.save("consulting_framework.docx")


# ------------------------------------------------
# MAIN ENGINE
# ------------------------------------------------

if st.button("Generate Consulting Framework"):

    st.subheader("Query Analysis")

    parsed=parse_query(query)

    st.write(parsed)

    project_type=detect_project_type(query)

    st.subheader("Project Type")

    st.write(project_type)

    if project_type not in FRAMEWORK_LIBRARY:

        project_type="market_opportunity"

    framework=FRAMEWORK_LIBRARY[project_type]

    toc=build_toc(framework)

    st.subheader("Dynamic Table of Contents")

    st.write(toc)

    modules=generate_modules(query,framework)

    st.subheader("Consulting Modules")

    st.write(modules)

    players=detect_players(query)

    st.subheader("Key Companies")

    st.write(players)

    create_word(query,toc,modules,players)

    with open("consulting_framework.docx","rb") as f:

        st.download_button(
            label="Download Word Report",
            data=f,
            file_name="consulting_framework.docx"
        )
