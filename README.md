# Yeshwanth Atmakuri

**AI Engineer | Software Developer**

I build AI-powered software, from research prototypes to production services. My work spans knowledge-graph retrieval, real-time voice AI, autonomous agents, and the backend services and web interfaces around them.

- **Currently:** AI Automation R&D Intern at Advfiction, designing workflow automation for a multi-sector Business OS.
- **Recognition:** Two-time Smart India Hackathon internal qualifier (2025 and 2026), selected among the top 45 of 300+ team entries.

[Portfolio](https://yesh-eosin.vercel.app/) | [LinkedIn](https://www.linkedin.com/in/yesh26/) | [Email](mailto:atmakuriyeshwanth@gmail.com)

## Journey

| When | Role | What I did |
|---|---|---|
| Aug 2026 to Present | **AI Automation R&D Intern**, Advfiction (remote) | Designing automation workflows for a multi-sector Business OS that connects CRM, ERP, AI and external services. Evaluated n8n, Zoho Flow, Zapier and Workato for webhooks, scheduled jobs, conditional logic, retries and error handling. |
| May to Jul 2026 | **Research Intern**, Cyber Threat Intelligence | Built a GraphRAG framework (ChromaDB, SentenceTransformers, Neo4j) that converts unstructured threat reports into MITRE ATT&CK knowledge graphs for next-technique prediction. Optimized a RotatE embedding model in PyTorch that outperformed GNN, LLM and Markov-chain baselines. |
| Mar to Aug 2026 | **Exchange Student**, Universiti Teknologi Malaysia | Semester exchange program in Johor Bahru, Malaysia. |
| Jan to Mar 2026 | **AI Engineering Intern**, Simsy AI (remote) | Deployed production-ready voice AI pipeline components (Python, FastAPI, Docker, LightRAG, LiveKit) and cut audio payload latency by 32% on AWS. Optimized the asynchronous backend and REST API architecture to support more parallel users, and reduced container baseline storage by 45%. |
| Ongoing | **Member**, McCarthy Lab, Next Tech Lab | Active member of a student mentorship lab, collaborating on AI projects. |

## Projects

### [Next-TTP-Prediction](https://github.com/YEsh-DEV/Next-TTP-Prediction)

A temporal-causal GraphRAG system that predicts the next technique an attacker group is likely to use, based on actor-aware knowledge graphs and RotatE embeddings.

- **Result:** 41.38% Hits@1
- **Stack:** Python, PyTorch, PyKEEN, Neo4j, ChromaDB

### [Nexi](https://github.com/YEsh-DEV/nexi-ntl): AI Voice Assistant

A voice assistant that routes each question between campus PDFs and structured JSON data, with persistent conversation memory and RAG-based grounding to reduce hallucinations.

- **Result:** 340 ms response latency and 98.4% grounded response accuracy
- **Stack:** Python, LlamaIndex, ChromaDB, LiveKit, Gemini

### [Palm Vein Biometric Payment System](https://github.com/YEsh-DEV/vein-detection)

An edge-based payment authentication system running on a Raspberry Pi 5. It uses near-infrared imaging, MediaPipe hand landmarks, Gabor wavelet VeinCode generation and parallel matching, with a FastAPI backend and a React app for enrollment, scanning and payment authorization. VeinCodes are stored encrypted.

- **Result:** Under 500 ms authentication and a false acceptance rate below 0.1%
- **Stack:** Python, MediaPipe, OpenCV, FastAPI, React, SQLite, Raspberry Pi 5

### [Autonomous Recovery Agent](https://github.com/YEsh-DEV/Autonomous-Recovery-Agent)

A LangGraph agent that parses payment failures, classifies the root cause and sends personalized retry links, reducing manual intervention. Event-driven FastAPI webhooks let it run as middleware inside existing payment backends without changing client infrastructure.

- **Stack:** Python, LangGraph, FastAPI, SQLite

## Tech Stack

<p align="center">
<img src="assets/armory.svg" alt="Tech stack by category. Languages: Python, C++, Java. Frontend: HTML, CSS, JavaScript, TypeScript, React. Backend: FastAPI, SQLAlchemy, LiveKit, REST API, Webhooks. AI and ML: PyTorch, TensorFlow, scikit-learn, XGBoost, OpenCV, MediaPipe, LangChain, LangGraph, LlamaIndex, CrewAI, Advanced RAG. Cloud and deployment: Docker, AWS, GitHub Actions, Vercel, Git. Databases: Neo4j, ChromaDB, Qdrant, PostgreSQL, SQLite." width="640">
</p>
<p align="center"><sub>Gold marks the tools I use most.</sub></p>
