#!/usr/bin/env python
"""LLM Router CLI — test routing, run health checks, view usage, manage cache.

Usage:
  python scripts/llm_router_cli.py --dry-run --agent research-agent --task paper_analysis --prompt "Analyze this..."
  python scripts/llm_router_cli.py --health-check
  python scripts/llm_router_cli.py --usage-summary
  python scripts/llm_router_cli.py --clear-cache
  python scripts/llm_router_cli.py --clear-usage
  python scripts/llm_router_cli.py --reset-circuits
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Ensure the project root is on the path
_project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_project_root))

from src.llm import (
    Complexity,
    Domain,
    LLMRouter,
    ProviderName,
    TaskRequest,
    TaskType,
)


def _parse_task_type(value: str) -> TaskType:
    try:
        return TaskType[value.upper()]
    except KeyError:
        valid = [t.name for t in TaskType]
        print(f"Invalid task type: {value}")
        print(f"Valid types: {', '.join(valid)}")
        sys.exit(1)


def _parse_complexity(value: str) -> Complexity:
    try:
        return Complexity[value.upper()]
    except KeyError:
        valid = [c.name for c in Complexity]
        print(f"Invalid complexity: {value}")
        print(f"Valid: {', '.join(valid)}")
        sys.exit(1)


def _parse_domain(value: str) -> Domain:
    try:
        return Domain[value.upper()]
    except KeyError:
        valid = [d.name for d in Domain]
        print(f"Invalid domain: {value}")
        print(f"Valid: {', '.join(valid)}")
        sys.exit(1)


def _parse_provider(value: str) -> ProviderName:
    try:
        return ProviderName[value.upper()]
    except KeyError:
        valid = [p.name for p in ProviderName]
        print(f"Invalid provider: {value}")
        print(f"Valid: {', '.join(valid)}")
        sys.exit(1)


def cmd_health_check(router: LLMRouter) -> None:
    """Run health check and print results."""
    result = router.health_check()
    print(json.dumps(result, indent=2, default=str))


def cmd_usage_summary(router: LLMRouter) -> None:
    """Print usage summary."""
    summary = router.get_usage_summary()
    print(json.dumps(summary, indent=2, default=str))


def cmd_clear_cache(router: LLMRouter) -> None:
    """Clear the response cache."""
    count = router.clear_cache()
    print(f"Cache cleared: {count} entries removed")


def cmd_clear_usage(router: LLMRouter) -> None:
    """Clear usage records."""
    count = router.clear_usage()
    print(f"Usage cleared: {count} entries removed")


def cmd_reset_circuits(router: LLMRouter) -> None:
    """Reset all circuit breakers."""
    router.reset_circuits()
    router.reset_rate_limiters()
    print("Circuits and rate limiters reset")


def cmd_route(args: argparse.Namespace) -> None:
    """Route a task and print the result."""
    dry_run = not args.real
    router = LLMRouter(dry_run=dry_run)

    task_type = _parse_task_type(args.task) if args.task else None

    # Build metadata
    metadata = {}
    if args.no_cache:
        metadata["no_cache"] = True

    if task_type and args.prompt:
        request = TaskRequest(
            task_id=args.task_id or f"cli-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            agent_name=args.agent,
            task_type=task_type,
            prompt=args.prompt,
            domain=_parse_domain(args.domain) if args.domain else Domain.SYSTEM,
            complexity=_parse_complexity(args.complexity) if args.complexity else Complexity.MEDIUM,
            requires_code=args.requires_code,
            requires_long_context=args.long_context,
            cost_sensitive=args.cost_sensitive,
            timeout_seconds=args.timeout,
            preferred_provider=_parse_provider(args.provider) if args.provider else None,
            fallback_allowed=not args.no_fallback,
            metadata=metadata,
        )
        response = router.route(request)
    elif args.prompt:
        response = router.ask(
            prompt=args.prompt,
            agent_name=args.agent,
            task_type=task_type,
            domain=_parse_domain(args.domain) if args.domain else None,
            complexity=_parse_complexity(args.complexity) if args.complexity else None,
            metadata=metadata,
            requires_code=args.requires_code,
            requires_long_context=args.long_context,
            cost_sensitive=args.cost_sensitive,
            timeout_seconds=args.timeout,
            preferred_provider=_parse_provider(args.provider) if args.provider else None,
            fallback_allowed=not args.no_fallback,
        )
    else:
        print("Error: --prompt is required for routing")
        sys.exit(1)

    result = {
        "task_id": response.task_id,
        "success": response.success,
        "provider": response.provider.value,
        "model": response.model,
        "content": (response.content[:500] + "..." if response.content and len(response.content) > 500 else response.content),
        "error": response.error,
        "fallback_used": response.fallback_used,
        "cache_hit": response.cache_hit,
        "rate_limited": response.rate_limited,
        "latency_ms": response.latency_ms,
        "latency_seconds": response.latency_seconds,
        "input_tokens": response.input_tokens,
        "output_tokens": response.output_tokens,
        "estimated_tokens": response.estimated_tokens,
        "estimated_cost": response.estimated_cost,
        "routing_reason": response.routing_decision.reason if response.routing_decision else None,
    }
    print(json.dumps(result, indent=2, default=str))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="LLM Router CLI — test routing, health, usage, and cache management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/llm_router_cli.py --dry-run --agent research-agent --task paper_analysis --prompt "Analyze this paper..."
  python scripts/llm_router_cli.py --real --agent programmer-agent --task code_generation --prompt "Write a function..."
  python scripts/llm_router_cli.py --health-check
  python scripts/llm_router_cli.py --usage-summary
  python scripts/llm_router_cli.py --clear-cache
""",
    )

    # Operation mode
    op_group = parser.add_argument_group("Operation")
    op_group.add_argument("--dry-run", action="store_true", default=True, help="Dry run (no real API call, default)")
    op_group.add_argument("--real", action="store_true", help="Make real API calls (requires API keys)")
    op_group.add_argument("--health-check", action="store_true", help="Run provider health checks")
    op_group.add_argument("--usage-summary", action="store_true", help="Show usage and cost summary")
    op_group.add_argument("--clear-cache", action="store_true", help="Clear the response cache")
    op_group.add_argument("--clear-usage", action="store_true", help="Clear usage records")
    op_group.add_argument("--reset-circuits", action="store_true", help="Reset circuit breakers and rate limiters")

    # Task parameters
    task_group = parser.add_argument_group("Task")
    task_group.add_argument("--agent", default="unknown", help="Agent name (e.g. research-agent)")
    task_group.add_argument("--task", help="Task type (e.g. PAPER_ANALYSIS)")
    task_group.add_argument("--prompt", help="Prompt text")
    task_group.add_argument("--task-id", help="Custom task ID")
    task_group.add_argument("--domain", help="Domain: crypto, commodities, cross_market, system")
    task_group.add_argument("--complexity", help="Complexity: low, medium, high")
    task_group.add_argument("--requires-code", action="store_true", help="Task requires code")
    task_group.add_argument("--long-context", action="store_true", help="Task requires long context")
    task_group.add_argument("--cost-sensitive", action="store_true", help="Task is cost sensitive")
    task_group.add_argument("--timeout", type=int, default=120, help="Timeout in seconds")
    task_group.add_argument("--provider", help="Preferred provider: claude, deepseek")
    task_group.add_argument("--no-fallback", action="store_true", help="Disable fallback")
    task_group.add_argument("--no-cache", action="store_true", help="Bypass cache for this request")

    args = parser.parse_args()

    # Determine operation
    operations = []
    if args.health_check:
        operations.append("health_check")
    if args.usage_summary:
        operations.append("usage_summary")
    if args.clear_cache:
        operations.append("clear_cache")
    if args.clear_usage:
        operations.append("clear_usage")
    if args.reset_circuits:
        operations.append("reset_circuits")
    if args.prompt:
        operations.append("route")

    if not operations:
        parser.print_help()
        sys.exit(0)

    dry_run = not args.real
    router = LLMRouter(dry_run=dry_run)

    for op in operations:
        if op == "health_check":
            cmd_health_check(router)
        elif op == "usage_summary":
            cmd_usage_summary(router)
        elif op == "clear_cache":
            cmd_clear_cache(router)
        elif op == "clear_usage":
            cmd_clear_usage(router)
        elif op == "reset_circuits":
            cmd_reset_circuits(router)
        elif op == "route":
            cmd_route(args)


if __name__ == "__main__":
    main()
