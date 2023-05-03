from pydantic import BaseSettings


class Settings(BaseSettings):
    api_url: str = "https://prices.runescape.wiki/api/v1/osrs"
    wiki_url: str = "https://oldschool.runescape.wiki/w/"

    user_agent: str = "osrs_gept/0.0.1"
    running_on: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

        fields = {
            "api_url": {"env": "API_URL"},
            "wiki_url": {"env": "WIKI_URL"},
            "user_agent": {"env": "USER_AGENT"},
            "running_on": {"env": "RUNNING_ON"},
        }
