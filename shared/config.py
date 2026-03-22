from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_base_url: str = Field(default='http://127.0.0.1:8080', alias='APP_BASE_URL')
    app_admin_token: str = Field(default='change-me', alias='APP_ADMIN_TOKEN')
    database_url: str = Field(default='sqlite:///./data/proxy.db', alias='DATABASE_URL')
    bot_token: str = Field(default='', alias='BOT_TOKEN')
    bot_admin_ids_raw: str = Field(default='', alias='BOT_ADMIN_IDS')
    server_address: str = Field(default='127.0.0.1', alias='SERVER_ADDRESS')
    reality_port: int = Field(default=443, alias='REALITY_PORT')
    reality_sni: str = Field(default='www.cloudflare.com', alias='REALITY_SNI')
    reality_public_key: str = Field(default='', alias='REALITY_PUBLIC_KEY')
    reality_short_id: str = Field(default='', alias='REALITY_SHORT_ID')
    hy2_port: int = Field(default=8443, alias='HY2_PORT')
    hy2_sni: str = Field(default='example.com', alias='HY2_SNI')
    hy2_insecure: bool = Field(default=True, alias='HY2_INSECURE')

    @property
    def bot_admin_ids(self) -> list[int]:
        if not self.bot_admin_ids_raw.strip():
            return []
        return [int(x.strip()) for x in self.bot_admin_ids_raw.split(',') if x.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
