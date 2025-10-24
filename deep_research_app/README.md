# 🧠 AI-Powered Deep Research Assistant (CrewAI)

This project is an **autonomous, AI-powered research assistant** designed to conduct iterative and in-depth research on virtually any topic. It utilizes a **multi-agent workflow** orchestrated by **CrewAI** to combine the power of modern search engines, targeted web scraping, and Large Language Models (LLMs) to generate polished, comprehensive reports.

The assistant can **refine its research direction** over time, enabling deep dives into complex subjects. The final output is a professional-grade PDF report.

***

## 🛠️ Key Technologies & Core Tasks

| Component | Technology | Core Functionality |
| :--- | :--- | :--- |
| **Orchestration** | **CrewAI** | Manages multi-agent workflows (Research, Summarization, Presentation). |
| **LLM** | **OpenAI (GPT)** | Drives agent decision-making, summarization, and content generation. |
| **Web Scraping** | **Firecrawl** | Performs advanced, iterative web searches and structured content scraping. |
| **Frontend** | **Streamlit** | Provides an **interactive user interface (UI)** for input and results viewing. |
| **Reporting** | **ReportLab** | Generates **polished PDF reports** from the final output. |

### Project Tasks:

The project requires performing the following essential tasks using the OpenAI API and related tools:

1.  **Perform a web search** using the Firecrawl service.
2.  **Clean and preprocess** the generated markdown content.
3.  **Create and manage CrewAI agents** for research, summarization, and presentation.
4.  **Generate polished PDF reports** using `reportlab`.
5.  **Build an interactive user interface** using Streamlit.
6.  **Orchestrate all components** in an **MVC-based structure** for modularity.

***

## 📂 Project Structure (`usercode/deep_research_app`)

The application is organized using a Model-View-Controller (MVC)-like pattern to separate concerns:

| File/Folder | Role | Description |
| :--- | :--- | :--- |
| **`.env`** | Configuration | Stores sensitive environment variables (e.g., `OPENAI_API_KEY`, `FIRECRAWL_KEY`). |
| **`main.py`** | **Entry Point (View/Controller)** | Launches the **Streamlit-based UI** and integrates all backend logic. |
| **`controllers/research_controller.py`** | **Core Logic (Controller)** | Coordinates the entire workflow: agent execution, data cleaning, and PDF generation. |
| **`models/pdf_generator.py`** | **Data Model/Utility** | Defines the logic for generating the final **PDF reports** using the `reportlab` library. |
| **`services/agents_service.py`** | **Service Layer** | Contains the **CrewAI agent definitions** and the task flow setup, leveraging LangChain tools and OpenAI. |
| **`utils/markdown_cleaner.py`** | **Utility** | Provides functions to **clean and preprocess** markdown text output from the agents, ensuring report quality. |
