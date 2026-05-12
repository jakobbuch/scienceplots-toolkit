---
name: "Spec: [Feature Name]"
description: "[Brief description of the feature or change]"
type: "[feature | refactor | bugfix | documentation]"
status: "[draft | proposed | approved | implemented]"
---

# Specification: [Feature Name]

## Problem Statement

[Describe the problem this specification addresses. What pain point, gap, or opportunity exists?]

## Proposed Solution

[High-level description of the proposed solution. What will be built and how does it solve the problem?]

## Acceptance Criteria

**These are the MUST-HAVE requirements.** Implementation is incomplete if any criterion is not met.

### Functional Requirements

- [ ] **AC-1**: [Specific, testable functional requirement]
- [ ] **AC-2**: [Specific, testable functional requirement]
- [ ] **AC-3**: [Specific, testable functional requirement]

### Non-Functional Requirements

- [ ] **AC-NF1**: [Performance, security, or quality requirement]
- [ ] **AC-NF2**: [Performance, security, or quality requirement]

### Documentation Requirements

- [ ] **AC-D1**: [Documentation requirement - docstrings, examples, etc.]
- [ ] **AC-D2**: [Documentation requirement]

## Scope

### In Scope

- [What IS included in this specification]
- [Specific features, files, or behaviors]

### Out of Scope

- [What is NOT included - explicitly excluded items]
- [Future enhancements, edge cases, etc.]

## Design

### Architecture

[Describe the architectural approach. What modules, classes, or functions will be created or modified?]

```
src/scienceplots_toolkit/
├── [new_module.py]      # [Purpose]
├── [existing_module.py] # [Changes]
```

### API Design

[Describe public API changes. What functions, classes, or methods will be exposed?]

```python
# Example usage
from scienceplots_toolkit import new_function

result = new_function(param1, param2)
```

### Data Structures

[Describe any new data classes, named tuples, or data structures.]

```python
from dataclasses import dataclass

@dataclass
class NewStructure:
    field1: str
    field2: int
```

## Implementation Plan

### Phase 1: [Foundation]

- [ ] Create [module/file]
- [ ] Implement [core functionality]
- [ ] Add tests for [specific behavior]

### Phase 2: [Integration]

- [ ] Integrate with [existing module]
- [ ] Update [documentation/examples]
- [ ] Add validation

### Phase 3: [Polish]

- [ ] Add edge case handling
- [ ] Performance optimization
- [ ] Final documentation review

## Testing Strategy

### Unit Tests

- [ ] Test [function] with [input] → expect [output]
- [ ] Test [function] error handling with [invalid input]
- [ ] Test [edge case]

### Integration Tests

- [ ] Test [module] integration with [other module]
- [ ] Test end-to-end workflow: [describe workflow]

### Visual Tests (if applicable)

- [ ] Generate baseline images for [plot type]
- [ ] Verify visual output matches design

## Dependencies

### Internal Dependencies

- [List dependencies on other modules or features]

### External Dependencies

- [List any new package dependencies]
- [Version requirements]

## Migration Plan (if applicable)

[Describe how existing code/data will be migrated to the new approach.]

### Breaking Changes

- [List any breaking changes]
- [Deprecation timeline]

### Backward Compatibility

- [Describe backward compatibility approach]
- [Deprecation warnings, shims, etc.]

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk description] | [Low/Med/High] | [Low/Med/High] | [How to mitigate] |
| [Another risk] | [Low/Med/High] | [Low/Med/High] | [How to mitigate] |

## Success Metrics

[How will you measure success? What observable outcomes indicate the feature is working?]

- [Metric 1]: e.g., "All tests pass with 100% coverage"
- [Metric 2]: e.g., "Zero type errors from ty"
- [Metric 3]: e.g., "Documentation complete and accurate"

## Related Work

- Related issues: #[issue-number]
- Related specs: [SPEC-XXX.md](SPEC-XXX.md)
- Related PRs: #[pr-number]

## Appendix

### Examples

[Provide usage examples, code snippets, or mockups.]

### References

[Link to relevant documentation, research, or inspiration.]

---

## Approval

**Spec Author**: [Name/Agent]
**Date Created**: YYYY-MM-DD
**Date Approved**: YYYY-MM-DD
**Approved By**: [Name/Agent]

## Change Log

| Date | Version | Change | Author |
|------|---------|--------|--------|
| YYYY-MM-DD | 1.0 | Initial spec | [Name] |
| | | | |
