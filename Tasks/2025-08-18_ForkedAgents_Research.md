# Task: ForkedAgents - Cost-Optimized Multi-Agent System with Caching

**Date Created**: 2025-08-18 17:56:40  
**Type**: Research & Feature Development  
**Priority**: High  
**Complexity**: High  

## Overview
Implement a forking mechanism for LiteAgent that leverages provider caching capabilities to optimize costs when deploying multiple specialized agents with shared large contexts (e.g., 30K+ token codebases).

## Background

### Problem Statement
Current multi-agent systems require sending the full context to each agent separately, resulting in:
- **5x cost** for 5 agents with the same 30K context
- **Increased latency** from repeated context processing
- **Token limit pressure** when context windows approach limits
- **Inefficient resource utilization** for parallel analysis tasks

### Proposed Solution: ForkedAgents
A forking mechanism that:
1. Loads large context once into a parent agent
2. Creates lightweight forked child agents that inherit the cached context
3. Specializes each fork through prefilling techniques
4. Constrains tool access per fork for focused functionality

### Key Innovation: Prefilling for Role Definition
Instead of role definition in system prompts (which break caching), use prefilled conversation:
```
System: "Your role will be defined by the user" + [30K codebase]
Fork 1 Prefill:
  User: "You are an expert security auditor..."
  Assistant: "I understand. As a security auditor, I will..."
Fork 2 Prefill:
  User: "You are a performance optimizer..."
  Assistant: "Understood. As a performance optimizer, I will..."
```

## Technical Details

### Affected Components

#### Core Components
- **liteagent/agent.py**: Add forking capability to base agent
  - New `fork()` method for creating child agents
  - Cache management for shared context
  - Fork lifecycle management
  
- **liteagent/memory.py**: Implement copy-on-write memory forking
  - `fork_memory()` method for efficient memory duplication
  - Prefill message injection
  - Cache key generation
  
- **liteagent/providers/**: Enhance caching support
  - Extend beyond Anthropic if possible
  - Cache hit/miss tracking
  - Cost calculation APIs

#### New Components
- **liteagent/forked_agent.py**: Main ForkedAgent implementation
  - Fork creation and management
  - Tool subsetting
  - Role specialization via prefilling
  
- **liteagent/prefill.py**: Prefill message management
  - Template system for role definitions
  - Conversation simulation
  - Validation of prefilled roles

### Implementation Approach

#### Phase 1: Core Infrastructure (Week 1)
1. Create `ForkedAgent` class extending `LiteAgent`
2. Implement basic `fork()` method
3. Add memory inheritance mechanism
4. Create prefill injection system

#### Phase 2: Optimization Features (Week 2)
1. Implement tool subsetting (`allowed_tools` parameter)
2. Add cache tracking and metrics
3. Create cost comparison utilities
4. Optimize for different providers

#### Phase 3: Integration & Testing (Week 3)
1. Observer system integration (ForkEvent)
2. Comprehensive unit tests
3. Integration tests with real providers
4. Performance benchmarking

#### Phase 4: Documentation & Examples (Week 4)
1. Create example applications
2. Write usage documentation
3. Performance comparison reports
4. Best practices guide

### Edge Cases

1. **Cache Invalidation**: 
   - Handle provider cache timeouts (typically 5 minutes for Anthropic)
   - Implement cache refresh strategy
   - Fallback to non-cached operation

2. **Memory Limits**:
   - Handle fork count limits (memory pressure)
   - Implement fork pooling/recycling
   - Graceful degradation when caching unavailable

3. **Provider Differences**:
   - Anthropic: Full caching support with cache_control
   - OpenAI: Limited caching, may need alternative approach
   - Others: Fallback to non-optimized forking

4. **Circular Dependencies**:
   - Prevent forks from forking themselves
   - Manage parent-child reference cycles
   - Clean shutdown of fork trees

5. **Tool Conflicts**:
   - Handle overlapping tool names in subsets
   - Validate tool availability before fork creation
   - Error handling for missing tools

6. **State Consistency**:
   - Ensure prefilled state doesn't conflict with actual usage
   - Handle role drift during long conversations
   - Maintain consistency across fork restarts

## Acceptance Criteria

### Functional Requirements
- [ ] Parent agent can create multiple forked children
- [ ] Forked agents inherit cached context without re-sending
- [ ] Each fork can have specialized role via prefilling
- [ ] Tool subsets work correctly per fork
- [ ] Cache hit rate > 80% for forked agents
- [ ] Cost reduction of 60-80% for 5-agent scenario

### Performance Requirements
- [ ] Fork creation < 100ms
- [ ] Memory overhead per fork < 1MB (excluding cached content)
- [ ] Support minimum 10 concurrent forks
- [ ] No performance degradation vs regular agents

### Testing Requirements
- [ ] Unit tests with 90%+ coverage
- [ ] Integration tests with Anthropic provider
- [ ] Cost comparison benchmarks
- [ ] Memory leak tests for fork lifecycle
- [ ] Edge case handling validation

### Documentation Requirements
- [ ] API documentation for ForkedAgent
- [ ] Usage examples for common scenarios
- [ ] Performance/cost comparison reports
- [ ] Migration guide from regular multi-agent

## Dependencies

### External Dependencies
- Anthropic SDK with caching support (already present)
- Provider APIs with cache capabilities

### Internal Dependencies
- Existing agent infrastructure
- Memory management system
- Observer/event system
- Provider abstraction layer

## Complexity Indicators

### Scope
- [x] Cross-module changes (5+)
- [x] Architecture changes
- [ ] Single file change
- [ ] Multiple files (2-5)

### Technical Complexity
- [x] Complex state management
- [x] Performance optimization needed
- [x] Requires learning new APIs/patterns
- [ ] Straightforward implementation

### Testing Requirements
- [x] Unit tests only
- [x] Integration tests needed
- [x] E2E tests required
- [x] Manual QA needed

### Coordination
- [x] Self-contained
- [ ] Needs design review
- [ ] Requires API changes
- [ ] Database migration
- [ ] Depends on other teams

## Use Case Examples

### Example 1: Codebase Analysis
```python
# Load 30K token codebase once
parent = ForkedAgent(
    model="claude-3-5-sonnet-20241022",
    context=load_codebase(),
    enable_caching=True
)

# Create specialized reviewers (minimal cost)
security_auditor = parent.fork(
    prefill_role="security expert",
    allowed_tools=["scan_vulnerabilities", "check_dependencies"]
)

performance_reviewer = parent.fork(
    prefill_role="performance optimizer", 
    allowed_tools=["profile_code", "suggest_optimizations"]
)

style_checker = parent.fork(
    prefill_role="code style expert",
    allowed_tools=["check_style", "suggest_refactoring"]
)

# Each fork operates on cached context
results = await asyncio.gather(
    security_auditor.analyze(),
    performance_reviewer.analyze(),
    style_checker.analyze()
)
```

### Example 2: Document Processing
```python
# Load large document once
parent = ForkedAgent(
    model="claude-3-5-sonnet-20241022",
    context=load_document("war_and_peace.txt"),
    enable_caching=True
)

# Create specialized analyzers
summarizer = parent.fork(prefill_role="summarization expert")
critic = parent.fork(prefill_role="literary critic")
translator = parent.fork(prefill_role="translator to Spanish")
fact_checker = parent.fork(prefill_role="historical fact checker")

# Process in parallel with ~80% cost savings
```

## Implementation Priority

1. **High Priority**:
   - Basic forking mechanism
   - Memory inheritance
   - Anthropic caching integration
   - Cost tracking

2. **Medium Priority**:
   - Tool subsetting
   - Prefill templates
   - Observer integration
   - Multi-provider support

3. **Low Priority**:
   - Fork pooling
   - Advanced metrics
   - UI visualization
   - Cross-provider optimization

## Success Metrics

1. **Cost Reduction**: 60-80% for multi-agent scenarios
2. **Performance**: <10% overhead vs single agent
3. **Adoption**: Used in 3+ example applications
4. **Reliability**: 99%+ success rate in tests
5. **Developer Experience**: Clear API, good documentation

## Risks & Mitigation

### Risk 1: Provider Caching Limitations
- **Risk**: Not all providers support caching
- **Mitigation**: Implement fallback to regular agents, document provider capabilities

### Risk 2: Memory Pressure
- **Risk**: Too many forks exhaust memory
- **Mitigation**: Implement fork limits, pooling, and recycling

### Risk 3: Cache Invalidation Complexity
- **Risk**: Cache expires during long-running tasks
- **Mitigation**: Implement cache refresh, graceful degradation

### Risk 4: API Complexity
- **Risk**: ForkedAgent API becomes too complex
- **Mitigation**: Simple defaults, progressive disclosure, good examples

## References

- [Anthropic Prompt Caching Documentation](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [Multi-Agent Orchestration Patterns](examples/orchestrator_example.py)
- [Current Agent Implementation](liteagent/agent.py)
- [Memory Management System](liteagent/memory.py)

## Notes

- This is primarily a research task to explore cost optimization strategies
- Initial implementation should focus on Anthropic provider (has best caching)
- Consider creating a separate `experimental/` directory for this feature initially
- May require provider-specific optimizations
- Could potentially save significant costs for enterprise users with large contexts

## Next Steps

1. Set up experimental branch for development
2. Create proof-of-concept with Anthropic provider
3. Benchmark cost savings with real-world scenarios
4. Gather feedback from potential users
5. Refine API based on usage patterns