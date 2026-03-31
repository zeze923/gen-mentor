from langchain_core.embeddings import Embeddings
from typing import Optional


class EmbedderFactory:
    @staticmethod
    def create(
        model: str = "sentence-transformers/all-MiniLM-L6-v2", 
        model_provider: Optional[str] = "huggingface",
        ) -> Embeddings:
        """Create an embedding model instance based on the specified model name."""
        if ':' in model:
            model_provider, model = model.split(':', 1)
        else:
            model_provider = model_provider or "huggingface"
        match model_provider.lower():
            case "huggingface":
                from langchain_huggingface import HuggingFaceEmbeddings
                import os
                
                # Check if model is a local path, otherwise use it as name
                # You can set an environment variable or a default local path
                local_model_path = os.environ.get("LOCAL_EMBEDDING_MODEL_PATH")
                if local_model_path and os.path.exists(local_model_path):
                    model = local_model_path
                
                # If model is a common name, it will be downloaded once to ~/.cache/huggingface/hub
                # To make it truly "local", users can point to a directory
                return HuggingFaceEmbeddings(
                    model_name=model,
                    model_kwargs={'device': 'cpu'}, # Can be changed to 'cuda' if GPU available
                    encode_kwargs={'normalize_embeddings': True}
                )
            case "openai":
                from langchain_openai import OpenAIEmbeddings
                return OpenAIEmbeddings(model=model)
            case "azure":
                from langchain_openai import AzureOpenAIEmbeddings
                return AzureOpenAIEmbeddings(model=model)
            case "together":
                from langchain_together import TogetherEmbeddings
                return TogetherEmbeddings(model=model)
            # NOTE: Add other model providers here as needed
            case _:
                raise ValueError(f"Unsupported model provider: {model_provider}")


if __name__ == "__main__":
    # Example usage
    embedder = EmbedderFactory.create(
        model="sentence-transformers/all-mpnet-base-v2", 
        model_provider="huggingface")
    text = "Hello, world!"
    embedding = embedder.embed_query(text)
    print(f"Embedding for '{text}': {embedding}")
