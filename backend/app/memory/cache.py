"""
LangChain SQLite cache — prevents redundant LLM calls during dev.
"""
from langchain_core.globals import set_llm_cache
from langchain_community.cache import SQLiteCache

def init_cache(db_path: str = ".langchain.db"):
    set_llm_cache(SQLiteCache(database_path=db_path))

