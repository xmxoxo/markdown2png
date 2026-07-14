import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "markdown2png"
    APP_VERSION: str = "1.0.0"
    TEMPLATE_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "template")
    OUTPUT_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "output")
    QINIU_ACCESS_KEY: str = os.getenv("QINIU_ACCESS_KEY", "")
    QINIU_SECRET_KEY: str = os.getenv("QINIU_SECRET_KEY", "")
    QINIU_BUCKET_NAME: str = os.getenv("QINIU_BUCKET_NAME", "kksaas")
    QINIU_BUCKET_DOMAIN: str = os.getenv("QINIU_BUCKET_DOMAIN", "https://up-kksaas.keyibao.com")

    class Config:
        case_sensitive = True


settings = Settings()