import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

load_dotenv(Path(__file__).parent / ".env")

# Load documents
files = ["campus_guidelines.txt", "department_rules.txt"]
docs = []
for f in files:
    docs.extend(TextLoader(f).load())

# Chunking
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300, chunk_overlap=50
)
chunks = splitter.split_documents(docs)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
db = Chroma.from_documents(chunks, embeddings)
retriever = db.as_retriever(search_kwargs={"k": 3})

llm = ChatGroq(

    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

# Prompt
prompt = PromptTemplate.from_template(
    """Answer using ONLY the context.
If unavailable, say "I don't have that information."
Context:
{context}Question: {question}Answer:"""
)
# RAG
def run_agent(query):
    docs = retriever.invoke(query)
    context = "\n\n".join(d.page_content for d in docs)

    answer = (prompt | llm).invoke({
        "context": context,
        "question": query
    })
    print("\nAnswer:", answer.content)
    print("\nSources:")
    for d in docs:
        print("-", d.metadata.get("source", "unknown"))
while True:
    q = input("\nAsk your question (exit to quit): ")

    if q.lower() == "exit":
        break

    run_agent(q)