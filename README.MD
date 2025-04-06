# 🇮🇳 भारतKredit (BharatKredit) – AI-Powered Agricultural Loan System

> **"Empowering farmers with automated, risk-aware, and multilingual loan approvals."**

---

## 🚩 Problem Statement

To design a **Customer 360** system for farmers that:
- Collects and validates multi-source agricultural data
- Assesses eligibility using AI agents
- Performs automated loan approvals and document verification
- Monitors risks (disaster, carbon)
- Sends real-time WhatsApp alerts in **regional languages**

---

## 🧠 Our AI Agent-Based Solution

| Agent Name            | Responsibility                                                |
|----------------------|----------------------------------------------------------------|
| DisasterMonitor       | Flags disaster-prone areas via `disaster_risks.csv`           |
| BusinessAnalyst       | Evaluates farmer profile and practices for eligibility        |
| LoanManager           | Decides loan amount, interest, and approval                   |
| DataMapper            | Maps customer data to required schema                         |
| DataArchitect         | Manages loan schema structures                                |
| DataGovernanceAgent   | Validates against governance rules from `governance_catalog.csv` |
| DocumentationAgent    | Simulates KYC, document checks                                |
| Certifier             | Issues a digital certificate of approval                      |
| GemmaAgent            | Translates alerts into regional languages using Gemma (Ollama)|
| WhatsAppAlert         | Sends loan alerts via Twilio WhatsApp                         |

---

## 📂 Project Structure

```bash
FARMING_LOANS/
├── app.py                       # Streamlit frontend
├── loans.db                     # SQLite DB for history
├── BharatKredit.jpg             # Banner image
│
├── agents/                      # All AI agents
│   ├── business_analyst.py
│   ├── carbon_scorer.py
│   ├── certifier.py
│   ├── data_architecture.py
│   ├── data_governance.py
│   ├── data_mapper.py
│   ├── database.py
│   ├── disaster_monitor.py
│   ├── documentation.py
│   ├── gemma_agent.py
│   ├── loan_manager.py
│   └── whatsapp_alert.py
│
├── data/
│   ├── farmers.csv              # Farmer input profiles
│   ├── disaster_risks.csv       # Disaster-prone regions
│   └── governance_catalog.csv   # Governance checks
