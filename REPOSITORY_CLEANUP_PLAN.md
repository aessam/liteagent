# Repository Structure Cleanup Plan

## Current Issues

**CONCLUSION: Repository structure violates Python project standards** (deduction)
└── WHY: Multiple anti-patterns present (observation)
    └── WHY: Build artifacts committed to repo (fact)
    └── WHY: Duplicate functionality across locations (fact)
    └── WHY: Configuration files scattered throughout (fact)
    └── WHY: Documentation mixed with code (observation)

## Problems to Fix

### 1. Build Artifacts & Temporary Files (Should NOT be in repo)
```
❌ liteagent.egg-info/           # setuptools build directory
❌ pytestdebug.log              # pytest debug log
❌ static/                      # empty directory
❌ __pycache__/                 # Python bytecode (if exists)
```

### 2. Temporary Documentation Files (Move to docs/)
```
❌ ephemeral_agent_implementation.md
❌ taskbased_agent_implementation.md
❌ FUNCTION_CALLING_CLEANUP_TASKS.md
❌ FUNCTION_CALLING_CLEANUP_SUMMARY.md
❌ test_function_calling_cleanup.py
```

### 3. Duplicate Functionality
```
❌ cli/ + liteagent/cli.py      # Two CLI implementations
❌ main.py + liteagent/__main__.py  # Two main entry points
❌ examples/ + liteagent/examples.py  # Two example locations
❌ tools/ scripts               # Development tools in root
```

### 4. Configuration Duplication
```
❌ setup.py + pyproject.toml    # Use only pyproject.toml (modern)
❌ requirements.txt + pyproject.toml deps  # Consolidate dependencies
❌ MANIFEST.in                  # Not needed with pyproject.toml
```

### 5. Test Structure Issues
```
❌ tests/tests/                 # Nested tests directory
❌ tests/integration/capabilities/  # Empty directory
❌ Scattered test utilities
```

## Standard Python Project Structure

**CONCLUSION: Should follow this standard structure** (industry standard)
```
liteagent/
├── pyproject.toml              # Modern Python packaging
├── README.md
├── LICENSE
├── .gitignore                  # Missing!
├── src/                        # Standard src layout
│   └── liteagent/
│       ├── __init__.py
│       ├── __main__.py         # CLI entry point
│       ├── core/               # Core functionality
│       ├── handlers/           # Provider handlers
│       ├── models/             # Model interfaces
│       └── utils/              # Utilities
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── docs/
│   ├── api/
│   ├── guides/
│   └── examples/
└── scripts/                    # Development scripts
    └── dev-tools/
```

## Cleanup Actions

### Phase 1: Remove Unwanted Files
- [ ] Delete `liteagent.egg-info/`
- [ ] Delete `pytestdebug.log`
- [ ] Delete `static/`
- [ ] Delete temporary documentation files
- [ ] Delete `test_function_calling_cleanup.py`

### Phase 2: Consolidate Duplicates
- [ ] Choose one CLI implementation (keep `liteagent/cli.py`)
- [ ] Remove duplicate `cli/`
- [ ] Remove `main.py` (keep `__main__.py`)
- [ ] Merge examples into one location
- [ ] Move development tools to `scripts/`

### Phase 3: Fix Configuration
- [ ] Remove `setup.py` (use only `pyproject.toml`)
- [ ] Remove `requirements.txt` (use pyproject.toml)
- [ ] Remove `MANIFEST.in`
- [ ] Create proper `.gitignore`

### Phase 4: Reorganize Structure
- [ ] Move to `src/liteagent/` layout
- [ ] Organize code into logical modules
- [ ] Fix test structure
- [ ] Organize documentation

### Phase 5: Update Configuration
- [ ] Update `pyproject.toml` entry points
- [ ] Fix import paths
- [ ] Update test configuration
- [ ] Update documentation links

## Expected Benefits

**CONCLUSION: This cleanup will provide significant benefits** (deduction)
└── WHY: Standard structure improves maintainability (industry practice)
└── WHY: Reduces confusion for contributors (fact)
└── WHY: Enables better tooling support (deduction)
    └── WHY: IDEs work better with standard layouts (industry standard)
└── WHY: Simplifies CI/CD setup (experience)
└── WHY: Reduces repository size (removing build artifacts)