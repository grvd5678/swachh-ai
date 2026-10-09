from pathlib import Path
from typing import List, Dict, Any
import chromadb

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = DATA_DIR / "chroma_db"

class RAGService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        self.collection = self.client.get_collection(name="waste_guidance")

    def retrieve_guidance(self, query: str, location: str = "Kolkata", n_results: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve authoritative chunks from ChromaDB for a given item query.
        Prioritizes local jurisdiction chunks when location matches knowledge base.
        """
        location_lower = location.lower()
        is_kolkata = any(k in location_lower for k in ["kolkata", "west bengal", "kmc"])

        # If location matches Kolkata, fetch extra results and re-rank local chunks first
        fetch_n = n_results + 3 if is_kolkata else n_results
        results = self.collection.query(
            query_texts=[query],
            n_results=fetch_n
        )

        matched_chunks = []
        if not results or not results["documents"] or not results["documents"][0]:
            return matched_chunks

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0] if "distances" in results and results["distances"] else [None] * len(documents)

        for doc, meta, dist in zip(documents, metadatas, distances):
            matched_chunks.append({
                "content": doc,
                "jurisdiction": meta.get("jurisdiction", "national"),
                "doc_title": meta.get("doc_title", ""),
                "source_citation": meta.get("source_citation", ""),
                "header": meta.get("header", ""),
                "waste_tags": meta.get("waste_tags", ""),
                "distance": dist
            })

        # Re-rank: only promote local chunks that are relevance-competitive
        # (within 0.15 distance of the best national chunk — prevents broad KMC
        # chunks from burying a highly relevant national pharmaceutical/battery rule)
        if is_kolkata:
            national = [c for c in matched_chunks if c["jurisdiction"] != "kolkata"]
            local = [c for c in matched_chunks if c["jurisdiction"] == "kolkata"]
            best_national_dist = national[0]["distance"] if national and national[0]["distance"] is not None else float("inf")
            competitive_local = [c for c in local if c["distance"] is not None and c["distance"] <= best_national_dist + 0.15]
            weak_local = [c for c in local if c not in competitive_local]
            matched_chunks = (competitive_local + national + weak_local)[:n_results]

        return matched_chunks

    def format_context_for_prompt(self, chunks: List[Dict[str, Any]]) -> str:
        """Format retrieved chunks into a clean, cited context string for Gemini."""
        if not chunks:
            return "No specific authoritative guidelines found in knowledge base."

        formatted = []
        for i, c in enumerate(chunks, 1):
            formatted.append(
                f"[Source {i}: {c['doc_title']} ({c['jurisdiction'].upper()}) - {c['source_citation']}]\n"
                f"Section: {c['header']}\n"
                f"Content:\n{c['content'].strip()}\n"
            )
        return "\n---\n".join(formatted)

# Global singleton
rag_service = RAGService()

