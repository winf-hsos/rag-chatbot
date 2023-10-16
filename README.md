# RAG Chatbot Framework
A framework for RAG chatbots developed at the University of Applied Sciences Osnabrück.

## Create and activate Python virtual environment

To create a virtual environment, type into terminal:
```
python -m venv .env
```

To activate, type into terminal:
```
.env\Scripts\activate
```

## Install required Python libraries

```
pip install -r requirements.txt
```

# Set the path for the configuration file
The whole chatbot framework is configured using a single config file: `config/config.yaml`. Within the framework, this config file is loaded by accessing the environment variable `CHATBOT_CONFIG_FILE`. Make sure you set this environment variable to the correct path:

```
SET CHATBOT_CONFIG_FILE=C:/code/rag-chatbot/chatbot/config.yaml
```

# Run the streamlit app

Goto `frontend/` directory and run:

```
streamlit run Home.py
```

# Links

- [ChromaDB](https://docs.trychroma.com/)
- [Unstructured.io](https://unstructured-io.github.io/unstructured/index.html)