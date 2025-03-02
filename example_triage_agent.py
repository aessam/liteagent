"""
Example demonstrating the TriageAgent with nested agents.

This example shows how to create a TriageAgent that dispatches tasks to specialized
resolver and validation agents.
"""
from dotenv import load_dotenv
import os
import argparse
from typing import Dict, List, Any

from liteagent import LiteAgent
from liteagent.agent_tool import AgentTool
from liteagent.observer import ConsoleObserver, FileObserver, TreeTraceObserver

# Mock tools for the example
def crm_search(query: str) -> List[Dict[str, Any]]:
    """
    Search the CRM database for customer information.
    
    Args:
        query: The search query
        
    Returns:
        List of matching customer records
    """
    # Mock implementation
    if "account" in query.lower():
        return [
            {"id": "C12345", "name": "Acme Corp", "status": "Active", "plan": "Enterprise"},
            {"id": "C67890", "name": "Globex Inc", "status": "Active", "plan": "Professional"}
        ]
    elif "billing" in query.lower():
        return [
            {"id": "B12345", "customer_id": "C12345", "amount": 1500, "status": "Paid", "date": "2023-05-15"},
            {"id": "B67890", "customer_id": "C67890", "amount": 750, "status": "Pending", "date": "2023-06-01"}
        ]
    else:
        return []

def support_directory(department: str) -> Dict[str, str]:
    """
    Get contact information for a support department.
    
    Args:
        department: The department name
        
    Returns:
        Contact information for the department
    """
    # Mock implementation
    directories = {
        "billing": {"email": "billing@example.com", "phone": "555-123-4567", "hours": "9am-5pm EST"},
        "technical": {"email": "support@example.com", "phone": "555-987-6543", "hours": "24/7"},
        "sales": {"email": "sales@example.com", "phone": "555-567-8901", "hours": "8am-6pm EST"}
    }
    return directories.get(department.lower(), {"message": "Department not found"})

def validate_solution(problem: str, solution: str) -> Dict[str, Any]:
    """
    Validate if a solution addresses the customer's problem.
    
    Args:
        problem: The customer's problem
        solution: The proposed solution
        
    Returns:
        Validation result
    """
    # Mock implementation - in a real system, this would have actual validation logic
    return {
        "valid": True,
        "confidence": 0.85,
        "feedback": "Solution addresses the core issue and provides clear next steps."
    }

def main():
    parser = argparse.ArgumentParser(description="Run the TriageAgent example")
    parser.add_argument("--model", default="gpt-4o-mini", help="Model to use")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--enable-observability", action="store_true", help="Enable observability features")
    args = parser.parse_args()
    
    # Check for API keys
    if not os.environ.get("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not found in environment variables")
    
    # Set up observers if enabled
    observers = []
    if args.enable_observability:
        observers.append(ConsoleObserver())
        observers.append(FileObserver("triage_agent_events.jsonl"))
        observers.append(TreeTraceObserver())
    # Create the resolver agent
    resolver_agent = LiteAgent(
        model=args.model,
        name="ResolverAgent",
        system_prompt="""You are a specialized agent that resolves customer support issues.
Your goal is to provide clear, accurate solutions to customer problems.
Use the provided tools to gather information and craft a comprehensive solution.
Be specific and provide step-by-step instructions when appropriate.""",
        tools=[crm_search, support_directory],
        debug=args.debug,
        observers=observers
    )
    
    # Create the validation agent
    validation_agent = LiteAgent(
        model=args.model,
        name="ValidationAgent",
        system_prompt="""You are a specialized agent that validates solutions to customer problems.
Your goal is to ensure that solutions are accurate, complete, and address the customer's core issue.
Evaluate the solution against the original problem and provide feedback.""",
        tools=[validate_solution],
        debug=args.debug,
        observers=observers
    )
    
    # Create agent tools from the resolver and validation agents with message templates
    resolver_tool = AgentTool(
        resolver_agent, 
        "resolve_issue", 
        "Resolve a customer support issue by providing a comprehensive solution",
        message_template="{message}"
    )
    
    validation_tool = AgentTool(
        validation_agent, 
        "validate_solution", 
        "Validate if a solution properly addresses the customer's problem",
        message_template="Please evaluate if the following solution effectively addresses the customer's problem:\n\nProblem: {problem}\n\nSolution: {solution}"
    )
    
    # Create the triage agent
    triage_agent = LiteAgent(
        model=args.model,
        name="TriageAgent",
        system_prompt="""You are a triage agent for customer support.
Your job is to analyze customer problems and dispatch them to the appropriate specialized agents.
For technical or account-related issues, use the resolve_issue tool with the 'message' parameter containing the customer's exact question.
Then use the validate_solution tool with 'problem' and 'solution' parameters to ensure the solution is appropriate.
Always provide a final response to the customer that includes the validated solution.""",
        tools=[crm_search, support_directory, resolver_tool, validation_tool],
        debug=args.debug,
        observers=observers
    )
    
    # Example customer problems
    problems = [
        "I can't access my account. I keep getting an error message when I try to log in.",
        "I was charged twice for my subscription this month. Can you help me get a refund?",
        "How do I upgrade my plan from Professional to Enterprise?"
    ]
    
    # Process each problem
    for i, problem in enumerate(problems):
        print(f"\n--- Problem {i+1} ---")
        print(f"Customer: {problem}")
        
        # Get response from the triage agent
        response = triage_agent.chat(problem)
        
        print(f"TriageAgent: {response}")
        print("-" * 50)
    if args.enable_observability:
        for observer in observers:
            if isinstance(observer, TreeTraceObserver):
                observer.print_trace()
    
if __name__ == "__main__":
    load_dotenv()
    main() 