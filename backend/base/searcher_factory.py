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
import json
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

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
            wrapper.provider_name = "duckduckgo"
        elif p in {"serper", "serper.dev", "google-serper"}:
            from langchain_community.utilities import GoogleSerperAPIWrapper
            wrapper = GoogleSerperAPIWrapper()
            wrapper.provider_name = "serper"
        elif p in {"bing", "microsoft-bing"}:
            from langchain_community.utilities import BingSearchAPIWrapper
            bing_subscription_key = kwargs.get("bing_subscription_key", None)
            bing_search_url = kwargs.get("bing_search_url", None)
            assert bing_subscription_key is not None, "bing_subscription_key is required for BingSearchAPIWrapper"
            assert bing_search_url is not None, "bing_search_url is required for BingSearchAPIWrapper"
            wrapper = BingSearchAPIWrapper(bing_subscription_key=bing_subscription_key, bing_search_url=bing_search_url)
            wrapper.provider_name = "bing"
        elif p in {"brave", "brave-search"}:
            from langchain_community.utilities import BraveSearchWrapper
            wrapper = BraveSearchWrapper()
            wrapper.provider_name = "brave"
        elif p in {"searx", "searxng", "searx-ng"}:
            # 读取 SearXNG 相关配置
            search_cfg = kwargs.get("search", {}) if isinstance(kwargs, dict) else {}
            searx_base_url = search_cfg.get("base_url") or search_cfg.get("searx_base_url") or kwargs.get("base_url")
            if not searx_base_url:
                raise ValueError("SearXNG requires search.base_url to be set, e.g. http://<host>:8080")
            # 可选参数
            searx_engines = search_cfg.get("engines", None)
            searx_categories = search_cfg.get("categories", None)
            searx_language = search_cfg.get("language", None)
            searx_timeout = search_cfg.get("timeout", 20)
            searx_verify_ssl = search_cfg.get("verify_ssl", False)
            wrapper = _SearxNGSearchWrapper(
                base_url=searx_base_url,
                engines=searx_engines,
                categories=searx_categories,
                language=searx_language,
                timeout=searx_timeout,
                verify_ssl=searx_verify_ssl,
            )
            wrapper.provider_name = "searx"
        else:
            raise ValueError("Unsupported search provider. Choose from {'bing', 'serper', 'duckduckgo', 'brave', 'searx', 'you'}.")
        return wrapper


@dataclass
class _SearxNGSearchWrapper:
    """Minimal SearXNG JSON API wrapper compatible with LangChain-style .results()."""
    base_url: str
    engines: list[str] | None = None
    categories: list[str] | None = None
    language: str | None = None
    timeout: int = 20
    verify_ssl: bool = False

    def _build_params(self, query: str, max_results: int | None = None) -> dict:
        params: dict[str, Any] = {
            "q": query,
            "format": "json",
        }
        if max_results:
            params["limit"] = max_results
        if self.language:
            params["language"] = self.language
        if self.categories:
            # SearXNG 支持 categories=general,web,news 等，以逗号分隔
            params["categories"] = ",".join(self.categories)
        if self.engines:
            # 通过 engines 参数限制具体引擎
            params["engines"] = ",".join(self.engines)
        return params

    def results(self, query: str, max_results: int = 5) -> list[dict]:
        import requests  # 延迟导入，避免在未使用时增加依赖负担
        url = self.base_url.rstrip("/") + "/search"
        params = self._build_params(query, max_results)
        try:
            resp = requests.get(url, params=params, timeout=self.timeout, verify=self.verify_ssl)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            # 返回空列表以与其他 wrapper 行为一致
            print(f"SearXNG request error: {e}")
            return []

        # 规范化结构：title/link/snippet
        items = []
        for r in data.get("results", []):
            link = r.get("url") or r.get("link") or r.get("href") or ""
            title = r.get("title") or ""
            snippet = r.get("content") or r.get("snippet") or r.get("summary") or None
            if link:
                items.append({"title": title, "link": link, "snippet": snippet})
            if len(items) >= max_results:
                break
        return items

class WebDocumentLoader:

    @staticmethod
    def invoke(
        urls: List[str],
        loader_type: str = "web",
        timeout: int = 10,
        concurrency: int = 4,
    ) -> List[Document]:
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
            
            def fetch_single(u: str) -> List[Document]:
                try:
                    loader = WebBaseLoader(
                        [u],
                        requests_kwargs={
                            'timeout': timeout,
                            'verify': False,
                            'headers': {
                                'User-Agent': os.environ.get("USER_AGENT", "Mozilla/5.0")
                            }
                        }
                    )
                    return loader.load()
                except Exception as e:
                    print(f"Error loading document from {u}: {e}")
                    return []

            # 并发抓取，尽快返回可用结果
            with ThreadPoolExecutor(max_workers=max(1, concurrency)) as executor:
                future_to_url = {executor.submit(fetch_single, u): u for u in urls}
                for future in as_completed(future_to_url):
                    docs = future.result()
                    if docs:
                        documents.extend(docs)
        
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
            load_page_content: bool = False,
            loader_timeout: int = 10,
            loader_concurrency: int = 4,
            **kwargs: Any
        ) -> None:
        self.searcher = searcher
        self.loader_type = loader_type
        self.max_search_results = max_search_results
        self.load_page_content = load_page_content
        self.loader_timeout = loader_timeout
        self.loader_concurrency = loader_concurrency

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
            load_page_content=config_dict.get("search", {}).get("load_page_content", False),
            loader_timeout=config_dict.get("search", {}).get("loader_timeout", 10),
            loader_concurrency=config_dict.get("search", {}).get("loader_concurrency", 4),
        )

    def invoke(self, query: str) -> List[SearchResult]:
        """Perform a search and return structured results with fallback mechanism."""
        raw_results = []
        providers_to_try = []
        
        # Determine the primary and fallback providers
        primary_provider = getattr(self.searcher, "provider_name", "unknown")
        providers_to_try.append(primary_provider)
        
        # Add fallback providers if not already the primary
        for p in ["searx", "duckduckgo"]:
            if p not in providers_to_try:
                providers_to_try.append(p)

        import logging
        logger = logging.getLogger(__name__)

        for provider in providers_to_try:
            try:
                current_searcher = self.searcher
                if provider != primary_provider:
                    logger.info(f"Falling back to search provider: {provider}")
                    # Create a temporary searcher for fallback
                    # Note: This is a simplified fallback. In a real scenario, you'd want to 
                    # pass the original config to SearcherFactory.create
                    try:
                        # Use fallback provider without requiring SearXNG base_url
                        temp_searcher = SearcherFactory.create(provider=provider)
                        raw_results = temp_searcher.results(query, max_results=self.max_search_results)
                    except Exception as fallback_err:
                        logger.warning(f"Fallback to {provider} failed: {fallback_err}")
                        continue
                else:
                    raw_results = self.searcher.results(query, max_results=self.max_search_results)
                
                if raw_results:
                    logger.info(f"Search successful using provider: {provider}")
                    break
            except Exception as e:
                logger.warning(f"Search provider {provider} failed: {e}")
                continue

        if not raw_results:
            logger.error("All search providers failed. Returning empty results.")
            return []

        urls = [item.get("link", "") for item in raw_results if item.get("link")]
        url_contents: List[Document] = []
        if self.load_page_content and urls:
            # 可选地加载页面正文；失败不阻塞
            url_contents = WebDocumentLoader.invoke(
                urls,
                loader_type=self.loader_type,
                timeout=self.loader_timeout,
                concurrency=self.loader_concurrency,
            )
        
        # 创建 URL 到文档的映射，处理可能的长度不匹配
        url_docs_dict = {}
        url_content_dict = {}
        for i, url in enumerate(urls):
            if self.load_page_content and i < len(url_contents) and url_contents[i] is not None:
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