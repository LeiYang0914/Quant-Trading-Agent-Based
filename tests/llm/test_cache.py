"""Tests for ResponseCache."""

import pytest

from src.llm.utils.cache import ResponseCache, _NEVER_CACHE
from src.llm.types import (
    Complexity,
    Domain,
    LLMResponse,
    ProviderName,
    TaskRequest,
    TaskType,
)


@pytest.fixture
def cache():
    c = ResponseCache(cache_dir=".cache/llm/test", ttl_seconds=3600, enabled=True)
    yield c
    c.clear()


@pytest.fixture
def sample_request():
    return TaskRequest(
        task_id="test-001",
        agent_name="research-agent",
        task_type=TaskType.SUMMARIZATION,
        prompt="Summarize this document about market trends.",
        domain=Domain.CRYPTO,
    )


@pytest.fixture
def sample_response(sample_request):
    return LLMResponse(
        task_id=sample_request.task_id,
        success=True,
        provider=ProviderName.DEEPSEEK,
        model="deepseek-v4-flash",
        content="This document discusses market trends in crypto.",
        estimated_cost=0.001,
    )


class TestCacheOperations:
    def test_cache_miss_initially(self, cache, sample_request):
        result = cache.get(sample_request, "deepseek", "deepseek-v4-flash")
        assert result is None

    def test_put_and_get(self, cache, sample_request, sample_response):
        cache.put(sample_request, "deepseek", "deepseek-v4-flash", sample_response)
        result = cache.get(sample_request, "deepseek", "deepseek-v4-flash")
        assert result is not None
        assert result.cache_hit is True
        assert result.content == sample_response.content
        assert result.provider == ProviderName.DEEPSEEK

    def test_different_prompt_different_key(self, cache, sample_request, sample_response):
        cache.put(sample_request, "deepseek", "deepseek-v4-flash", sample_response)
        req2 = TaskRequest(
            task_id="test-002",
            agent_name="research-agent",
            task_type=TaskType.SUMMARIZATION,
            prompt="A completely different prompt.",
        )
        result = cache.get(req2, "deepseek", "deepseek-v4-flash")
        assert result is None

    def test_different_provider_different_key(self, cache, sample_request, sample_response):
        cache.put(sample_request, "deepseek", "deepseek-v4-flash", sample_response)
        result = cache.get(sample_request, "claude", "claude-sonnet-4-6")
        assert result is None

    def test_clear_removes_all(self, cache, sample_request, sample_response):
        cache.put(sample_request, "deepseek", "deepseek-v4-flash", sample_response)
        assert cache.size == 1
        cache.clear()
        assert cache.size == 0
        result = cache.get(sample_request, "deepseek", "deepseek-v4-flash")
        assert result is None

    def test_disabled_cache_always_misses(self, sample_request, sample_response):
        c = ResponseCache(enabled=False)
        c.put(sample_request, "deepseek", "deepseek-v4-flash", sample_response)
        assert c.size == 0
        result = c.get(sample_request, "deepseek", "deepseek-v4-flash")
        assert result is None


class TestCacheExclusions:
    def test_code_generation_not_cached(self, cache):
        """CODE_GENERATION should never be cached."""
        assert TaskType.CODE_GENERATION in _NEVER_CACHE
        req = TaskRequest(
            task_id="test-code-001",
            agent_name="programmer-agent",
            task_type=TaskType.CODE_GENERATION,
            prompt="Write a function.",
        )
        resp = LLMResponse(
            task_id=req.task_id,
            success=True,
            provider=ProviderName.CLAUDE,
            model="claude-sonnet-4-6",
            content="def foo(): pass",
        )
        cache.put(req, "claude", "claude-sonnet-4-6", resp)
        result = cache.get(req, "claude", "claude-sonnet-4-6")
        assert result is None

    def test_risk_review_not_cached(self, cache):
        """RISK_REVIEW should never be cached."""
        assert TaskType.RISK_REVIEW in _NEVER_CACHE
        req = TaskRequest(
            task_id="test-risk-001",
            agent_name="risk-agent",
            task_type=TaskType.RISK_REVIEW,
            prompt="Review this strategy risk.",
        )
        resp = LLMResponse(
            task_id=req.task_id,
            success=True,
            provider=ProviderName.CLAUDE,
            model="claude-sonnet-4-6",
            content="Risk acceptable.",
        )
        cache.put(req, "claude", "claude-sonnet-4-6", resp)
        result = cache.get(req, "claude", "claude-sonnet-4-6")
        assert result is None

    def test_debugging_not_cached(self, cache):
        """DEBUGGING should never be cached."""
        assert TaskType.DEBUGGING in _NEVER_CACHE

    def test_code_planning_not_cached(self, cache):
        """CODE_PLANNING should never be cached."""
        assert TaskType.CODE_PLANNING in _NEVER_CACHE

    def test_code_review_not_cached(self, cache):
        """CODE_REVIEW should never be cached."""
        assert TaskType.CODE_REVIEW in _NEVER_CACHE

    def test_no_cache_metadata(self, cache):
        """metadata.no_cache = true should prevent caching."""
        req = TaskRequest(
            task_id="test-nocache-001",
            agent_name="research-agent",
            task_type=TaskType.SUMMARIZATION,
            prompt="Summarize this.",
            metadata={"no_cache": True},
        )
        resp = LLMResponse(
            task_id=req.task_id,
            success=True,
            provider=ProviderName.DEEPSEEK,
            model="deepseek-v4-flash",
            content="Summary.",
        )
        cache.put(req, "deepseek", "deepseek-v4-flash", resp)
        result = cache.get(req, "deepseek", "deepseek-v4-flash")
        assert result is None

    def test_summarization_is_cacheable(self, cache, sample_request, sample_response):
        """SUMMARIZATION should be cacheable."""
        cache.put(sample_request, "deepseek", "deepseek-v4-flash", sample_response)
        assert cache.size == 1
