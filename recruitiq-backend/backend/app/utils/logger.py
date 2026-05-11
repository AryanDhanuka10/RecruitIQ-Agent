import os
import logging
from backend.app.utils.config import settings

def setup_logger():
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger("RecruitIQ")

def setup_langsmith():
    if settings.langchain_tracing_v2:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_ENDPOINT"] = settings.langchain_endpoint
        os.environ["LANGCHAIN_API_KEY"] = settings.langchain_api_key
        os.environ["LANGCHAIN_PROJECT"] = settings.langchain_project
        print("LangSmith tracing configured.")
    else:
        print("LangSmith tracing is disabled.")

setup_langsmith()
