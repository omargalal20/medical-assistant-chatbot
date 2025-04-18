from langchain_community.retrievers import PubMedRetriever
from loguru import logger

from config.settings import get_settings

settings = get_settings()


class RetrieverClient:
    """Retriever Client"""

    def __init__(self):
        """Initialize Retriever configuration."""
        try:
            self.retriever = PubMedRetriever(
                api_key=settings.RETRIEVER_API_KEY,
                top_k_results=settings.RETRIEVER_TOP_K_RESULTS,
            )
        except Exception as e:
            logger.error(f"LLM failed to instantiate: {str(e)}")
            raise RuntimeError("LLM failed to instantiate.") from e

    def get_retriever(self):
        """Return the configured LLM instance."""
        return self.retriever

    async def get_relevant_documents(self, query: str):
        """Return the configured LLM instance."""
        return await self.retriever.ainvoke(query)
