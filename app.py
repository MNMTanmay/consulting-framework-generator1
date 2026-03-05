import streamlit as st
from openai import OpenAI

st.title("AI Consulting Framework Generator")

query = st.text_area("Paste Client Query")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

system_prompt = """
You are a senior strategy consulting research architect.

Steps:
1. Detect industry
2. Detect project type
3. Build consulting modules

Each module must include:
- Module Title
- Objective
- Key Questions
- Analysis Required
- Deliverables

Then generate a structured Table of Contents.
"""

if st.button("Generate Framework"):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    )

    result = response.choices[0].message.content

    st.write(result)
