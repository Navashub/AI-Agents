import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
load_dotenv()

st.title("AI translator App")
st.divider()
st.markdown("## Translate text to any language.")


language_to_translate = st.selectbox(
    label="Language to translate to:",
    options=["English", "Spanish", "French", "Japanese"]
)

text_to_translate = st.text_area("Paste text here:")

translate_btn = st.button("Translate")


#models 
groq_llm = ChatGroq(model="llama-3.1-8b-instant")

# Chat prompt template
chat_prompt_template = ChatPromptTemplate.from_messages(
    [("system", "You are a professional translator. Your task is to translate the following text to {language}"), ("user", "{text}")
    ]
)

prompt = chat_prompt_template.invoke({
    "language": language_to_translate,
    "text": text_to_translate
})

if translate_btn and text_to_translate.strip() != "":
    placeholder = st.empty()
    full_translation = ""

    for chunk in groq_llm.stream(prompt):
        full_translation += chunk.content
        placeholder.text(full_translation)

elif translate_btn:
    st.error("Please provide the text to translate.")