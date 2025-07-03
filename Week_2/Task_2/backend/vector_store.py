import os

from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_openai import ChatOpenAI


class VectorStore:

    def __init__(
        self,
        data_dir: str = "data/vector_store",
        embedding_model: str = "text-embedding-3-small",
    ):
        os.makedirs(data_dir, exist_ok=True)
        self.data_dir = data_dir
        self.embeddings = OpenAIEmbeddings(model=embedding_model)

    def _load(self) -> FAISS:
        """
        Load the FAISS vector index from local storage.

        Returns:
            FAISS: Loaded FAISS vectorstore instance or None if not found.
        """
        if os.path.exists(self.data_dir):
            return FAISS.load_local(
                self.data_dir, self.embeddings, allow_dangerous_deserialization=True
            )

    def _split_docs(self, docs: list[Document]) -> list[Document]:
        """
        Split documents into chunks suitable for embedding.

        Args:
            docs (List[Document]): List of loaded documents.

        Returns:
            List[Document]: List of chunked documents.
        """
        splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        return splitter.split_documents(docs)

    def index_file(self, file_path: str) -> None:
        """
        Load and index documents from a file, then save to local FAISS index.

        Args:
            file_path (str): Path to the document file.
        """
        docs = TextLoader(file_path, encoding="utf-8").load()
        chunks = self._split_docs(docs)
        index_path = os.path.join(self.data_dir, "index.faiss")
        if os.path.exists(index_path):
            vectorstore = self._load()
            vectorstore.add_documents(chunks)
        else:
            vectorstore = FAISS.from_documents(chunks, self.embeddings)

        vectorstore.save_local(str(self.data_dir))

    def get_chain(self, api_key: str, model_name: str = "gpt-4o") -> RetrievalQA:
        """
        Create a RetrievalQA chain using the loaded vectorstore and an OpenAI LLM.

        Args:
            api_key (str): OpenAI API key.
            model_name (str, optional): Language model name.

        Returns:
            RetrievalQA: Initialized RetrievalQA chain.
        """
        llm = ChatOpenAI(api_key=api_key, model=model_name)
        retriever = self._load().as_retriever(search_kwargs={"k": 3})
        return RetrievalQA.from_llm(llm=llm, retriever=retriever)

    def search(self, query: str, api_key: str) -> str:
        """
        Perform a query search against the vectorstore using RetrievalQA chain.

        Args:
            query (str): The search query string.
            api_key (str): OpenAI API key.

        Returns:
            str: The search result.
        """
        chain = self.get_chain(api_key=api_key)
        result = chain.invoke({"query": query})
        return result["result"]
