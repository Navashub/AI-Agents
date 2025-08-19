from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="llama3.2")

template = """
You are an exeprt in answering questions about LUXDEV Data Engineering Course Outline

Here are some markdown for lux: {markdown}

Here is the question to answer: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# results = chain.invoke({"markdown": [], "question": "What topics are offered in Lux Data engineering"})
# print(results)

while True:
    print("\n\n-------------------------------")
    question = input("Ask your question (q to quit): ")
    print("\n\n")
    if question == "q":
        break
    
    markdown = retriever.invoke(question)
    result = chain.invoke({"markdown": markdown, "question": question})
    print(result)