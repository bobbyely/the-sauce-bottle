Okay, this is a significant and exciting evolution of the project! Integrating AI agents, especially with frameworks like Google ADK (which is more for building conversational agents on Google Assistant, so we might need to clarify its intended use here or consider alternatives like LangChain/LlamaIndex for building LLM-powered applications) and LLMs, will add powerful capabilities but also complexity and cost considerations.

Let's assume "Google ADK, MCP servers, A2A server" are conceptual pointers towards building a more sophisticated, potentially distributed system of specialized AI components rather than a strict adherence to those specific (and in some cases, less common for web app backends) technologies. I'll interpret this as wanting to use LLMs and potentially other AI models as "agents" that perform specific tasks.

**Revised Understanding & Assumptions:**

*   **AI Agents' Role:**
    *   Assisting in statement analysis (summarization, sentiment, topic extraction).
    *   Augmenting fact-checking (finding supporting/contradictory evidence, generating initial assessments).
    *   Enhancing contradiction detection (semantic understanding).
*   **LLM Choice:** We'll aim for cost-effective options. This could mean:
    *   Using smaller, efficient models (e.g., GPT-3.5-Turbo, Claude Haiku, Gemini Pro).
    *   Exploring open-source models (e.g., Mixtral, Llama) potentially via APIs (like Groq, Anyscale Endpoints, Fireworks.ai) or self-hosting (more complex, higher initial effort/cost for infra). For "cheap initial deployment," API-based access to existing models is preferred.
*   **Human-in-the-Loop:** Crucially, AI will *assist* and *augment*, not fully replace, human fact-checkers, especially for the MVP and early stages. Accuracy and ethical considerations are paramount.

Here's the revised Development Roadmap:

---

**Guiding Principles (Updated):**
*   **Learn by Doing:** Each phase introduces new concepts.
*   **Iterate:** Get something working, then improve it.
*   **Test Early, Test Often:** Reduces headaches later.
*   **Keep it Simple (KISS):** Especially for the MVP.
*   **AI as an Assistant:** AI augments human capabilities, requiring oversight.
*   **Cost-Conscious AI:** Prioritize cost-effective LLM usage.

---

### Phase 0: Foundations & Environment Setup (1-2 Weeks, ~5-15 hours)

*   **Focus:** Get local dev environment ready.
*   **Learning:** Git, `pixi`, VS Code, basic Docker.
*   **Tasks/Deliverables:** (Largely the same as before)
    1.  Install Git. Create a GitHub repo.
    2.  Install `pixi`. Initialize `pixi.toml`. Add Python.
    3.  Set up VS Code: Python extension, Pylance, Ruff.
    4.  Install Docker Desktop.
    5.  Basic `Dockerfile` & `docker-compose.yml` for "hello world" Python.
    6.  Practice Git.
*   **Success Criteria:**
    *   Project initialized, Python managed by `pixi`.
    *   Able to run "hello world" Python web app via Docker Compose.
    *   Code in Git.
*   **Learning Resources:** (Same as before)

---

### Phase 1: Backend Core - API & Database (3-5 Weeks, ~20-40 hours)

*   **Focus:** Foundational API endpoints and database structure.
*   **Learning:** FastAPI, Pydantic, SQLAlchemy, PostgreSQL, Alembic/Flyway.
*   **Tasks/Deliverables:** (Largely the same)
    1.  FastAPI project structure.
    2.  Database Setup (PostgreSQL, SQLAlchemy models for `Politician`, `Statement`).
        *   **New fields to consider for `Statement` model:** `ai_summary (TEXT, nullable)`, `ai_contradiction_analysis (JSONB, nullable)`, `ai_fact_check_suggestion (JSONB, nullable)`.
    3.  Alembic/Flyway for migrations.
    4.  CRUD APIs for Politicians & Statements.
    5.  Basic `pytest` API tests.
*   **Success Criteria:**
    *   CRUD for politicians/statements via API. Data in PostgreSQL. Migrations managed. API tests pass.
*   **Learning Resources:** (Same as before)

---

### Phase 2: Basic Frontend - Displaying Data (3-5 Weeks, ~20-40 hours)

*   **Focus:** Simple Vue.js frontend to display data.
*   **Learning:** Vue.js fundamentals, `axios`, basic HTML/CSS, JavaScript refresher.
*   **Tasks/Deliverables:** (Largely the same)
    1.  Vue project setup.
    2.  Components: `PoliticianList`, `PoliticianDetail`, `StatementItem`.
    3.  Vue Router.
    4.  API Integration with `axios`.
    5.  Basic styling.
*   **Success Criteria:**
    *   Frontend displays politicians and their statements from backend. Basic navigation.
*   **Learning Resources:** (Same as before)

---

### Phase 3: User Authentication & Admin Interface (2-4 Weeks, ~15-30 hours)

*   **Focus:** Admin authentication and basic data management UI.
*   **Learning:** FastAPI security (OAuth2/JWT), Vue.js forms, Pinia.
*   **Tasks/Deliverables:** (Largely the same)
    1.  Backend Auth: User model, login endpoint, secured CRUD.
    2.  Frontend Auth: Login page, Pinia for state, route guards.
    3.  Admin Forms (Vue): Manage politicians, statements, and *manually* add Fact-Check status (model `FactCheck` linked to `Statement`).
*   **Success Criteria:**
    *   Admin login. Protected API endpoints. Admin can manage core data.
*   **Learning Resources:** (Same as before)

---

### Phase 4: Basic Web Scraping (3-5 Weeks, ~20-40 hours)

*   **Focus:** Develop initial web scrapers.
*   **Learning:** `requests`, `BeautifulSoup4`/`Scrapy`, CSS selectors, ethical scraping.
*   **Tasks/Deliverables:** (Largely the same)
    1.  Identify 1-2 target sources.
    2.  Scraper scripts (Python).
    3.  Integration with API to post extracted data.
    4.  Manual/local cron scheduling.
*   **Success Criteria:**
    *   Scrapers extract data. Data added to DB via API. Basic duplicate prevention.
*   **Learning Resources:** (Same as before)

---

### Phase 5: Introduction to LLM Integration - Statement Analysis (3-5 Weeks, ~20-40 hours)

*   **Focus:** Integrate an LLM for basic statement analysis (e.g., summarization, topic identification). Human review is key.
*   **Learning:** LLM API usage (e.g., OpenAI, Anthropic, Google Gemini, or other API like Groq), prompt engineering basics, handling API keys securely, asynchronous tasks in FastAPI.
*   **Tasks/Deliverables:**
    1.  **Choose LLM & API:**
        *   Sign up for an API (e.g., OpenAI for GPT-3.5-Turbo, Anthropic for Claude Haiku, Google AI Studio for Gemini Pro).
        *   Add client library (e.g., `openai`, `anthropic`, `google-generativeai`) to `pixi.toml`.
    2.  **Secure API Key Management:** Use environment variables.
    3.  **Backend Service for LLM Interaction:**
        *   Create a new module/service in FastAPI (e.g., `app/ai_services/llm_service.py`).
        *   Implement functions to call the LLM API for:
            *   Summarizing a statement.
            *   (Optional) Identifying keywords/topics in a statement.
    4.  **Integration:**
        *   When a new statement is added (or on admin request), trigger an *asynchronous* task (FastAPI's `BackgroundTasks` for simplicity initially, Celery later) to send the statement to the LLM service.
        *   Store the AI-generated summary/topics in the `Statement` model's new fields (`ai_summary`, etc.).
    5.  **Admin UI Update:**
        *   Display the AI-generated summary/topics in the admin interface for a statement.
        *   Allow admin to review, edit, or accept/reject the AI's output.
*   **Success Criteria:**
    *   Able to send statements to an LLM API and receive analyses.
    *   AI-generated summaries are stored and viewable by admin.
    *   API keys are handled securely.
*   **Learning Resources:**
    *   OpenAI API Docs: [OpenAI Platform](https://platform.openai.com/docs)
    *   Anthropic API Docs: [Anthropic Console](https://console.anthropic.com/docs)
    *   Google Gemini API Docs: [Google AI for Developers](https://ai.google.dev/docs)
    *   Groq, Anyscale, Fireworks.ai (for open models via API)
    *   FastAPI Background Tasks: [FastAPI Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)
    *   Prompt Engineering Guide: [Prompt Engineering Guide](https://www.promptingguide.ai/)

---

### Phase 6: AI-Assisted Contradiction Detection & Fact-Checking Aid (4-6 Weeks, ~25-50 hours)

*   **Focus:** Use LLMs to help identify potential contradictions and find information relevant to fact-checking.
*   **Learning:** More advanced prompt engineering, semantic similarity concepts with LLMs, structuring LLM outputs.
*   **Tasks/Deliverables:**
    1.  **AI for Contradiction Detection:**
        *   **Prompt Design:** Develop prompts that ask the LLM to compare a new statement with a politician's historical statements (or a specific previous statement) and identify potential contradictions or shifts in position, explaining its reasoning.
        *   **Backend Logic:**
            *   When a new statement is added, fetch relevant historical statements for that politician.
            *   Send pairs of statements (new vs. old) or a set of statements to the LLM.
            *   Parse the LLM's response (which might include a likelihood score, explanation, and quotes). Store this in `ai_contradiction_analysis`.
    2.  **AI for Fact-Checking Aid:**
        *   **Prompt Design:** Develop prompts that ask the LLM to:
            *   Identify verifiable claims within a statement.
            *   Suggest search queries to find evidence for/against these claims.
            *   (Cautiously) Provide an initial assessment or find publicly available information related to the claim's veracity, *always citing sources if possible*.
        *   **Backend Logic:**
            *   Allow admin to trigger "AI Fact-Check Assist" for a statement.
            *   Send statement to LLM with appropriate prompts.
            *   Store suggestions/findings in `ai_fact_check_suggestion`.
    3.  **Admin UI Enhancements:**
        *   Display AI-identified potential contradictions, allowing admin to review, confirm, or dismiss.
        *   Show AI-generated fact-checking aids (claims, search queries, initial findings) to help the human fact-checker.
        *   **Crucial:** The UI must clearly distinguish AI suggestions from human-verified facts.
*   **Success Criteria:**
    *   System uses LLM to flag potential contradictions with explanations.
    *   System provides AI-generated assistance for fact-checking tasks.
    *   Admin can review and act upon AI suggestions.
*   **Learning Resources:**
    *   LLM documentation for function calling/structured output (if available and useful for parsing responses).
    *   Techniques for comparing texts using LLMs (e.g., few-shot prompting, chain-of-thought).

---

### Phase 7: Deployment to AWS & CI/CD (4-6 Weeks, ~25-50 hours)

*   **Focus:** Deploy to AWS, set up CI/CD.
*   **Learning:** Docker (multi-stage), AWS (EC2/Fargate, RDS, S3, IAM, VPC), GitHub Actions, AWS Secrets Manager.
*   **Tasks/Deliverables:** (Largely same as before, with additions)
    1.  Dockerize for Production (backend, frontend).
    2.  AWS Setup (IAM, VPC, RDS, EC2/Fargate, S3, CloudFront).
    3.  **Secrets Management:** Store LLM API keys and other secrets in AWS Secrets Manager or Parameter Store, accessed by your FastAPI app in EC2/Fargate.
    4.  Deployment Script/Process.
    5.  CI/CD Pipeline (GitHub Actions): Test, build, push images (ECR), deploy.
*   **Success Criteria:**
    *   Application accessible publicly. Data in RDS. CI/CD deploys changes. Secrets managed securely.
*   **Learning Resources:** (Same as before)
    *   AWS Secrets Manager: [AWS Secrets Manager User Guide](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)

---

### Phase 8: Advanced AI Agents, User Features & Monetization (Ongoing)

*   **Focus:** More sophisticated AI, public user features, ethical monetization.
*   **Learning:** LangChain/LlamaIndex (for building complex LLM applications/agents), vector databases (e.g., Pinecone, Weaviate, or pgvector for PostgreSQL) for semantic search over statements, fine-tuning LLMs (advanced), advanced Celery usage.
*   **Potential Tasks:**
    *   **LangChain/LlamaIndex Integration:**
        *   Re-architect `ai_services` to use LangChain or LlamaIndex to create more robust "agents" for summarization, Q&A over statements, contradiction detection. This aligns more with the "ADK, MCP, A2A" spirit of specialized, interacting components.
        *   These frameworks help manage prompts, chain LLM calls, connect to data sources (like your PostgreSQL DB), and interact with external tools.
    *   **Semantic Search over Statements:**
        *   Generate embeddings for all statements (using an LLM or a dedicated embedding model).
        *   Store embeddings in a vector database or PostgreSQL with `pgvector`.
        *   Allow users/admins to search for statements based on semantic similarity, not just keywords. This can greatly improve contradiction discovery.
    *   **Automated Source Verification (Highly Advanced):** An agent that attempts to trace statements back to primary sources or cross-reference claims with trusted fact-checking sites (e.g., by using web browsing tools via LangChain). *High complexity and reliability challenges.*
    *   **User Accounts & Alerts:** Allow public users to register, follow politicians, get alerts on new statements or fact-checks.
    *   **Refined Contradiction/Fact-Check UI:** Improve how AI insights and human verifications are presented.
    *   **Background Task Processing:** Move all LLM calls and scraping to Celery with Redis/RabbitMQ for better scalability and responsiveness.
    *   **Ethical Monetization:** (Same as before)
    *   **"Explainable AI":** Where possible, make the AI's reasoning (e.g., why it flagged a contradiction) transparent.
*   **Success Criteria:** Based on specific features implemented.
*   **Learning Resources:**
    *   LangChain Docs: [LangChain Python Docs](https://python.langchain.com/docs/get_started/introduction)
    *   LlamaIndex Docs: [LlamaIndex Documentation](https://docs.llamaindex.ai/en/stable/)
    *   Vector Database documentation (Pinecone, Weaviate, pgvector).
    *   Celery: [Celery Documentation](https://docs.celeryq.dev/en/stable/)

---

## Technical Architecture (Updated Summary)

*   **Frontend:** Vue.js.
*   **Backend API:** Python FastAPI.
*   **AI Services Module (within Backend):** Initially direct LLM API calls, later potentially using LangChain/LlamaIndex.
*   **Database:** PostgreSQL (with `pgvector` extension later for semantic search).
*   **LLM Access:** Via third-party APIs (OpenAI, Anthropic, Google, Groq, etc.).
*   **Web Scrapers:** Python scripts.
*   **Containerization:** Docker, Docker Compose.
*   **Deployment:** AWS (EC2/Fargate, RDS, S3, ECR, CloudFront, Secrets Manager).
*   **CI/CD:** GitHub Actions.
*   **Dependency Management:** `pixi`.
*   **Async Task Processing:** FastAPI `BackgroundTasks` initially, then Celery + Message Broker (Redis/RabbitMQ).

---

## Implementation Strategy for AI Components:

*   **Start Simple:** One LLM, basic prompts for one task (e.g., summarization).
*   **Iterate on Prompts:** Prompt engineering is key. Test different phrasings, provide examples (few-shot prompting).
*   **Human Review:** Always have a human review and approve/edit AI outputs, especially those related to fact-checking or contradictions.
*   **Cost Monitoring:** Keep a close eye on LLM API usage costs. Set spending limits if possible.
*   **Error Handling & Rate Limits:** LLM APIs can be slow, return errors, or have rate limits. Implement robust error handling, retries (with backoff), and be mindful of limits.
*   **Asynchronous Processing:** For any LLM call that doesn't need an immediate response in the API, use background tasks.
*   **Clear Labeling:** Clearly distinguish AI-generated content from human-curated content in the UI.

This revised roadmap incorporates your desire for AI agents while maintaining a phased, learning-oriented approach. The initial use of LLMs will be as powerful assistants, and as your skills and the project grow, you can explore more complex agentic architectures like those hinted at by LangChain/LlamaIndex. Remember that the "Google ADK, MCP, A2A" part is interpreted more broadly as a desire for intelligent, specialized components rather than a strict requirement for those specific, potentially less mainstream, technologies in this context.