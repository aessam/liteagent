"""
Tool-call enforcement mechanism for ensuring reliable LLM behavior.

This module provides utilities to enforce tool usage when required,
preventing LLMs from bypassing tools and providing unreliable answers.
"""

import re
import json
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass
from enum import Enum
import logging


class EnforcementLevel(Enum):
    """Levels of tool-call enforcement."""
    NONE = "none"
    WARN = "warn"
    REQUIRE = "require"
    FORCE = "force"


@dataclass
class ToolRequirement:
    """Defines when and how a tool must be used."""
    tool_name: str
    required_patterns: List[str]  # Regex patterns that trigger requirement
    enforcement_level: EnforcementLevel
    error_message: str
    fallback_action: Optional[str] = None


class ToolCallEnforcer:
    """Enforces tool usage based on defined requirements."""
    
    def __init__(self):
        self.requirements: List[ToolRequirement] = []
        self.violation_history: List[Dict[str, Any]] = []
        self.logger = logging.getLogger(__name__)
        
        # Default requirements for common scenarios
        self._setup_default_requirements()
    
    def _setup_default_requirements(self):
        """Setup default tool usage requirements."""
        self.requirements = [
            ToolRequirement(
                tool_name="get_weather",
                required_patterns=[
                    r"weather.*in\s+\w+",
                    r"what.*weather",
                    r"temperature.*in\s+\w+",
                    r"forecast.*for\s+\w+"
                ],
                enforcement_level=EnforcementLevel.REQUIRE,
                error_message="Weather queries must use the get_weather tool"
            ),
            ToolRequirement(
                tool_name="add_numbers",
                required_patterns=[
                    r"\d+\s*\+\s*\d+",
                    r"add\s+\d+.*\d+",
                    r"sum.*\d+.*\d+",
                    r"calculate.*\d+.*plus.*\d+"
                ],
                enforcement_level=EnforcementLevel.REQUIRE,
                error_message="Addition calculations must use the add_numbers tool"
            ),
            ToolRequirement(
                tool_name="multiply_numbers",
                required_patterns=[
                    r"\d+\s*\*\s*\d+",
                    r"\d+\s*×\s*\d+",
                    r"multiply.*\d+.*\d+",
                    r"\d+.*times.*\d+"
                ],
                enforcement_level=EnforcementLevel.REQUIRE,
                error_message="Multiplication calculations must use the multiply_numbers tool"
            ),
            ToolRequirement(
                tool_name="calculate_square_root",
                required_patterns=[
                    r"square\s+root.*\d+",
                    r"sqrt.*\d+",
                    r"√.*\d+",
                    r"what.*square.*root"
                ],
                enforcement_level=EnforcementLevel.FORCE,
                error_message="Square root calculations must use the calculate_square_root tool"
            ),
            ToolRequirement(
                tool_name="get_user_data",
                required_patterns=[
                    r"user\s+user\d+",
                    r"information.*user\d+",
                    r"data.*for.*user\d+",
                    r"get.*user.*\d+"
                ],
                enforcement_level=EnforcementLevel.REQUIRE,
                error_message="User data queries must use the get_user_data tool"
            )
        ]
    
    def add_requirement(self, requirement: ToolRequirement):
        """Add a new tool usage requirement."""
        self.requirements.append(requirement)
    
    def check_message_requirements(self, message: str, available_tools: List[str]) -> List[str]:
        """
        Check if a message requires specific tools to be used.
        
        Returns list of required tool names.
        """
        required_tools = []
        
        message_lower = message.lower()
        
        for requirement in self.requirements:
            # Skip if tool is not available
            if requirement.tool_name not in available_tools:
                continue
            
            # Check if any pattern matches
            for pattern in requirement.required_patterns:
                if re.search(pattern, message_lower, re.IGNORECASE):
                    required_tools.append(requirement.tool_name)
                    break
        
        return list(set(required_tools))  # Remove duplicates
    
    def validate_response(self, 
                         message: str,
                         response: str,
                         tools_called: List[str],
                         available_tools: List[str]) -> Dict[str, Any]:
        """
        Validate that required tools were used in the response.
        
        Returns validation result with violations and recommendations.
        """
        required_tools = self.check_message_requirements(message, available_tools)
        violations = []
        warnings = []
        
        for required_tool in required_tools:
            requirement = next(
                (req for req in self.requirements if req.tool_name == required_tool),
                None
            )
            
            if not requirement:
                continue
            
            tool_was_called = required_tool in tools_called
            
            if not tool_was_called:
                violation = {
                    "tool": required_tool,
                    "requirement": requirement,
                    "message": message,
                    "enforcement_level": requirement.enforcement_level,
                    "error_message": requirement.error_message
                }
                
                if requirement.enforcement_level in [EnforcementLevel.REQUIRE, EnforcementLevel.FORCE]:
                    violations.append(violation)
                    self.violation_history.append(violation)
                elif requirement.enforcement_level == EnforcementLevel.WARN:
                    warnings.append(violation)
        
        return {
            "valid": len(violations) == 0,
            "violations": violations,
            "warnings": warnings,
            "required_tools": required_tools,
            "tools_called": tools_called,
            "message": message
        }
    
    def create_enforced_system_prompt(self, 
                                    base_prompt: str,
                                    available_tools: List[str]) -> str:
        """
        Create a system prompt with embedded tool enforcement rules.
        """
        enforcement_rules = []
        
        for requirement in self.requirements:
            if requirement.tool_name in available_tools:
                patterns_str = " or ".join([f'"{p}"' for p in requirement.required_patterns[:3]])
                
                rule = f"""
- {requirement.tool_name.upper()}: MANDATORY for queries matching patterns like {patterns_str}
  → Enforcement: {requirement.enforcement_level.value.upper()}
  → {requirement.error_message}"""
                
                enforcement_rules.append(rule)
        
        if not enforcement_rules:
            return base_prompt
        
        enforcement_section = f"""
CRITICAL TOOL ENFORCEMENT RULES:
You MUST follow these tool usage requirements:
{''.join(enforcement_rules)}

FAILURE TO USE REQUIRED TOOLS WILL RESULT IN RESPONSE REJECTION.
When in doubt, use the tool rather than attempting to answer without it.
"""
        
        return base_prompt + enforcement_section
    
    def create_validation_prompt_modifier(self, 
                                        original_message: str,
                                        available_tools: List[str]) -> str:
        """
        Create a prompt modifier that emphasizes required tools.
        """
        required_tools = self.check_message_requirements(original_message, available_tools)
        
        if not required_tools:
            return original_message
        
        tool_emphasis = []
        for tool in required_tools:
            requirement = next(
                (req for req in self.requirements if req.tool_name == tool),
                None
            )
            if requirement and requirement.enforcement_level == EnforcementLevel.FORCE:
                tool_emphasis.append(f"CRITICAL: You MUST use {tool} for this request.")
        
        if tool_emphasis:
            emphasis_text = "\n".join(tool_emphasis)
            return f"{original_message}\n\n{emphasis_text}"
        
        return original_message
    
    def get_enforcement_statistics(self) -> Dict[str, Any]:
        """Get statistics about enforcement violations."""
        if not self.violation_history:
            return {
                "total_violations": 0,
                "violations_by_tool": {},
                "violations_by_enforcement_level": {}
            }
        
        tool_violations = {}
        level_violations = {}
        
        for violation in self.violation_history:
            tool = violation["tool"]
            level = violation["enforcement_level"].value
            
            tool_violations[tool] = tool_violations.get(tool, 0) + 1
            level_violations[level] = level_violations.get(level, 0) + 1
        
        return {
            "total_violations": len(self.violation_history),
            "violations_by_tool": tool_violations,
            "violations_by_enforcement_level": level_violations,
            "most_violated_tool": max(tool_violations.items(), key=lambda x: x[1])[0] if tool_violations else None
        }
    
    def clear_violation_history(self):
        """Clear the violation history."""
        self.violation_history.clear()


class EnforcementTestSuite:
    """Test suite for validating tool enforcement mechanisms."""
    
    def __init__(self, enforcer: ToolCallEnforcer):
        self.enforcer = enforcer
    
    def test_pattern_recognition(self) -> Dict[str, Any]:
        """Test that patterns correctly identify tool requirements."""
        test_cases = [
            {
                "message": "What's the weather in Tokyo?",
                "expected_tools": ["get_weather"],
                "available_tools": ["get_weather", "add_numbers"]
            },
            {
                "message": "Calculate 123 + 456",
                "expected_tools": ["add_numbers"],
                "available_tools": ["get_weather", "add_numbers"]
            },
            {
                "message": "What is the square root of 789456123?",
                "expected_tools": ["calculate_square_root"],
                "available_tools": ["calculate_square_root", "add_numbers"]
            },
            {
                "message": "Get information for user123",
                "expected_tools": ["get_user_data"],
                "available_tools": ["get_user_data", "get_weather"]
            },
            {
                "message": "Hello, how are you?",
                "expected_tools": [],
                "available_tools": ["get_weather", "add_numbers"]
            }
        ]
        
        results = []
        passed = 0
        
        for case in test_cases:
            required_tools = self.enforcer.check_message_requirements(
                case["message"], 
                case["available_tools"]
            )
            
            success = set(required_tools) == set(case["expected_tools"])
            if success:
                passed += 1
            
            results.append({
                "message": case["message"],
                "expected": case["expected_tools"],
                "actual": required_tools,
                "success": success
            })
        
        return {
            "total_tests": len(test_cases),
            "passed": passed,
            "failed": len(test_cases) - passed,
            "pass_rate": (passed / len(test_cases)) * 100,
            "detailed_results": results
        }
    
    def test_validation_logic(self) -> Dict[str, Any]:
        """Test response validation logic."""
        test_cases = [
            {
                "message": "What's the weather in Paris?",
                "tools_called": ["get_weather"],
                "available_tools": ["get_weather"],
                "should_pass": True
            },
            {
                "message": "What's the weather in Paris?", 
                "tools_called": [],
                "available_tools": ["get_weather"],
                "should_pass": False
            },
            {
                "message": "Calculate 7 + 9",
                "tools_called": ["add_numbers"],
                "available_tools": ["add_numbers"],
                "should_pass": True
            },
            {
                "message": "Calculate 7 + 9",
                "tools_called": [],
                "available_tools": ["add_numbers"],
                "should_pass": False
            }
        ]
        
        results = []
        passed = 0
        
        for case in test_cases:
            validation = self.enforcer.validate_response(
                case["message"],
                "dummy response",
                case["tools_called"],
                case["available_tools"]
            )
            
            success = validation["valid"] == case["should_pass"]
            if success:
                passed += 1
            
            results.append({
                "message": case["message"],
                "tools_called": case["tools_called"],
                "expected_valid": case["should_pass"],
                "actual_valid": validation["valid"],
                "success": success,
                "violations": len(validation["violations"])
            })
        
        return {
            "total_tests": len(test_cases),
            "passed": passed,
            "failed": len(test_cases) - passed,
            "pass_rate": (passed / len(test_cases)) * 100,
            "detailed_results": results
        }
    
    def test_prompt_enhancement(self) -> Dict[str, Any]:
        """Test that prompts are properly enhanced with enforcement rules."""
        base_prompt = "You are a helpful assistant."
        available_tools = ["get_weather", "add_numbers", "calculate_square_root"]
        
        enhanced_prompt = self.enforcer.create_enforced_system_prompt(
            base_prompt, 
            available_tools
        )
        
        # Check that enforcement rules were added
        has_enforcement = "CRITICAL TOOL ENFORCEMENT RULES" in enhanced_prompt
        has_mandatory_rules = "MANDATORY" in enhanced_prompt
        has_tool_names = all(tool.upper() in enhanced_prompt for tool in available_tools)
        
        return {
            "base_prompt_length": len(base_prompt),
            "enhanced_prompt_length": len(enhanced_prompt),
            "enhancement_added": len(enhanced_prompt) > len(base_prompt),
            "has_enforcement_section": has_enforcement,
            "has_mandatory_rules": has_mandatory_rules,
            "has_all_tool_names": has_tool_names,
            "success": has_enforcement and has_mandatory_rules and has_tool_names
        }
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all enforcement tests."""
        print("Running tool enforcement tests...")
        
        results = {
            "pattern_recognition": self.test_pattern_recognition(),
            "validation_logic": self.test_validation_logic(),
            "prompt_enhancement": self.test_prompt_enhancement()
        }
        
        # Calculate overall statistics
        total_tests = sum(r.get("total_tests", 1) for r in results.values())
        total_passed = sum(r.get("passed", 1 if r.get("success", False) else 0) for r in results.values())
        
        results["summary"] = {
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_tests - total_passed,
            "overall_pass_rate": (total_passed / total_tests) * 100 if total_tests > 0 else 0
        }
        
        return results


# Global enforcer instance
global_tool_enforcer = ToolCallEnforcer()


def run_enforcement_tests():
    """Run tool enforcement validation tests."""
    print("=" * 60)
    print("TOOL CALL ENFORCEMENT TESTING")
    print("=" * 60)
    
    test_suite = EnforcementTestSuite(global_tool_enforcer)
    results = test_suite.run_all_tests()
    
    print("\nTEST RESULTS:")
    print("=" * 60)
    
    summary = results["summary"]
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Passed: {summary['total_passed']}")
    print(f"Failed: {summary['total_failed']}")
    print(f"Pass Rate: {summary['overall_pass_rate']:.1f}%")
    
    print("\nDETAILED RESULTS:")
    for test_name, test_result in results.items():
        if test_name == "summary":
            continue
            
        print(f"\n{test_name.replace('_', ' ').title()}:")
        if "pass_rate" in test_result:
            print(f"  Pass Rate: {test_result['pass_rate']:.1f}%")
        elif "success" in test_result:
            print(f"  Success: {'✓' if test_result['success'] else '✗'}")
    
    # Show enforcement statistics
    stats = global_tool_enforcer.get_enforcement_statistics()
    if stats["total_violations"] > 0:
        print(f"\nENFORCEMENT VIOLATIONS: {stats['total_violations']}")
        print("Violations by tool:")
        for tool, count in stats["violations_by_tool"].items():
            print(f"  {tool}: {count}")
    
    return results


if __name__ == "__main__":
    run_enforcement_tests()