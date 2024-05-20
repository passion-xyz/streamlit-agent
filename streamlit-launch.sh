python3 -m venv agent-with-memory
source agent-with-memory/bin/activate
poetry install --sync
python3 -m pip install langchain langchain-community python-dotenv langchain_openai --use-pep517 --break-system-packages
python3 main.py