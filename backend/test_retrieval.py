import sys
from pathlib import Path
import chromadb

# Ensure UTF-8 output in Windows terminals
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = DATA_DIR / "chroma_db"

def test_query(query_text: str, location_hint: str = "kolkata", n_results: int = 3):
    print("\n" + "=" * 70)
    print(f"🔍 QUERY: '{query_text}' | Location context: '{location_hint}'")
    print("=" * 70)

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_collection(name="waste_guidance")

    # Perform query
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0] if "distances" in results and results["distances"] else [None] * len(documents)

    for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances), start=1):
        dist_str = f"{dist:.4f}" if dist is not None else "N/A"
        print(f"\n[Result {i}] Distance: {dist_str}")
        print(f"  • Source: {meta.get('doc_title')}")
        print(f"  • Jurisdiction: {meta.get('jurisdiction')} | Tags: {meta.get('waste_tags')}")
        print(f"  • Section: {meta.get('header')}")
        print("  • Snippet Preview:")
        # Print first 250 characters of doc
        snippet = doc.strip().replace("\n", " ")
        if len(snippet) > 250:
            snippet = snippet[:250] + "..."
        print(f"    \"{snippet}\"")

def run_all_tests():
    test_cases = [
        ("I have a broken swollen power bank", "kolkata"),
        ("expired paracetamol and cough syrup bottles", "kolkata"),
        ("fused CFL tube light with mercury", "kolkata"),
        ("old phone charger with damaged copper wire", "kolkata"),
        ("leftover vegetable peels and kitchen food waste", "kolkata")
    ]

    for item, loc in test_cases:
        test_query(item, loc)

if __name__ == "__main__":
    run_all_tests()

