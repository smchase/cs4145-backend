# Evaluation of RAG Search Performance (CS4145, Group 3, Backend)
RAG (Retrieval-Augmented Generation) Search is an Artificial Intelligence technique that combines the natural language capabilities of Large Language Models (LLMs) with the functionality of information retrieval systems, such as traditional search engines. The aim of such RAG models is to provide more accurate and factually supported answers to the questions of users.

However, the performance of these models is itself evaluated automatically using a separate LLM as obtaining human evaluations is often deemed too costly. This raises the issue of unwarranted trust in conversational AI and begs the question how a human's judgement would differ from that of the LLM. Exploring this question is precisely the goal of our research, for which we created this system to collect human evaluations of RAG Search responses.

## Setup

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up .env**:
   - Create a `.env` file in the root directory of the project.
   - Add the following environment variables to the `.env` file:
     ```
     DB_HOST=<your-db-host>
      DB_PORT=5432
      DB_NAME=<your-db-name>
      DB_USER=<your-db-user>
      DB_PASSWORD=<your-db-password>
     ```

5. **Set up dev requirements**:
   ```bash
   pip install -r requirements-dev.txt
   pre-commit install
   ```
