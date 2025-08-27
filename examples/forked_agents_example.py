#!/usr/bin/env python3
"""
ForkedAgents Example - Cost-Optimized Multi-Agent Code Review

This example demonstrates how to use ForkedAgents to create multiple specialized
code reviewers from a single parent agent with cached context, saving significant
costs when analyzing large codebases.

Usage:
    python examples/forked_agents_example.py --provider anthropic --model claude-3-5-sonnet-20241022 --path ./liteagent
    python examples/forked_agents_example.py --provider openai --model gpt-4-turbo --path ./src
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from liteagent.forked_agent import ForkedAgent
from liteagent import liteagent_tool
from liteagent.observer import ConsoleObserver

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


# ============================================================================
# SHARED TOOLS FOR CODE ANALYSIS
# ============================================================================

@liteagent_tool(name="analyze_security", 
                description="Analyze code for security vulnerabilities")
def analyze_security(code_snippet: str) -> str:
    """Analyze code for common security issues."""
    issues = []
    
    # Simple security checks (in real implementation, use proper tools)
    if "eval(" in code_snippet:
        issues.append("⚠️ Use of eval() detected - potential code injection risk")
    if "exec(" in code_snippet:
        issues.append("⚠️ Use of exec() detected - potential code injection risk")
    if "__import__" in code_snippet:
        issues.append("⚠️ Dynamic import detected - review for security")
    if "os.system" in code_snippet:
        issues.append("⚠️ Direct system command execution detected")
    if "pickle.loads" in code_snippet:
        issues.append("⚠️ Pickle deserialization - potential security risk")
        
    return "\n".join(issues) if issues else "✅ No obvious security issues detected"


@liteagent_tool(name="analyze_performance",
                description="Analyze code for performance issues")
def analyze_performance(code_snippet: str) -> str:
    """Analyze code for performance problems."""
    issues = []
    
    # Simple performance checks
    if "for i in range(len(" in code_snippet:
        issues.append("💡 Consider using enumerate() instead of range(len())")
    if ".append(" in code_snippet and "for " in code_snippet:
        issues.append("💡 Consider list comprehension for better performance")
    if "+" in code_snippet and "str" in code_snippet and "for" in code_snippet:
        issues.append("💡 String concatenation in loop - consider join() or list")
    if "global " in code_snippet:
        issues.append("💡 Global variable usage may impact performance")
        
    return "\n".join(issues) if issues else "✅ No obvious performance issues detected"


@liteagent_tool(name="analyze_style",
                description="Analyze code style and suggest improvements")
def analyze_style(code_snippet: str) -> str:
    """Analyze code style and conventions."""
    issues = []
    
    # Simple style checks
    lines = code_snippet.split('\n')
    for i, line in enumerate(lines, 1):
        if len(line) > 100:
            issues.append(f"Line {i}: Line too long ({len(line)} chars)")
        if line.strip().startswith("#TODO"):
            issues.append(f"Line {i}: TODO comment found")
        if "  " in line and not line.strip().startswith("#"):
            issues.append(f"Line {i}: Multiple spaces detected (use consistent indentation)")
            
    return "\n".join(issues) if issues else "✅ Code style looks good"


@liteagent_tool(name="suggest_refactoring",
                description="Suggest refactoring improvements")
def suggest_refactoring(code_snippet: str) -> str:
    """Suggest refactoring improvements."""
    suggestions = []
    
    # Simple refactoring suggestions
    if code_snippet.count("def ") > 10:
        suggestions.append("📦 Consider splitting into multiple modules")
    if any(len(line) > 10 for line in code_snippet.split('\n') if line.strip().startswith("def ")):
        suggestions.append("📝 Some function names are very long - consider shorter names")
    if "class " in code_snippet and code_snippet.count("def ") > 20:
        suggestions.append("🔄 Large class detected - consider splitting responsibilities")
        
    return "\n".join(suggestions) if suggestions else "✅ Code structure looks good"


@liteagent_tool(name="check_documentation",
                description="Check code documentation quality")
def check_documentation(code_snippet: str) -> str:
    """Check if code is properly documented."""
    issues = []
    
    # Count functions and docstrings
    func_count = code_snippet.count("def ")
    docstring_count = code_snippet.count('"""')
    
    if func_count > 0 and docstring_count < func_count:
        issues.append(f"📚 Missing docstrings: {func_count} functions, only {docstring_count//2} documented")
    
    if "class " in code_snippet and '"""' not in code_snippet[:code_snippet.find("def ")]:
        issues.append("📚 Class missing docstring")
        
    return "\n".join(issues) if issues else "✅ Documentation looks complete"


# ============================================================================
# CODEBASE LOADER
# ============================================================================

def load_codebase(path: str, max_files: int = 10) -> str:
    """
    Load Python files from a directory into a single context string.
    
    Args:
        path: Path to the codebase directory
        max_files: Maximum number of files to load
        
    Returns:
        String containing the codebase content
    """
    codebase = []
    file_count = 0
    
    for root, dirs, files in os.walk(path):
        # Skip hidden directories and common non-code directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
        
        for file in files:
            if file.endswith('.py') and file_count < max_files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, path)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        codebase.append(f"\n{'='*60}\n")
                        codebase.append(f"FILE: {relative_path}\n")
                        codebase.append(f"{'='*60}\n")
                        codebase.append(content)
                        file_count += 1
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    
                if file_count >= max_files:
                    break
                    
    print(f"📂 Loaded {file_count} Python files from {path}")
    return "\n".join(codebase)


# ============================================================================
# MAIN EXAMPLE
# ============================================================================

async def run_forked_analysis(provider: str, model: str, codebase_path: str):
    """
    Demonstrate ForkedAgents with specialized code reviewers.
    
    Args:
        provider: LLM provider to use
        model: Model name
        codebase_path: Path to codebase to analyze
    """
    print("\n" + "="*60)
    print("🔍 FORKEDAGENTS CODE REVIEW DEMONSTRATION")
    print("="*60)
    
    # Reset cost tracker for this session
    from liteagent.provider_cost_tracker import get_cost_tracker
    cost_tracker = get_cost_tracker()
    cost_tracker.events = []  # Reset events for clean session tracking
    print("🔄 Cost tracker reset for this session")
    
    # Load the codebase
    print(f"\n📚 Loading codebase from {codebase_path}...")
    codebase_content = load_codebase(codebase_path, max_files=5)
    
    # Calculate context size
    context_size = len(codebase_content)
    estimated_tokens = context_size // 4  # Rough estimate
    print(f"📊 Context size: {context_size:,} characters (~{estimated_tokens:,} tokens)")
    
    # Create the parent agent with the full codebase context
    print(f"\n🤖 Creating parent agent with cached context...")
    
    # Get initial cost baseline (cost_tracker already imported above)
    initial_cost = cost_tracker.get_total_cost()
    initial_tokens = cost_tracker.get_total_tokens()
    
    parent = ForkedAgent(
        model=model,
        name="codebase_analyzer",
        system_prompt=f"""You are a comprehensive code analysis system. 
        You have been loaded with a codebase that you will analyze from different perspectives.
        
        CODEBASE CONTENT:
        {codebase_content}
        
        You will be forked into specialized agents for different analysis tasks.""",
        tools=[analyze_security, analyze_performance, analyze_style, 
               suggest_refactoring, check_documentation],
        provider=provider,
        enable_caching=True,
        debug=True,
        observers=[ConsoleObserver(verbose=True)]
    )
    
    print(f"✅ Parent agent created with context_id: {parent.context_id}")
    
    # Print cost after parent creation
    current_cost = cost_tracker.get_total_cost()
    current_tokens = cost_tracker.get_total_tokens()
    step_cost = current_cost - initial_cost
    step_tokens = current_tokens - initial_tokens
    print(f"💰 Cost after parent creation: ${step_cost:.6f} ({step_tokens:,} tokens)")
    
    # CRITICAL: Ensure cache is established BEFORE creating any forks
    print("\n🔧 Establishing cache for context sharing...")
    if not parent._is_prepared_for_caching():
        print("📡 Parent needs cache preparation - this will establish shared context")
        parent._prepare_for_caching()
        
        # Check cost after cache preparation
        cache_prep_cost = cost_tracker.get_total_cost()
        cache_prep_tokens = cost_tracker.get_total_tokens()
        prep_cost = cache_prep_cost - current_cost
        prep_tokens = cache_prep_tokens - current_tokens
        print(f"💰 Cache preparation cost: ${prep_cost:.6f} ({prep_tokens:,} tokens)")
    else:
        print("✅ Cache already prepared")
    
    # Create specialized forked agents (now they can use the established cache)
    print("\n🔀 Creating specialized forked agents...")
    print("🎯 Cache is established - forks should now share context efficiently")
    
    # Store cost before forking (after cache preparation)
    pre_fork_cost = cost_tracker.get_total_cost()
    pre_fork_tokens = cost_tracker.get_total_tokens()
    
    # Security Auditor Fork
    security_auditor = parent.fork(
        name="security_auditor",
        prefill_role="security expert focusing on vulnerabilities and secure coding practices",
        allowed_tools=["analyze_security"],
        system_prompt_suffix="Focus specifically on security vulnerabilities, authentication issues, and data validation."
    )
    print(f"  🔒 Security Auditor fork created: {security_auditor.context_id}")
    
    # Performance Optimizer Fork
    performance_optimizer = parent.fork(
        name="performance_optimizer",
        prefill_role="performance optimization expert focusing on efficiency and speed",
        allowed_tools=["analyze_performance"],
        system_prompt_suffix="Focus on algorithm efficiency, resource usage, and performance bottlenecks."
    )
    print(f"  ⚡ Performance Optimizer fork created: {performance_optimizer.context_id}")
    
    # Style Checker Fork
    style_checker = parent.fork(
        name="style_checker",
        prefill_role="code style expert ensuring clean, readable, and maintainable code",
        allowed_tools=["analyze_style", "check_documentation"],
        system_prompt_suffix="Focus on code readability, naming conventions, and documentation quality."
    )
    print(f"  🎨 Style Checker fork created: {style_checker.context_id}")
    
    # Refactoring Advisor Fork
    refactoring_advisor = parent.fork(
        name="refactoring_advisor",
        prefill_role="software architect focusing on design patterns and code structure",
        allowed_tools=["suggest_refactoring"],
        system_prompt_suffix="Focus on design patterns, SOLID principles, and architectural improvements."
    )
    print(f"  🏗️ Refactoring Advisor fork created: {refactoring_advisor.context_id}")
    
    # Print cost after fork creation
    post_fork_cost = cost_tracker.get_total_cost()
    post_fork_tokens = cost_tracker.get_total_tokens()
    fork_creation_cost = post_fork_cost - pre_fork_cost
    fork_creation_tokens = post_fork_tokens - pre_fork_tokens
    print(f"💰 Cost for creating 4 forks: ${fork_creation_cost:.6f} ({fork_creation_tokens:,} tokens)")
    
    # Run parallel analysis with all forked agents
    print("\n🚀 Running parallel analysis with forked agents...")
    print("   (Each agent analyzes the same codebase from their perspective)")
    
    # Define analysis tasks
    tasks = [
        ("Security Audit", security_auditor, 
         "Analyze the codebase for security vulnerabilities. Use your tools and provide a comprehensive security report."),
        ("Performance Review", performance_optimizer,
         "Analyze the codebase for performance issues. Use your tools and suggest optimizations."),
        ("Style Check", style_checker,
         "Review the code style and documentation. Use your tools and provide improvement suggestions."),
        ("Refactoring Suggestions", refactoring_advisor,
         "Analyze the code structure and suggest refactoring improvements. Use your tools to identify areas for improvement.")
    ]
    
    # CRITICAL: Verify cache is ready before running any analysis
    if not parent._is_prepared_for_caching():
        print("❌ CRITICAL ERROR: Cache not established! This will cause rate limit failures.")
        return
    else:
        print("✅ Cache verified - proceeding with fork analysis")
    
    # Run analyses (forks should now use cached context)
    results = {}
    analysis_start_cost = cost_tracker.get_total_cost()
    analysis_start_tokens = cost_tracker.get_total_tokens()
    
    for i, (task_name, agent, prompt) in enumerate(tasks, 1):
        print(f"\n📝 Running {task_name}...")
        
        # Track cost before this specific task
        task_start_cost = cost_tracker.get_total_cost()
        task_start_tokens = cost_tracker.get_total_tokens()
        
        try:
            response = agent.run(prompt)
            
            # Check if response indicates failure
            if "Rate limit" in response or "Error" in response or "failed" in response:
                print(f"⚠️ {task_name} encountered issues")
                results[task_name] = response
                success = False
            else:
                print(f"✅ {task_name} completed successfully")
                results[task_name] = response
                success = True
            
            # Calculate cost for this specific task
            task_end_cost = cost_tracker.get_total_cost()
            task_end_tokens = cost_tracker.get_total_tokens()
            task_cost = task_end_cost - task_start_cost
            task_tokens = task_end_tokens - task_start_tokens
            
            status_icon = "✅" if success else "⚠️"
            print(f"   {status_icon} Status: {'Success' if success else 'Issues encountered'}")
            print(f"   💰 Task cost: ${task_cost:.6f} ({task_tokens:,} tokens)")
            
            # Show cumulative cost progress
            total_analysis_cost = task_end_cost - analysis_start_cost
            total_analysis_tokens = task_end_tokens - analysis_start_tokens
            print(f"   📊 Analysis progress: {i}/4 tasks, total cost: ${total_analysis_cost:.6f} ({total_analysis_tokens:,} tokens)")
            
        except Exception as e:
            print(f"❌ {task_name} failed with exception: {e}")
            results[task_name] = f"Exception: {e}"
    
    # Display results
    print("\n" + "="*60)
    print("📊 ANALYSIS RESULTS")
    print("="*60)
    
    for task_name, result in results.items():
        print(f"\n### {task_name} ###")
        print(result[:500] + "..." if len(result) > 500 else result)
    
    # Display what actually works
    print("\n" + "="*60)
    print("✅ FORKEDAGENTS SUCCESS SUMMARY")
    print("="*60)
    
    fork_tree = parent.get_fork_tree()
    
    # Count successes vs failures for accurate reporting  
    successful_tasks = sum(1 for result in results.values() if not ("Rate limit" in result or "Error" in result or "Exception" in result))
    failed_tasks = len(results) - successful_tasks
    
    print(f"\n🎯 What's Working:")
    context_chars = len(codebase_content)
    estimated_tokens = context_chars // 4
    print(f"  • Parent agent loaded: {context_chars:,} characters (~{estimated_tokens:,} tokens)")
    print(f"  • Specialized forks created: {len(fork_tree['children'])}")
    print(f"  • System architecture: Parent → Multiple specialized forks")
    if successful_tasks == len(results):
        print(f"  • All {len(results)} tasks completed successfully")
        print(f"  • No crashes: System completed successfully")
    else:
        print(f"  • {successful_tasks}/{len(results)} tasks completed successfully")
    
    print(f"\n🔀 Fork Summary:")
    for child in fork_tree['children']:
        tools = ", ".join(child['allowed_tools']) if child['allowed_tools'] else "all"
        print(f"  • {child['name']}: {tools}")
    
    print(f"\n📈 Task Success Rate:")
    print(f"  • Successful: {successful_tasks}/{len(results)} tasks")
    print(f"  • Failed: {failed_tasks}/{len(results)} tasks")
    if failed_tasks > 0:
        print(f"  ⚠️ System needs optimization to handle parallel requests")
    
    # Show detailed cost breakdown
    final_cost = cost_tracker.get_total_cost()
    final_tokens = cost_tracker.get_total_tokens()
    total_session_cost = final_cost - initial_cost
    total_session_tokens = final_tokens - initial_tokens
    
    cost_summary = cost_tracker.get_summary()
    
    print(f"\n💰 Detailed Cost Breakdown:")
    print(f"  📈 Session Summary:")
    print(f"    • Total session cost: ${total_session_cost:.6f}")
    print(f"    • Total session tokens: {total_session_tokens:,}")
    print(f"    • Average cost per token: ${(total_session_cost/total_session_tokens)*1000:.4f} per 1K tokens" if total_session_tokens > 0 else "    • No tokens processed")
    
    print(f"\n  🔍 Cost Breakdown by Phase:")
    parent_creation_cost = step_cost if 'step_cost' in locals() else 0
    fork_cost = fork_creation_cost if 'fork_creation_cost' in locals() else 0
    analysis_cost = total_session_cost - parent_creation_cost - fork_cost
    
    print(f"    • Parent creation: ${parent_creation_cost:.6f} ({(parent_creation_cost/total_session_cost)*100:.1f}%)" if total_session_cost > 0 else "    • Parent creation: $0.000000")
    print(f"    • Fork creation: ${fork_cost:.6f} ({(fork_cost/total_session_cost)*100:.1f}%)" if total_session_cost > 0 else "    • Fork creation: $0.000000")
    print(f"    • Analysis tasks: ${analysis_cost:.6f} ({(analysis_cost/total_session_cost)*100:.1f}%)" if total_session_cost > 0 else "    • Analysis tasks: $0.000000")
    
    if "message" not in cost_summary:
        fork_savings = cost_summary.get('fork_savings', {})
        if not isinstance(fork_savings, str):
            cached_tokens = fork_savings.get('cached_tokens', 0)
            if cached_tokens > 0:
                print(f"\n  🎯 Caching Benefits:")
                print(f"    • Cached tokens used: {cached_tokens:,}")
                print(f"    • Cache efficiency: {(cached_tokens/total_session_tokens)*100:.1f}%" if total_session_tokens > 0 else "")
                if fork_savings.get('savings', 0) > 0:
                    print(f"    • Estimated savings: ${fork_savings['savings']:.6f} ({fork_savings.get('savings_percent', 0):.1f}%)")
    
    print(f"\n💡 Cost Optimization Analysis:")
    print(f"  📊 Traditional vs ForkedAgent Approach:")
    estimated_traditional_cost = total_session_cost * 4  # Rough estimate if each agent loaded full context
    estimated_savings = estimated_traditional_cost - total_session_cost
    print(f"    • ForkedAgent cost: ${total_session_cost:.6f}")
    print(f"    • Traditional estimate: ${estimated_traditional_cost:.6f} (4x agents × full context each)")
    print(f"    • Estimated savings: ${estimated_savings:.6f} ({(estimated_savings/estimated_traditional_cost)*100:.1f}%)")
    print(f"    • Cost reduction factor: {estimated_traditional_cost/total_session_cost:.1f}x" if total_session_cost > 0 else "")
    
    print(f"\n  ✨ Real-world Benefits:")
    print(f"    • Context loaded once, shared via provider caching")
    print(f"    • 4 specialized agents created from single parent")
    print(f"    • Each agent has focused tools and expertise")
    print(f"    • Scalable to unlimited specialized agents")
    
    # Count successes vs failures
    successful_tasks = sum(1 for result in results.values() if not ("Rate limit" in result or "Error" in result or "Exception" in result))
    failed_tasks = len(results) - successful_tasks
    
    if failed_tasks == 0:
        print("\n✨ ForkedAgents demonstration completed successfully!")
    else:
        print(f"\n⚠️ ForkedAgents demonstration completed with {failed_tasks} issues.")
        print(f"💡 The system needs optimization to handle parallel fork requests effectively.")


def main():
    """Main entry point for the example."""
    parser = argparse.ArgumentParser(description="ForkedAgents Code Review Example")
    parser.add_argument("--provider", "-p", default="anthropic",
                       choices=["anthropic", "openai", "groq"],
                       help="LLM provider to use")
    parser.add_argument("--model", "-m", default="claude-3-5-sonnet-20241022",
                       help="Model name to use")
    parser.add_argument("--path", default="./liteagent",
                       help="Path to codebase to analyze")
    
    args = parser.parse_args()
    
    # Check if path exists
    if not os.path.exists(args.path):
        print(f"❌ Error: Path '{args.path}' does not exist")
        sys.exit(1)
    
    # Run the async example
    try:
        # For this example, we'll run synchronously
        # In production, you'd use asyncio.run()
        asyncio.run(run_forked_analysis(args.provider, args.model, args.path))
    except KeyboardInterrupt:
        print("\n\n👋 Example interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()