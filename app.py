import streamlit as st
from groq import Groq

st.title("AI Consulting Framework Generator")

query = st.text_area("Paste Client Query")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

system_prompt = """
You are a senior strategy consulting architect.

Steps:
1. Detect industry
2. Detect consulting project type
3. Create research modules

Each module must include:
- Objective
- Key Questions
- Analysis Required
- Deliverables

Finally generate a structured consulting Table of Contents.
"""

if st.button("Generate Framework"):

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    )

    result = response.choices[0].message.content

    st.write(result)
