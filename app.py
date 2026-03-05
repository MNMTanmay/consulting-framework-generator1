import streamlit as st
from groq import Groq
from docx import Document

st.set_page_config(page_title="Consulting Intelligence Engine")

st.title("Consulting AI Intelligence Engine")

query = st.text_area("Paste Client Query")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

CURRENT_YEAR = 2025
FORECAST_YEAR = 2030


# ------------------------------------------------
# UNIVERSAL CONSULTING FRAMEWORK
# ------------------------------------------------

FRAMEWORK = [
"Industry Context",
"System Architecture",
"Product / Technology Definition",
"Application Landscape",
"Material or Technology Substitution",
"Industry Value Chain",
"Technology Roadmap",
"Regulatory and Safety Landscape",
"Competitive Landscape",
"Regional Market Analysis",
"Market Size Estimation",
"Revenue Pools by Application",
"High Growth Segments",
"Strategic Opportunity Matrix"
]


# ------------------------------------------------
# QUERY PARSER
# ------------------------------------------------

def parse_query(query):

    prompt=f"""
Extract structured information from the query.

Return JSON format.

Fields:

Industry
Product_or_Technology
Applications
Geography
Keywords

If geography not mentioned assume Global.

Query:
{query}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content


# ------------------------------------------------
# ARCHITECTURE MAPPING (SHORT BULLETS)
# ------------------------------------------------

def architecture_mapping(query):

    prompt=f"""
Identify the system architecture relevant to this query.

Return concise bullet points.

Highlight where the product fits.

Example output style:

• Cell  
• Module  
• Pack  
• Thermal management  

Query:
{query}
"""

    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content


# ------------------------------------------------
# STRATEGIC QUESTIONS GENERATOR
# ------------------------------------------------

def generate_questions(section,query):

    prompt=f"""
Generate 3–4 strategic consulting questions.

Section:
{section}

Query:
{query}

Return concise analytical questions.
"""

    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content


# ------------------------------------------------
# KEY PLAYERS
# ------------------------------------------------

def detect_players(query):

    prompt=f"""
Identify 8–10 leading companies relevant to this market.

Return bullet list.

Query:
{query}
"""

    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content


# ------------------------------------------------
# REVENUE POOLS
# ------------------------------------------------

def revenue_pools(query):

    prompt=f"""
Identify key revenue pools for this product in the market.

Break down by application.

Highlight growth drivers.

Query:
{query}
"""

    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content


# ------------------------------------------------
# RESEARCH METHODOLOGY
# ------------------------------------------------

def research_methodology():

    return """

Research Methodology

This study integrates multiple analytical approaches.

Market Estimation
• Top-down market modeling
• Bottom-up demand calculations
• Norm-based material intensity modeling

Data Sources
• Internal database of 50,000+ research reports
• Industry publications and regulatory filings
• Company disclosures and technical papers

Primary Intelligence
• Interviews with manufacturers
• Discussions with suppliers
• Expert consultations

Continuous Market Intelligence
• Daily monitoring of industry news
• Technology announcements
• policy developments

"""


# ------------------------------------------------
# MODULE GENERATOR
# ------------------------------------------------

def generate_modules(query):

    output=""

    for section in FRAMEWORK:

        questions=generate_questions(section,query)

        output+=f"\n\n{section}\n"

        output+=questions

    return output


# ------------------------------------------------
# WORD EXPORT
# ------------------------------------------------

def create_word(query,parsed,architecture,revenue,players,modules):

    doc=Document()

    doc.add_heading("Consulting Research Framework",level=1)

    doc.add_heading("Client Query",level=2)
    doc.add_paragraph(query)

    doc.add_heading("Query Analysis",level=2)
    doc.add_paragraph(parsed)

    doc.add_heading("Research Methodology",level=2)
    doc.add_paragraph(research_methodology())

    doc.add_heading("System Architecture",level=2)
    doc.add_paragraph(architecture)

    doc.add_heading("Revenue Pools",level=2)
    doc.add_paragraph(revenue)

    doc.add_heading("Key Companies",level=2)
    doc.add_paragraph(players)

    doc.add_heading("Consulting Framework",level=2)
    doc.add_paragraph(modules)

    doc.save("consulting_framework.docx")


# ------------------------------------------------
# MAIN ENGINE
# ------------------------------------------------

if st.button("Generate Consulting Framework"):

    st.subheader("Query Analysis")

    parsed=parse_query(query)

    st.write(parsed)

    st.subheader("Architecture Mapping")

    architecture=architecture_mapping(query)

    st.write(architecture)

    st.subheader("Revenue Pools")

    revenue=revenue_pools(query)

    st.write(revenue)

    st.subheader("Key Companies")

    players=detect_players(query)

    st.write(players)

    st.subheader("Consulting Framework")

    modules=generate_modules(query)

    st.write(modules)

    create_word(query,parsed,architecture,revenue,players,modules)

    with open("consulting_framework.docx","rb") as f:

        st.download_button(
            label="Download Word Report",
            data=f,
            file_name="consulting_framework.docx"
        )
