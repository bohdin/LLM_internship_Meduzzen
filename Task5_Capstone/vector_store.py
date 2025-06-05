from openai import AsyncOpenAI
import faiss
import numpy as np
import os
import json

class VectorStore():

    def __init__(self, index_path: str = "data/vectors.faiss", kb_path: str = "data/kb.json"):
        self.dimension = 1536
        self.index_path = index_path
        self.kb_path = kb_path
        self.index = faiss.IndexFlatIP(self.dimension)
        self.kb = {}
        self.next_id = 0

        self._load()
        

    def _load(self):
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)

        if os.path.exists(self.kb_path):
            with open(self.kb_path, "r") as f:
                self.kb = json.load(f)
                self.next_id = max([int(k) for k in self.kb.keys()], default=-1) + 1


    def save(self):
        faiss.write_index(self.index, self.index_path)

        with open(self.kb_path, "w") as f:
            json.dump(self.kb, f, indent=2)


    async def _get_embeddings(self, client: AsyncOpenAI, text: str) -> np.ndarray:
        """
        Generate normalized embedding vector from input text

        Args:
            client (OpenAI): An initialized OpenAI client
            text (str): Text to embed

        Returns:
            np.ndarray: A normalized NumPy array of text embedding
        """
        response = await client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )

        vector = np.array(response.data[0].embedding)

        cosine_vector = vector / np.linalg.norm(vector)

        return np.expand_dims(cosine_vector, axis=0)


    async def add_text(self, client: AsyncOpenAI, text: str, id: int = None) -> None:
        embedding = await self._get_embeddings(client, text)

        assigned_id = id or self.next_id
        self.kb[assigned_id] = text
        self.index.add(embedding)

        if id is None:
            self.next_id += 1


    async def search(self, client: AsyncOpenAI, query: str, top_k: int = 3) -> list[tuple[int, str]]:
        query_embedding = await self._get_embeddings(client, query)

        results = self.index.search(query_embedding, top_k)

        return [ (idx, self.get_by_id(idx)) for idx in results[1][0] if idx in self.kb.keys()]
    
    async def get_by_id(self, index: int):
        return self.kb.get(index)