# Setup
- Install Python version 3.11 (pyenv recommended)
- Run the `install_dependencies.sh` script to install requirements and setup a virtual environment (`.venv`)
- Activate the virtual environment `source .venv/bin/activate`
- Build and run the Milvus docker container with `docker compose up` at the root directory of this project
- Create `.env` file and populate it with API keys:
    - `OPENAI_API_KEY`
