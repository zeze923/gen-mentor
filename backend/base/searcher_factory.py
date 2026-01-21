"""Concise provider-agnostic web search factory using LangChain community utilities.

This implementation leverages lightweight wrappers shipped with LangChain
instead of hand-written HTTP code. It supports Bing, Tavily, and Serper.dev.
"""

from __future__ import annotations

from pydoc import doc
from typing import Any, Dict, List, Union, cast
from langchain_core.documents import Document
from .dataclass import SearchResult
from pydantic import BaseModel
from omegaconf import OmegaConf, DictConfig
from utils.config import ensure_config_dict
import warnings
import urllib3

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SearcherFactory:
    """Create concise searchers backed by LangChain community utilities."""

    @staticmethod
    def create(provider: str, **kwargs: Any) -> BaseModel:
        p = (provider or "").strip().lower()
        if p in {"duckduckgo", "duck-duck-go"}:
            from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
            wrapper = DuckDuckGoSearchAPIWrapper(region="us-en", safesearch="moderate")
        elif p in {"serper", "serper.dev", "google-serper"}:
            from langchain_community.utilities import GoogleSerperAPIWrapper
            wrapper = GoogleSerperAPIWrapper()
        elif p in {"bing", "microsoft-bing"}:
            from langchain_community.utilities import BingSearchAPIWrapper
            bing_subscription_key = kwargs.get("bing_subscription_key", None)
            bing_search_url = kwargs.get("bing_search_url", None)
            assert bing_subscription_key is not None, "bing_subscription_key is required for BingSearchAPIWrapper"
            assert bing_search_url is not None, "bing_search_url is required for BingSearchAPIWrapper"
            wrapper = BingSearchAPIWrapper(bing_subscription_key=bing_subscription_key, bing_search_url=bing_search_url)
        elif p in {"brave", "brave-search"}:
            from langchain_community.utilities import BraveSearchWrapper
            wrapper = BraveSearchWrapper()
        else:
            raise ValueError("Unsupported search provider. Choose from {'bing', 'serper', 'duckduckgo', 'brave', 'searx', 'you'}.")
        return wrapper


class WebDocumentLoader:

    @staticmethod
    def invoke(urls: List[str], loader_type: str = "web") -> List[Document]:
        """Load documents from the provided URLs using the specified loader."""
        if not urls:
            return []
        
        documents = []
        
        if loader_type == "docling":
            from langchain_docling import DoclingLoader
            try:
                loader = DoclingLoader(urls)
                documents = loader.load()
            except Exception as e:
                print(f"Error loading documents from URLs with Docling: {e}")
                
        elif loader_type == "web":
            from langchain_community.document_loaders import WebBaseLoader
            import os
            
            # 设置 USER_AGENT 环境变量（如果未设置）
            if not os.environ.get("USER_AGENT"):
                os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            
            # 逐个加载 URL，这样即使某些失败，其他的仍然可以成功
            for url in urls:
                try:
                    loader = WebBaseLoader(
                        [url], 
                        requests_kwargs={
                            'timeout': 30,  # 增加超时时间到 30 秒
                            'verify': False,  # 禁用 SSL 验证
                            'headers': {
                                'User-Agent': os.environ.get("USER_AGENT", "Mozilla/5.0")
                            }
                        }
                    )
                    docs = loader.load()
                    documents.extend(docs)
                except Exception as e:
                    print(f"Error loading document from {url}: {e}")
                    # 继续处理下一个 URL
                    continue
        
        if not documents:
            print("No documents successfully loaded from any URL.")
            
        return documents


class SearchRunner:
    """Manager to perform searches using different providers."""

    def __init__(
            self, 
            searcher: BaseModel,
            loader_type: str = "web",
            max_search_results: int = 5,
            **kwargs: Any
        ) -> None:
        self.searcher = searcher
        self.loader_type = loader_type
        self.max_search_results = max_search_results

    @staticmethod
    def from_config(
            config: Union[DictConfig, Dict[str, Any]],
        ) -> "SearchRunner":
  
        config_dict = ensure_config_dict(config)
        searcher = SearcherFactory.create(
            provider=config_dict.get("search", {}).get("provider", "duckduckgo"),
            **config_dict,
        )
        return SearchRunner(
            searcher=searcher,
            loader_type=config_dict.get("search", {}).get("loader_type", "web"),
            max_search_results=config_dict.get("search", {}).get("max_results", 5),
        )

    def invoke(self, query: str) -> List[SearchResult]:
        """Perform a search and return structured results."""
        raw_results = self.searcher.results(query, max_results=self.max_search_results)
        urls = [item.get("link", "") for item in raw_results if item.get("link")]
        
        # 加载文档内容，但即使失败也继续处理
        url_contents = WebDocumentLoader.invoke(urls, loader_type=self.loader_type)
        
        # 创建 URL 到文档的映射，处理可能的长度不匹配
        url_docs_dict = {}
        url_content_dict = {}
        for i, url in enumerate(urls):
            if i < len(url_contents) and url_contents[i] is not None:
                url_docs_dict[url] = url_contents[i]
                url_content_dict[url] = url_contents[i].page_content
            else:
                # 如果文档加载失败，使用空内容
                url_content_dict[url] = ""

        structured_results: List[SearchResult] = []
        for item in raw_results:
            link = item.get("link", "")
            structured_results.append(
                SearchResult(
                    title=item.get("title", ""),
                    link=link,
                    content=url_content_dict.get(link, ""),
                    snippet=item.get("snippet", None),
                    document=url_docs_dict.get(link, None)
                )
            )

        return structured_results


if __name__ == "__main__":
    searcher = SearcherFactory.create(
        provider="duckduckgo",
    )

    searcher_runner = SearchRunner(
        searcher=searcher,
        loader_type="web",
        max_search_results=5,
    )
    results = searcher_runner.invoke("LangChain community utilities")
    print(results)