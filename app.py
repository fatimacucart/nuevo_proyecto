import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

## Generation function
def llm_generate(llm_instance, prompt_text):
  template = ChatPromptTemplate.from_messages([
      ("system", "You are a digital marketing expert specialized in SEO and persuasive copywriting."),
      ("human", "{prompt}"),
  ])

  chain = template | llm_instance | StrOutputParser()

  res = chain.invoke({"prompt": prompt_text})
  return res

st.set_page_config(page_title="Content Generator 🤖", page_icon="🤖")
st.title("Content generator")

# API Key input
groq_api_key = st.text_input("Enter your GROQ API Key:", type="password")

# UI elements for content generation
topic = st.text_input("Topic:", placeholder="e.g., nutrition, mental health, routine check-ups, self-care tips, etc.")
platform = st.selectbox("Platform:", ['Instagram', 'Facebook', 'LinkedIn', 'Blog', 'E-mail'])
tone = st.selectbox("Message tone:", ['Normal', 'Informative', 'Inspiring', 'Urgent', 'Informal'])
length = st.selectbox("Text length:", ['Short', 'Medium', 'Long'])
audience = st.selectbox("Target audience:", ['All', 'Young adults', 'Families', 'Seniors', 'Teenagers'])
cta = st.checkbox("Include CTA")
hashtags = st.checkbox("Return Hashtags")
keywords = st.text_area("Keywords (SEO):", placeholder="Example: wellness, preventive healthcare...")

if st.button("Generate content"):
    if not groq_api_key:
        st.error("Please enter your GROQ API Key to generate content.")
    elif not topic:
        st.error("Please enter a topic to generate content.")
    else:
        # Set the API key for this session
        os.environ["GROQ_API_KEY"] = groq_api_key

        ## Connection with the LLM
        id_model = "llama-3.3-70b-versatile"
        try:
            llm = ChatGroq(
                model=id_model,
                temperature=0.7,
                max_tokens=None,
                timeout=None,
                max_retries=2,
            )
        except Exception as e:
            st.error(f"Failed to initialize LLM. Check your API key and network connection. Error: {e}")
            llm = None

        if llm:
            prompt_for_llm = f"""
            Write an SEO-optimized text on the topic '{topic}'.
            Return only the final text in your response and don't put it inside quotes.
            - Platform where it will be published: {platform}.
            - Tone: {tone}.
            - Target audience: {audience}.
            - Length: {length}.
            - {"Include a clear Call to Action." if cta else "Do not include a Call to Action."}
            - {"Include relevant hashtags at the end of the text." if hashtags else "Do not include hashtags."}
            {"- Keywords to include (for SEO): " + keywords if keywords else ""}
            """
            with st.spinner("Generating content..."):
                try:
                    res = llm_generate(llm, prompt_for_llm)
                    st.markdown(res)
                except Exception as e:
                    st.error(f"Error generating content: {e}")

