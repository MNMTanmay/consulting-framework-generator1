import streamlit as st
import openai

st.set_page_config(page_title="AI Consulting Framework Generator")

st.title("AI Consulting Framework Generator")

st.write("Paste a client query and generate a consulting research framework.")

query = st.text_area("Client Query")

openai.api_key = "PASTE_YOUR_OPENAI_API_KEY"

if st.button("Generate Framework"):

    system_prompt = """
You are a senior strategy consulting research architect.

Your task is to transform any client query into a consulting project framework.

Steps:

1 Detect the industry
2 Detect the project type
3 Extract stakeholders and objectives
4 Generate consulting modules

Each module must include:

MODULE TITLE
Objective
Key Questions
Analysis Required
Deliverables

After modules, generate a structured consulting Table of Contents.

The framework must adapt depending on the query topic.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":query}
        ],
        temperature=0.7
    )

    result = response["choices"][0]["message"]["content"]

    st.write(result)
