import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Consulting Framework Generator")

st.title("AI Consulting Framework Generator")

query = st.text_area("Paste Client Query")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

system_prompt = """
You are a senior strategy consulting architect.

Convert a client query into a consulting research framework.

Steps:
1. Detect industry
2. Detect consulting project type
3. Build consulting research modules

Each module must contain:
• Objective
• Key Questions
• Analysis Required
• Deliverables

Also generate a structured consulting Table of Contents.

The framework must adapt based on the query topic.
"""

if st.button("Generate Framework"):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ],
        temperature=0.3
    )

    result = response.choices[0].message.content

    st.write(result)
