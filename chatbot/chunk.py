class Chunk:

    def __init__(self, chunk_doc) -> None:
        self.content = chunk_doc.get("content")
        self.metadata = chunk_doc.get("metadata")
        self.embedding = chunk_doc.get("embedding")

    def set_embedding(self, embedding):
        self.embedding = embedding

    def to_json(self):
        return { "content" : self.content, "metadata" : self.metadata, "embedding" : self.embedding }
