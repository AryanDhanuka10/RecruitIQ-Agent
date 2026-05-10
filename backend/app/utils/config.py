from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    groq_api_key: str = ""
    app_env: str = "development"
    log_level: str = "INFO"
    secret_key: str = "changeme"
    langchain_tracing_v2: bool = False
    langchain_api_key: str = ""

    langchain_project: str = "RecruitIQ-Agent"
    langchain_endpoint: str = "https://api.smith.langchain.com"

    model_config = {"env_file": ".env"}

settings = Settings()
