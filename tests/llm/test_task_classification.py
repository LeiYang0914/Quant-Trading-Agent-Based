"""Tests for task classification heuristics."""

import pytest

from src.llm.prompts.task_classifier import classify_task, infer_complexity
from src.llm.types import TaskType


class TestClassifyTask:
    def test_code_generation_keywords(self):
        assert classify_task("write code for a backtest engine") == TaskType.CODE_GENERATION
        assert classify_task("implement a funding rate signal") == TaskType.CODE_GENERATION
        assert classify_task("build a function to compute Sharpe ratio") == TaskType.CODE_GENERATION
        assert classify_task("create a script to download data") == TaskType.CODE_GENERATION
        assert classify_task("generate code for the API adapter") == TaskType.CODE_GENERATION

    def test_code_planning_keywords(self):
        assert classify_task("plan the code architecture for the backtest") == TaskType.CODE_PLANNING
        assert classify_task("design the implementation of the signal") == TaskType.CODE_PLANNING
        assert classify_task("how should I implement the data loader") == TaskType.CODE_PLANNING

    def test_code_review_keywords(self):
        assert classify_task("review this code for bugs") == TaskType.CODE_REVIEW
        assert classify_task("code review the backtest module") == TaskType.CODE_REVIEW

    def test_debugging_keywords(self):
        assert classify_task("debug the data loader issue") == TaskType.DEBUGGING
        assert classify_task("fix this bug in the signal") == TaskType.DEBUGGING
        assert classify_task("why does this error happen") == TaskType.DEBUGGING

    def test_summarization_keywords(self):
        assert classify_task("summarize this paper") == TaskType.SUMMARIZATION
        assert classify_task("give me a tldr of the article") == TaskType.SUMMARIZATION
        assert classify_task("sum up the findings") == TaskType.SUMMARIZATION

    def test_text_cleanup_keywords(self):
        assert classify_task("format this document") == TaskType.TEXT_CLEANUP
        assert classify_task("clean up this markdown") == TaskType.TEXT_CLEANUP
        assert classify_task("reformat the memo") == TaskType.TEXT_CLEANUP

    def test_git_activity_summary_keywords(self):
        assert classify_task("git log summary for this week") == TaskType.GIT_ACTIVITY_SUMMARY
        assert classify_task("give me a commit summary for the last week") == TaskType.GIT_ACTIVITY_SUMMARY
        assert classify_task("create an activity summary of recent changes") == TaskType.GIT_ACTIVITY_SUMMARY

    def test_memory_update_keywords(self):
        assert classify_task("memory update for the session") == TaskType.MEMORY_UPDATE
        assert classify_task("remember this decision") == TaskType.MEMORY_UPDATE
        assert classify_task("save to memory the project state") == TaskType.MEMORY_UPDATE

    def test_falls_back_to_general_qa(self):
        assert classify_task("hello how are you") == TaskType.GENERAL_QA
        assert classify_task("what is the weather") == TaskType.GENERAL_QA


class TestInferComplexity:
    def test_high_complexity_types(self):
        assert infer_complexity("any text", TaskType.SYSTEM_ARCHITECTURE) == "high"
        assert infer_complexity("any text", TaskType.CODE_GENERATION) == "high"
        assert infer_complexity("any text", TaskType.DEBUGGING) == "high"

    def test_low_complexity_types(self):
        assert infer_complexity("any text", TaskType.SUMMARIZATION) == "low"
        assert infer_complexity("any text", TaskType.TEXT_CLEANUP) == "low"
        assert infer_complexity("any text", TaskType.CLASSIFICATION) == "low"
        assert infer_complexity("any text", TaskType.MEMORY_UPDATE) == "low"

    def test_medium_default(self):
        assert infer_complexity("a routine task", TaskType.GENERAL_QA) == "medium"

    def test_complex_keywords_override(self):
        assert infer_complexity("this is a complex and nuanced problem", TaskType.GENERAL_QA) == "high"

    def test_simple_keywords_override(self):
        assert infer_complexity("this is a simple quick task", TaskType.GENERAL_QA) == "low"

    def test_code_required_implies_high(self):
        assert infer_complexity("do something", TaskType.GENERAL_QA, requires_code=True) == "high"

    def test_long_context_implies_high(self):
        assert infer_complexity("do something", TaskType.GENERAL_QA, long_context=True) == "high"
