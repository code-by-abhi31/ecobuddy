# 🌱 EcoBuddy: Multi-Agent Sustainability & ROI Guide

EcoBuddy is an autonomous, stateful multi-agent system that analyzes the environmental impact of physical products and calculates the financial ROI of switching to sustainable alternatives. 

Unlike standard linear LLM wrappers, EcoBuddy uses a **Router Node (AI-as-a-Judge)** to dynamically control execution flow, preventing prompt injections and halting execution on invalid inputs to preserve compute.

## ⚙️ Architecture

Built entirely with open-source frameworks and local persistence:
*   **Orchestration:** LangGraph (StateGraph, Conditional Edges, TypedDict State)
*   **LLM Inference:** Groq (`compound-mini`) for high-throughput, low-latency agentic loops
*   **Frontend UI:** Streamlit 
*   **Agent Nodes:**
    *   `Router Node`: Gatekeeper that classifies input (Product vs. Invalid).
    *   `Impact Analyst`: Calculates carbon/material footprint.
    *   `Lifestyle Coach`: Generates practical, zero-waste alternatives.
    *   `ROI Analyst`: Calculates localized 1-year financial savings in INR.

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/code-by-abhi31/ecobuddy.git](https://github.com/code-by-abhi31/ecobuddy.git)
   cd ecobuddy