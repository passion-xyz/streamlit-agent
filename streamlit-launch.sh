python3 -m venv stramlit-agent
source stramlit-agent/bin/activate
poetry install --sync
python3 -m pip install langchain langchain-community python-dotenv langchain_openai streamlit --use-pep517 --break-system-packages
python3 -m pip install streamlit-scrollable-textbox setuptools streamlit_chat streamlit-extras --use-pep517 --break-system-packages
python3 -m pip freeze > requirements.txt
streamlit run streamlit.py