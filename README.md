# cs4145-backend

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
