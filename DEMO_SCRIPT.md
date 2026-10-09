# ⏱️ 3-Minute Hackathon Demo Script: Swachh.ai

**Track:** Track 03 — Waste & Energy  
**Speaker:** Gourav Das ([@grvd5678](https://github.com/grvd5678))  
**Target Duration:** Exactly 3:00 minutes  
**Storytelling Flow:** Problem → Solution → Live Working Demo → Architecture & AWS → Impact

---

## 🎬 0:00 – 0:40 | The Hook & The Problem
*(Screen: Camera on you or opening slide showing Swachh.ai logo)*

> "Hi everyone, I'm Gourav Das. 
> 
> Most of us know where a plastic bottle or leftover food goes. 
> But what happens when you have a **swollen power bank, a broken CFL bulb, and expired medicine** sitting in your drawer?
> 
> Right now, people hesitate. And worse—many throw them into the ordinary municipal dustbin. 
> Compacted lithium batteries cause dangerous truck fires. Broken CFLs release neurotoxic mercury vapor. Expired antibiotics flush into our water supply.
> 
> Existing AI tools don't solve this. If you ask a generic chatbot, it gives you a Wikipedia essay explaining what a battery is. 
> 
> But citizens don't need an essay. They need a decision. 
> **Swachh.ai doesn't just tell people what their waste is. It tells them what to do with it.**"

---

## 💻 0:40 – 1:50 | Live Product Walkthrough
*(Screen: Switch to `http://localhost:3000`)*

> "Let's see Swachh.ai in action.
> 
> Here is our interface—clean, fast, and built specifically for ordinary citizens.
> 
> I'll enter our exact problem: 
> *'I have a broken swollen power bank, an old CFL bulb, and some expired paracetamol tablets.'*
> 
> And our location: **Kolkata, West Bengal**.
> 
> Now, I click **Get My Disposal Plan**."

*(Click button — wait 1-2 seconds for cards to render)*

> "Instantly, Swachh.ai produces an itemized, location-aware disposal plan:
> 
> 1. **Broken Power Bank:** It detects it as a *Portable Lithium-ion Battery*. Instead of saying 'recycle it', it gives an urgent, actionable instruction: *'Keep completely separate from household garbage. Do not puncture or crush.'* And points to the Kolkata EPR battery drop-off pathway.
> 2. **Old CFL Bulb:** Classified as *Domestic Hazardous Waste*. It warns about mercury vapor and instructs the citizen to wrap it intact and hand it over to the KMC conservancy worker in a separate black bag.
> 3. **Expired Paracetamol:** Classified under *Pharmaceutical Domestic Hazardous Waste*, with a clear safety rule: *'Never flush down drains to prevent water contamination.'*
> 
> Notice every card has three crucial elements:
> - **WHAT TO DO** (Direct action)
> - **LOCAL DISPOSAL PATHWAY** (Location-specific)
> - **WHY** (Hazard & environmental rationale)
> - **LEGAL SOURCE CITATION** grounded in official CPCB regulations."

---

## ☁️ 1:50 – 2:35 | Architecture & AWS Story
*(Screen: Show the Architecture diagram from `README.md` or the bottom section of the homepage)*

> "How does this work under the hood?
> 
> We specifically did NOT build an ungrounded ChatGPT wrapper. Swachh.ai uses a **Retrieval-Augmented Generation (RAG)** pipeline:
> 
> 1. **Knowledge Base:** We ingested official regulatory documents:
>    - MoEFCC Solid Waste Management Rules 2016
>    - Battery Waste Management Rules 2022
>    - E-Waste Management Rules 2022
>    - Kolkata Municipal Corporation bye-laws
> 2. **ChromaDB Vector Store:** Chunks and indexes these regulations with metadata filtering for local vs. national jurisdiction.
> 3. **Google Gemini LLM:** Uses structured Pydantic schemas to generate typed, hallucination-free decisions.
> 
> **Our AWS Cloud Strategy:**
> - **Amazon S3:** Serves as our authoritative document repository where official government regulations are securely stored.
> - **Amazon ECS Express Mode + AWS Fargate:** Runs our containerized FastAPI backend on serverless Fargate compute with automated HTTPS routing and zero idle EC2 instances.
> - **Amazon CloudWatch:** Monitors backend queries, RAG retrieval latencies, and system audit logs."

---

## 🌍 2:35 – 3:00 | Impact & Closing
*(Screen: Back to Swachh.ai results card / your camera)*

> "By answering *'What should I DO?'* rather than *'What is this?'*, Swachh.ai bridges the gap between complex environmental regulations and daily citizen actions.
> 
> It prevents fires, keeps neurotoxins out of landfills, and makes waste segregation intuitive for millions of households.
> 
> **Swachh.ai: Know your waste. Know what to do.**
> 
> Thank you!"

---

### 💡 Tips for Recording Your Demo Video:
1. **Pacing:** Speak clearly and don't rush. The script is timed for a calm 130–140 words per minute.
2. **Preset Button:** Use the built-in preset button (`🔋 Power bank + 💡 CFL + 💊 Medicine`) so you don't waste seconds typing manually.
3. **Show the Citation:** Zoom in briefly or hover over the official CPCB / SWM 2016 legal citation on the card—judges love seeing that level of regulatory grounding!

