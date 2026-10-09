import os
import re
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
KB_DIR = DATA_DIR / "knowledge_base"
CHROMA_DIR = DATA_DIR / "chroma_db"

def extract_metadata_from_file(filename: str, content: str):
    """Infer document-level metadata from headers and filename."""
    jurisdiction = "kolkata" if "kolkata" in filename else "national"
    
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    doc_title = title_match.group(1).strip() if title_match else filename
    
    source_match = re.search(r"\*\*Source:\*\*\s*(.+)$", content, re.MULTILINE)
    source_citation = source_match.group(1).strip() if source_match else "Official Regulations"

    return jurisdiction, doc_title, source_citation

def chunk_markdown_document(content: str):
    """
    Split markdown document into logical sections based on ##, ### or #### headers.
    """
    sections = re.split(r"\n(?=#{2,4}\s+)", content)
    chunks = []
    for sec in sections:
        sec = sec.strip()
        if not sec:
            continue
        # Extract section heading
        header_match = re.match(r"^(#{2,4}\s+.+)", sec)
        header = header_match.group(1).replace("#", "").strip() if header_match else "General"
        chunks.append({
            "header": header,
            "text": sec
        })
    return chunks

def tag_waste_types(text: str) -> str:
    """Identify relevant waste type keywords in chunk."""
    text_lower = text.lower()
    tags = []
    if any(k in text_lower for k in ["battery", "power bank", "lithium-ion", "cell"]):
        tags.append("battery")
    if any(k in text_lower for k in ["e-waste", "electronic", "charger", "cable", "phone", "it equipment"]):
        tags.append("e-waste")
    if any(k in text_lower for k in ["cfl", "fluorescent", "lamp", "mercury", "tube"]):
        tags.append("cfl_mercury")
    if any(k in text_lower for k in ["medicine", "pharmaceutical", "syrup", "tablet", "ointment"]):
        tags.append("pharmaceutical")
    if any(k in text_lower for k in ["hazardous", "paint", "chemical", "pesticide"]):
        tags.append("chemical_hazardous")
    if any(k in text_lower for k in ["wet waste", "dry waste", "biodegradable", "segregation", "bin"]):
        tags.append("general_solid_waste")
    return ",".join(tags) if tags else "general"

def ingest():
    print(f"Loading knowledge base from: {KB_DIR}")
    if not KB_DIR.exists():
        raise FileNotFoundError(f"Directory not found: {KB_DIR}")

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    
    # Using Chroma's default sentence-transformer embedding function (all-MiniLM-L6-v2)
    collection = client.get_or_create_collection(
        name="waste_guidance",
        metadata={"description": "Authoritative Indian National and Local Waste Management Guidance"}
    )

    # Clear existing to avoid duplicates on re-ingestion
    existing_count = collection.count()
    if existing_count > 0:
        print(f"Cleaning previous {existing_count} records from collection...")
        all_ids = collection.get()["ids"]
        if all_ids:
            collection.delete(ids=all_ids)

    doc_ids = []
    documents = []
    metadatas = []

    files = sorted(list(KB_DIR.glob("*.md")))
    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        jurisdiction, doc_title, source_citation = extract_metadata_from_file(file_path.name, content)
        chunks = chunk_markdown_document(content)

        print(f"Processing '{file_path.name}': {len(chunks)} chunks found.")

        for idx, chunk in enumerate(chunks):
            chunk_id = f"{file_path.stem}_chunk_{idx}"
            waste_tags = tag_waste_types(chunk["text"])
            
            doc_ids.append(chunk_id)
            documents.append(chunk["text"])
            metadatas.append({
                "source_file": file_path.name,
                "jurisdiction": jurisdiction,
                "doc_title": doc_title,
                "source_citation": source_citation,
                "header": chunk["header"],
                "waste_tags": waste_tags
            })

    print(f"\nIngesting {len(documents)} chunks into ChromaDB...")
    collection.add(
        ids=doc_ids,
        documents=documents,
        metadatas=metadatas
    )

    print(f"SUCCESS: Ingested {collection.count()} chunks into ChromaDB at {CHROMA_DIR}!")

if __name__ == "__main__":
    ingest()

