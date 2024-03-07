from pydantic import SecretStr, field_serializer
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigModel(BaseSettings):
    bot_token: SecretStr

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_serializer('bot_token', when_used='json')
    def dump_secret(self, v):
        return v.get_secret_value()

# config = ConfigModel()
# print(config.bot_token.get_secret_value())
# print(config.model_dump_json())
