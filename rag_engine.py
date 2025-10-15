import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

class RAGEngine:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.vectorstore = None
        # Use a mock or local embeddings for testing without API calls
        # self.embeddings = OpenAIEmbeddings()
        self.embeddings = None  # Placeholder for now

    def load_documents(self):
        documents = []
        for file in os.listdir(self.data_dir):
            if file.endswith('.txt'):
                loader = TextLoader(os.path.join(self.data_dir, file))
                documents.extend(loader.load())
        return documents

    def build_vectorstore(self):
        documents = self.load_documents()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        # Mock vectorstore for testing without embeddings
        self.vectorstore = MockVectorStore(docs)

    def retrieve(self, query, k=3):
        if self.vectorstore is None:
            self.build_vectorstore()
        docs = self.vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]

class MockVectorStore:
    def __init__(self, docs):
        self.docs = docs

    def similarity_search(self, query, k=3):
        # Simple mock: return first k docs
        return self.docs[:k]
