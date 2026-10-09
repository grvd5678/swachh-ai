# ♻️ Swachh.ai

<div align="center">

### **Know your waste. Know what to do.**

*A location-aware, regulation-grounded waste-disposal decision assistant for Indian households.*

[![Track](https://img.shields.io/badge/Track-03%20Waste%20%26%20Energy-emerald?style=for-the-badge)](https://www.wemakedevs.org/aws/env)
[![AWS](https://img.shields.io/badge/AWS-ECS%20Fargate%20%7C%20S3%20%7C%20CloudWatch-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com)
[![Next.js](https://img.shields.io/badge/Next.js-16%20App%20Router-black?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Python%203.12-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Gemini](https://img.shields.io/badge/Google-Gemini%20AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)

**Built solo by [Gourav Das (@grvd5678)](https://github.com/grvd5678) for the WeMakeDevs AWS Environmental Hackathon**

[Live Backend API](http://54.89.84.114:8000/docs) • [API Health Check](http://54.89.84.114:8000/api/health) • [Demo Video / Pitch](DEMO_SCRIPT.md)

</div>

---

## 📌 The Real Problem

Ordinary citizens generally know where a plastic bottle or food peel goes. But difficult, hazardous household waste creates confusion:

- 🔋 **Swollen Power Banks & Lithium Batteries:** Crushed in garbage trucks → **severe compaction fires**.
- 💡 **Fused CFL Bulbs & Tube Lights:** Smashed in municipal carts → **toxic mercury vapor release**.
- 💊 **Expired Medicines & Syrups:** Flushed down toilets/sinks → **water table contamination & antibiotic resistance**.
- 🔌 **Broken Chargers & Cables:** Burned in scrap yards → **toxic dioxin emissions**.

Generic AI chatbots fail here: they generate long Wikipedia-style summaries explaining *what* an item is, but they don't give the citizen a safe, local, and legally grounded decision.

> **Our Core Philosophy:**  
> **Swachh.ai doesn't just tell citizens what their waste is. It tells them what to do with it.**

---

## 💡 What Swachh.ai Does

Swachh.ai is **not a generic chatbot**. It is an action-oriented decision assistant:

$$\text{User Waste Description} + \text{Citizen Location} \xrightarrow{\text{RAG + Gemini}} \text{Actionable Disposal Plan}$$

### 🎯 Sample Output Card
```
┌────────────────────────────────────────────────────────────────────────┐
│ 🔋 POWER BANK                                   🟢 High Confidence     │
│ Category: E-waste / Portable Lithium-ion Battery                       │
│                                                                        │
│ ➡️ WHAT TO DO                                                          │
│ Keep completely separate from household garbage. Do not puncture,     │
│ crush, or expose to heat. Tape terminals with electrical tape.         │
│                                                                        │
│ 📍 LOCAL DISPOSAL PATHWAY                                              │
│ Surrender to authorized EPR battery collection points, retail brand    │
│ take-back drives, or Kolkata designated municipal e-waste drop-offs.   │
│                                                                        │
│ ⚠️ WHY IT MATTERS                                                      │
│ Lithium-ion cells pose severe thermal runaway & fire risks in trucks.  │
│                                                                        │
│ 📜 OFFICIAL SOURCE                                                     │
│ Battery Waste Management Rules, 2022 (MoEFCC Notification G.S.R. 664(E))│
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Architecture & Data Pipeline

```
                       ♻️ SWACHH.AI ARCHITECTURE

                               CITIZEN
                                  │
                 "Power bank + CFL bulb + paracetamol"
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   Next.js 16 UI  │ (Vercel / Tailwind CSS)
                         └────────┬─────────┘
                                  │ HTTPS
                                  ▼
                         ┌──────────────────┐
                         │   FastAPI API    │ (AWS ECS + Fargate)
                         └────────┬─────────┘
                                  │
                   ┌──────────────┴──────────────┐
                   ▼                             ▼
            Item Extraction                Citizen Location
                   │                             │
                   └──────────────┬──────────────┘
                                  ▼
                         ┌──────────────────┐
                         │  ChromaDB (RAG)  │ (all-MiniLM-L6-v2 Embeddings)
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
                         ┌──────────────────┐
                         │  Google Gemini   │ (Strict Pydantic JSON Schema)
                         └────────┬─────────┘
                                  │
                                  ▼
                         ♻️ YOUR DISPOSAL PLAN
                                  │
             ┌────────────────────┼────────────────────┐
             ▼                    ▼                    ▼
         CATEGORY            WHAT TO DO               WHY
      (Classification)    (Direct Action)      (Hazard Rationale)
```

---

## 📚 Authoritative Knowledge Base (No Hallucinations)

Swachh.ai grounds its answers exclusively in curated, substantive Indian environmental legal frameworks stored in [`data/knowledge_base/`](data/knowledge_base/):

| # | Regulation | Governing Authority | Focus Area |
|---|---|---|---|
| 1 | **Solid Waste Management Rules, 2016** | MoEFCC / CPCB | Rule 3(1)(17) Domestic Hazardous Waste definitions & Rule 4 generator duties |
| 2 | **Battery Waste Management Rules, 2022** | MoEFCC Notification G.S.R. 664(E) | Portable batteries, power banks, fire safety, and EPR collection drop-offs |
| 3 | **E-Waste (Management) Rules, 2022** | MoEFCC Notification G.S.R. 801(E) | IT accessories, mobile chargers, cables, and authorized dismantler channels |
| 4 | **Kolkata Municipal Corporation (KMC) Bye-laws** | KMC & WBPCB | Ward doorstep green/white/black bin segregation and local compactor drop-off |

---

## 🛡️ 3-Tier Reliability Engine (Never Crashes)

In an environmental product, safety and accuracy are non-negotiable. Swachh.ai implements a 3-tier fallback hierarchy:

1. **Tier 1 (Primary AI):** Google Gemini (`gemini-3.5-flash-lite` / `gemini-3.8-flash`) generating typed Pydantic structured JSON.
2. **Tier 2 (AI Retry with Backoff):** Exponential backoff handling on transient 503 or quota limits.
3. **Tier 3 (Deterministic Rule Engine):** If all LLM APIs are unreachable, the system automatically synthesizes a grounded disposal decision directly from the top retrieved ChromaDB regulatory chunks.
4. **Honest Confidence Scoring:** Decisions clearly display **🟢 High Confidence**, **🟡 Limited Evidence**, or **🔴 Unsupported / Advisory** (telling the citizen what *not* to throw away).

---

## ☁️ AWS Cloud Architecture

Built strictly following AWS best practices for serverless, cost-effective workloads with **zero idle EC2 servers**:

- **Amazon S3:** Durable object repository for authoritative government gazette documents and markdown knowledge source files.
- **Amazon ECR:** Private container registry hosting the production backend container image.
- **Amazon ECS + AWS Fargate:** Serverless container execution hosting the live FastAPI API (`http://54.89.84.114:8000`), automatically scaling and running without virtual machine overhead.
- **Amazon CloudWatch:** Centralized container logs, query latencies, and audit trails.

---

## 💻 Tech Stack

| Component | Technology | Purpose |
|---|---|---|
| **Frontend** | Next.js 16 (App Router), TypeScript, Tailwind CSS | High-contrast, responsive dark UI with 1-click hackathon demo presets |
| **Icons** | Lucide React | Visual waste item categorisation and status badges |
| **Backend** | FastAPI (Python 3.12), Pydantic v2 | High-performance asynchronous REST API with typed schema validation |
| **Vector DB** | ChromaDB (Local persistent) | In-container vector retrieval using `all-MiniLM-L6-v2` ONNX embeddings |
| **Cloud** | AWS ECS, Fargate, ECR, S3, CloudWatch | Serverless container compute and durable document storage |
| **Container** | Docker (`python:3.12-slim`) | Pre-bakes knowledge base ingestion during build for instant container boot |

---

## ⚡ Running Locally

### 1. Prerequisites
- Python 3.12+
- Node.js 18+

### 2. Backend Setup
```powershell
# 1. Activate virtual environment
.\.venv\Scripts\activate

# 2. Run local API server
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
*API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)*

### 3. Frontend Setup
```powershell
cd frontend
npm.cmd run dev
```
*Web App: [http://localhost:3000](http://localhost:3000)*

### 4. Vector Store Re-ingestion & Tests
```powershell
# Ingest regulations into ChromaDB
.\.venv\Scripts\python.exe backend\ingest.py

# Run retrieval benchmark tests
.\.venv\Scripts\python.exe backend\test_retrieval.py
```

---

## 📽️ Hackathon Demo

- **Pitch Script & Timing:** See [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md) for the exact 3-minute video presentation flow:
  1. **0:00 – 0:40:** The Problem (The hazardous household waste dilemma)
  2. **0:40 – 1:50:** Live Working Product Walkthrough
  3. **1:50 – 2:35:** Architecture & AWS Cloud Story
  4. **2:35 – 3:00:** Impact & Real-World Waste Segregation

---

<div align="center">

**Developed with ❤️ by Gourav Das for WeMakeDevs AWS Environmental Hacks (Track 03)**  
*Know your waste. Know what to do.*

</div>
