# ♻️ Swachh.ai

> **Know your waste. Know what to do.**  
> *Track 03: Waste & Energy — WeMakeDevs AWS Hackathon*  
> **Solo Developer:** Gourav Das ([@grvd5678](https://github.com/grvd5678))

Swachh.ai is a location-aware AI waste-disposal decision assistant. Unlike generic chatbots that merely explain what waste is, Swachh.ai identifies complex items, retrieves authoritative environmental regulations via RAG (Retrieval-Augmented Generation), and produces a structured, actionable disposal plan.

---

## 🏗️ Architecture

```
                       ♻️ SWACHH.AI

                           CITIZEN
                              │
             "Power bank + CFL bulb + medicine"
                              │
                              ▼
                     ┌──────────────────┐
                     │  Next.js 16 UI   │ (Tailwind CSS, TypeScript)
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │   FastAPI API    │
                     └────────┬─────────┘
                              │
               ┌──────────────┴──────────────┐
               ▼                             ▼
        Waste Item Parsing             User Location
               │                             │
               └──────────────┬──────────────┘
                              ▼
                     ┌──────────────────┐
                     │  RAG Retrieval   │ (ChromaDB + all-MiniLM-L6-v2)
                     └────────┬─────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
          National Rules               Local Bye-laws
          - SWM Rules 2016             - KMC 3-Bin Rules
          - Battery Rules 2022         - Ward Drop-off points
          - E-Waste Rules 2022
                │                           │
                └─────────────┬─────────────┘
                              ▼
                     ┌──────────────────────────┐
                     │  Google Gemini           │
                     │  Primary:  gemini-3.5-flash-lite │
                     │  Fallback: gemini-3.8-flash      │
                     └────────┬─────────────────┘
                              │
                              ▼
                     ♻️ DISPOSAL PLAN
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
     CATEGORY            WHAT TO DO               WHY
  (Classification)    (Direct Action)      (Hazard Rationale)
```

---

## ⚡ Quick Start

### 1. Backend (FastAPI + ChromaDB)

```powershell
# Activate Python virtual environment
.\.venv\Scripts\activate

# Add your Gemini API Key in .env
# Copy template: copy .env.example .env
# GEMINI_API_KEY=your_key_here

# Run the FastAPI server
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
API docs available at: `http://localhost:8000/docs`

### 2. Frontend (Next.js)

```powershell
cd frontend
npm.cmd run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🧪 Knowledge Base & RAG Ingestion

The authoritative knowledge base lives in `data/knowledge_base/`:
- `01_solid_waste_management_rules_2016.md` (Domestic Hazardous Waste, generator duties)
- `02_battery_waste_management_rules_2022.md` (Portable batteries, power banks, EPR rules)
- `03_e_waste_management_rules_2022.md` (Consumer electronics, chargers, dismantler pathways)
- `04_kolkata_kmc_waste_guidelines.md` (Kolkata Municipal Corporation green/white/black bin bye-laws)

To re-ingest or verify retrieval quality:
```powershell
.\.venv\Scripts\python.exe backend\ingest.py
.\.venv\Scripts\python.exe backend\test_retrieval.py
```

---

## ☁️ AWS Deployment (Live)

The backend is deployed on AWS and running in production:

- **Amazon S3**: Authoritative repository for regulatory documents and knowledge base files.
- **Amazon ECS + AWS Fargate**: Serverless container execution for FastAPI backend — no idle EC2, automated scaling.
- **Amazon CloudWatch**: Container logs, query metrics, and audit tracing.
- **No Idle EC2**: Zero EC2 server maintenance or idle costs.

Live API: `http://54.89.84.114:8000` — Health check: `http://54.89.84.114:8000/api/health`  
> Note: Fargate assigns a new public IP on each task restart. Update `frontend/.env.local` with the new IP if redeployed.

---

## 🤖 AI Model

- **Primary**: `gemini-3.5-flash-lite` (Google Gemini) — fast, reliable, optimized for structured JSON output
- **Fallback**: `gemini-3.8-flash` — higher quality, used automatically if primary is unavailable
- **Retry logic**: Exponential backoff on 503 before falling back
- **Grounded fallback**: Deterministic rule-based engine using ChromaDB top chunks if all LLM calls fail
