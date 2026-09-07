<<<<<<< HEAD
# 🚀 AI Startup Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14.2.3-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-FF6F61?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.4.1-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)

> An autonomous, multi-agent intelligence platform that conducts deep-web research, verifies cross-source data, predicts growth trajectories, formulates investment theses, and generates pixel-perfect PDF executive intelligence reports in real-time.

---

## 🌟 Key Features

| Feature Area | Capabilities & Description | Technical Implementation |
| :--- | :--- | :--- |
| **🤖 Autonomous Multi-Agent Orchestration** | 5 specialized AI agents run sequentially in a managed state graph to research, verify, analyze, report, and alert. | **LangGraph StateGraph**, **LangChain**, **ThreadPoolExecutor** |
| **🔍 Unified Deep Web Gathering** | Crawls web sources for funding history, hiring velocity, executive news, and social sentiment. | **Tavily AI Search API**, **Firecrawl Web Scraper** |
| **⚡ Real-Time WebSocket Streaming** | Streams agent progress, intermediate findings, and final reports live to the frontend dashboard. | **FastAPI WebSockets**, **Zustand State Management** |
| **📊 Growth Trajectory Meter** | Predicts startup performance and renders custom visual trajectory indicators (Low / Moderate / High Growth). | **Regex Sentiment Analyzer**, **ReportLab Vector Graphics** |
| **📑 Executive PDF Report Generator** | Generates professional, publication-ready PDF reports with dynamic headers, custom tables, and zero overlap. | **ReportLab Platypus**, `NumberedCanvas`, **UTF-8 Sanitizer** |
| **⚡ Modern Next.js UI Dashboard** | Interactive dark-mode dashboard with dynamic metric grids, news feeds, and live search tracking. | **Next.js 14 (App Router)**, **Recharts**, **Lucide React** |

---

## 🏗️ System Architecture & Workflow

### High-Level System Architecture

```mermaid
graph TD
    subgraph Client Layer ["🖥️ Frontend Dashboard (Next.js 14)"]
        UI["React User Interface"]
        WS_Client["WebSocket Consumer (Zustand)"]
        PDF_View["PDF Download Viewer"]
    end

    subgraph Backend Layer ["⚡ FastAPI Backend Server (Port 8000)"]
        Router["APIRouter (/api/v1/startups)"]
        WS_Server["WebSocket Manager (/ws/analysis)"]
        BgTasks["Async Background Task Runner"]
    end

    subgraph Agent Layer ["🤖 Autonomous Multi-Agent Pipeline (LangGraph)"]
        GA["1. Gathering Agent"]
        AA["2. Analysis & Verification Agent"]
        IA["3. Investment Insight Agent"]
        RA["4. PDF Report Agent"]
        AL["5. Real-Time Alert Agent"]
    end

    subgraph Data & Services ["🛠️ External Services & Storage"]
        Tavily["Tavily Search API"]
        LLM["OpenRouter / Grok / OpenAI"]
        ReportLab["ReportLab PDF Compiler"]
        PDF_Store["generated_reports/*.pdf"]
    end

    UI -->|POST /research| Router
    Router -->|Background Task| BgTasks
    BgTasks -->|Invoke State Graph| GA
    
    GA -->|Web Search| Tavily
    GA -->|Synthesize Intel| LLM
    GA -->|Partial Stream| WS_Server
    
    GA --> AA
    AA -->|Verify Data| LLM
    AA --> IA
    IA -->|Formulate Thesis| LLM
    IA --> RA
    
    RA -->|Compile Flowables| ReportLab
    ReportLab -->|Save Document| PDF_Store
    RA --> AL
    
    AL -->|Broadcast Stream| WS_Server
    WS_Server -->|Live JSON Updates| WS_Client
    WS_Client --> UI
    UI -->|Download PDF| PDF_View
```

---

## 🔄 Autonomous Multi-Agent Pipeline Flowchart

```mermaid
flowchart LR
    Start([User Initiates Research]) --> Node1

    subgraph Pipeline ["Autonomous Agent Pipeline"]
        Node1["🔍 Gathering Agent\n(Tavily Search & Scrape)"] -->|Extracted Data| Node2["🧠 Analysis Agent\n(Cross-Verification & Growth Meter)"]
        Node2 -->|Verified Intel| Node3["💡 Investment Insight Agent\n(Investment Thesis & Recommendations)"]
        Node3 -->|Structured Payload| Node4["📑 Report Agent\n(ReportLab PDF Generator)"]
        Node4 -->|PDF Path| Node5["🔔 Alert Agent\n(WebSocket Event Broadcast)"]
    end

    Node5 --> Finish([PDF Download & Interactive Insights Ready])

    style Node1 fill:#3b82f6,stroke:#1d4ed8,color:#fff
    style Node2 fill:#8b5cf6,stroke:#6d28d9,color:#fff
    style Node3 fill:#ec4899,stroke:#be185d,color:#fff
    style Node4 fill:#10b981,stroke:#047857,color:#fff
    style Node5 fill:#f59e0b,stroke:#b45309,color:#fff
```

---

## 🤖 Multi-Agent Roster Breakdown

| Agent Name | Primary Responsibility | Key Inputs | Tools & Services | Primary Output Payload |
| :--- | :--- | :--- | :--- | :--- |
| **🔍 Gathering Agent** | Unified deep-web search and multi-perspective data extraction. | `startup_name` | Tavily Search, Firecrawl Scraper, LLM | `research_data`, `funding_data`, `hiring_data`, `news_data`, `social_data` |
| **🧠 Analysis Agent** | Cross-verifies metrics, detects data discrepancies, and computes growth trajectory. | Extracted raw data dicts | Regex Sentiment Matcher, LLM | `verification_status`, `growth_prediction`, `is_verified` |
| **💡 Investment Insight Agent** | Evaluates risk profiles and formulates BUY / HOLD / AVOID investment recommendations. | Verified analysis & growth metrics | LLM Reasoning Engine | `investment_insights` (`recommendation`, `risk_analysis`) |
| **📑 PDF Report Agent** | Compiles structured state data into an aligned, publication-ready PDF document. | Complete `AgentState` | `ReportService` (ReportLab Engine) | `generated_reports/{startup}_{timestamp}.pdf` |
| **🔔 Alert Agent** | Dispatches real-time completion signals and metrics to connected UI clients. | Generated PDF path & report summary | FastAPI WebSocket Broadcast | JSON WebSocket Event Payload |

---

## 📡 API Endpoint Reference

### REST API Endpoints

| Method | Endpoint | Description | Request Body / Query | Response Payload |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/startups/research` | Triggers background multi-agent research workflow. | `{"startup_name": "OpenAI"}` | `{"status": "success", "message": "Agents dispatched..."}` |
| `GET` | `/api/v1/startups/{startup_name}/report/pdf` | Downloads the latest generated PDF intelligence report. | URL Path Parameter | `FileResponse` (`application/pdf`) |
| `GET` | `/` | Root API health & welcome endpoint. | None | `{"message": "Welcome to AI Startup Intelligence..."}` |

### WebSocket Gateway

| Channel | Gateway URI | Direction | Payload Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Live Analysis Stream** | `ws://localhost:8000/ws/analysis` | Server $\rightarrow$ Client | `JSON` | Real-time agent state broadcasts (`agent_start`, `agent_partial_result`, `analysis_complete`). |

---

## 📄 Executive PDF Report Features

The PDF reporting engine (`report_service.py`) is engineered using **ReportLab** with precision formatting:

| PDF Component | Architectural Enhancement | Visual Benefit |
| :--- | :--- | :--- |
| **Exact 504pt Grid Alignment** | Margins are set to `0.75 in` with all headers, tables, drawings, and cards locked to `504 pt` width. | 100% margin alignment with zero awkward whitespace gaps. |
| **Structured Table Cards** | Callout sections (Verification Status & Recommendation Box) are wrapped in single-cell `Table` flowables. | Eliminates background box overlap over section titles completely. |
| **Dynamic Growth Meter Graphic** | Rendered via ReportLab `Drawing` shapes, using regex word-boundary matching (`\bhigh\b` vs `\blow\b`). | Prevents false positives (e.g., `"highly competitive"` triggering green bar). |
| **Unicode Text Sanitization** | `clean_pdf_text()` pre-processor converts `₹` $\rightarrow$ `INR`, smart quotes $\rightarrow$ standard quotes, and removes invalid characters. | Eliminates black box (`■`) rendering artifacts in standard fonts. |
| **Dynamic Numbered Canvas** | Custom `NumberedCanvas` pass-through canvas calculates exact total pages dynamically. | Produces professional `"Page X of Y"` footers and running headers. |

---

## ⚙️ Environment Variables

Create a `.env` file in the project root directory:

| Variable Name | Purpose | Example / Default Value | Required? |
| :--- | :--- | :--- | :---: |
| `OPENROUTER_API_KEY` | LLM inference gateway for agent reasoning. | `sk-or-v1-...` | Yes |
| `TAVILY_API_KEY` | Deep-web research search engine API. | `tvly-...` | Yes |
| `GROK_API_KEY` | Optional alternative LLM provider API. | `xai-...` | Optional |
| `FIRECRAWL_API_KEY` | Web page scraping & parsing API key. | `fc-...` | Optional |
| `LANGCHAIN_TRACING_V2` | LangSmith observability tracing flag. | `true` | Optional |
| `LANGCHAIN_API_KEY` | LangSmith API key for telemetry. | `lsv2_pt_...` | Optional |

---

## 🛠️ Quick Start & Installation

### Option 1: Running Locally (Recommended)

#### Prerequisites
- **Python 3.11+**
- **Node.js 18+** & **npm**

#### 1. Clone & Setup Backend
```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate      # Windows (PowerShell)
# source venv/bin/activate   # macOS / Linux

# Install backend dependencies
pip install -r requirements.txt

# Start FastAPI development server
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

#### 2. Setup Frontend
```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install frontend dependencies
npm install

# Start Next.js development server
npm run dev
```

> 🌐 **Frontend Dashboard:** [http://localhost:3000](http://localhost:3000)  
> ⚡ **FastAPI Swagger API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Option 2: Running via Docker Compose

Run the full platform stack (Backend, Frontend, Redis) in containerized mode:

```bash
# Build and launch containers
docker-compose up --build
```

---

## 📁 Repository Directory Structure

```files.txt
task 1/
├── backend/
│   ├── agents/              # LangGraph multi-agent nodes & workflow definition
│   │   ├── nodes.py         # Agent node functions (Gathering, Analysis, Insight, Report, Alert)
│   │   ├── state.py         # TypedDict AgentState schema
│   │   └── workflow.py      # StateGraph compilation & edge routing
│   ├── api/                 # FastAPI API routes & WebSocket handlers
│   │   └── api_v1/          # Endpoint routers (/research, /report/pdf, /ws/analysis)
│   ├── core/                # System configuration & scheduler
│   ├── generated_reports/   # Target output folder for PDF executive reports
│   ├── services/            # Core business logic services
│   │   ├── llm_service.py   # LangChain LLM instance setup
│   │   ├── report_service.py# ReportLab PDF compilation & graphics engine
│   │   ├── scrape_service.py# Firecrawl web scraping integration
│   │   └── search_service.py# Tavily search API integration
│   ├── main.py              # FastAPI application entrypoint
│   └── requirements.txt     # Python backend dependencies
├── frontend/
│   ├── src/
│   │   └── app/             # Next.js 14 App Router pages & UI components
│   ├── package.json         # Node.js frontend dependencies
│   └── tailwind.config.js   # TailwindCSS styling configuration
├── docker-compose.yml       # Docker container orchestration manifest
└── README.md                # Project documentation & architecture manual
```

---

## 🛡️ License

This project is open-source under the [MIT License](LICENSE).
=======
# AI-Startup-Intelligence-Platform
An autonomous platform for startup discovery, data verification, intelligence analysis, growth trajectory prediction, and executive PDF reporting.
>>>>>>> d72dadf8b71406d34f2eb2725ca67595dff6be2d
