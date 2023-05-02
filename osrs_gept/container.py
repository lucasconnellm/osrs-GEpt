from dependency_injector import containers, providers

from osrs_gept.settings import Settings
from osrs_gept.wiki_client import WikiClient


class OsrsContainer(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[Settings()])
    

    # Wiki client factory
    wiki_client_factory = providers.Factory(
        WikiClient,
        api_url=config.api_url,
        user_agent=config.user_agent,
    )
