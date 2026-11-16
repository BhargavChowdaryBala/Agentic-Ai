import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

load_dotenv()

# Step 1: Load the knowledge base from the file
loader = TextLoader("career_notes.txt", encoding="utf-8")
documents = loader.load()


print(len(documents))
# Step 2: Split the document into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=40)
chunks = splitter.split_documents(documents)
print("Number of chunks:", len(chunks))

# Step 3: Embed the chunks and store them in FAISS
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vector_store = FAISS.from_documents(chunks, embeddings)

# Step 4: Create a retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# Step 5: Prompt template
prompt = ChatPromptTemplate.from_template(
    """You are a friendly career mentor for engineering students. Using only
the context below, recommend the single best-fitting role, explain in one or two
sentences why it fits the student, and state the approximate entry-level package
range. If the context does not contain the answer, say so.

Context:
{context}

Student's question: {question}
"""
)

# Step 6: LLM and output parser
llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash")
output_parser = StrOutputParser()

# # Step 7: Format retrieved documents
# def format_docs(retrieved_docs):
#     return "\n\n".join(doc.page_content for doc in retrieved_docs)

# Step 8: RAG chain
rag_chain = (
    {"context": retriever , "question": RunnablePassthrough()}
    | prompt
    | llm
    | output_parser
)

# Step 9: Ask a question
question = "I love automating repetitive tasks and setting up Docker containers, but I'm not interested in designing networks. Which career suits me, and what package can I expect?"
answer = rag_chain.invoke(question)

print("Bhargav Chowdary")
print("23A81A0507")
print("Question:", question)
print("\nCareer Advisor Answer:\n", answer)