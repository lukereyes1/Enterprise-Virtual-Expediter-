# ShortScreen - Single Source of Truth Refactoring Plan

## Current State Analysis

### Models/Schemas Duplicated Across:

**Python (6 locations):**
1. `shortscreen/data.py`: MarketData, FundamentalData
2. `shortscreen/factors.py`: RawMetrics, FactorScores
3. `shortscreen/engine.py`: ShortCandidate
4. `shortscreen/macro.py`: MacroRegime, ThemeConfig
5. `shortscreen/datastore.py`: CacheMetadata
6. `shortscreen/jobs.py`: JobResult, JobPhaseMetrics, JobStatus, JobType

**TypeScript (1 location):**
7. `shortscreen-mobile/src/types/index.ts`: ALL API types (duplicates Python)

**FastAPI Backend (1 location):**
8. `shortscreen-mobile/backend/main.py`: Pydantic models (duplicates Python)

**Documentation (multiple):**
9. READMEs with example schemas

### Config Values Spread Across:

**YAML Files:**
1. `shortscreen/config/theme_config.yaml`: Theme weights, sensitivities
2. `shortscreen/config/etf_proxies.yaml`: ETF tickers
3. `shortscreen/config/service_config.yaml`: Service settings

**Hard-coded in Python:**
4. `shortscreen/themes.py`: Filter thresholds (P/S > 3, D/E > 1.5, etc.)
5. `shortscreen/factors.py`: Factor weight calculations (0.40, 0.30, etc.)
6. `shortscreen/cli.py`: Default values (top=20)

**Hard-coded in TypeScript:**
7. `shortscreen-mobile/src/api/client.ts`: API_BASE_URL

### Issues Identified:

1. ❌ **No single source**: Change FactorScores requires editing 3+ files
2. ❌ **Manual sync**: TypeScript types manually mirror Python
3. ❌ **No validation**: Config changes don't verify against code
4. ❌ **Magic numbers**: Factor weights scattered in code
5. ❌ **Brittle**: Add new factor = edit 6+ locations

---

## Refactoring Solution

### Phase 1: Central Models Module ✅

**Create `shortscreen/models/`** as single source of truth:

```
shortscreen/models/
├── __init__.py
├── core.py           # MacroRegime, FactorScores, RawMetrics
├── data.py           # MarketData, FundamentalData
├── screening.py      # ShortCandidate, ThemeScore
├── jobs.py           # JobResult, JobStatus
├── events.py         # Event, EventType
├── reports.py        # Report, ReportMetrics
└── config.py         # Config dataclasses
```

**Technology:** Pydantic v2 (validation + JSON schema generation)

**Benefits:**
- Single definition for all models
- Auto-generate JSON schemas
- Runtime validation
- Type safety

### Phase 2: Unified Config System ✅

**Consolidate to `shortscreen/config/`:**

```
shortscreen/config/
├── __init__.py
├── defaults.py       # Python constants (DRY)
├── themes.yaml       # ALL theme config (weights, filters, ETFs)
├── factors.yaml      # ALL factor config (weights, formulas)
├── universe.yaml     # Universe filters
├── service.yaml      # Service settings
└── alerts.yaml       # Alert thresholds
```

**Validation:**
- Config loader validates against Pydantic models
- Fail fast on startup if invalid
- Type-safe config access

### Phase 3: Auto-Generation Scripts ✅

**Create `scripts/`:**

```
scripts/
├── gen_openapi.py          # Generate OpenAPI spec from Pydantic
├── gen_typescript_types.py # Generate TS types from Pydantic
├── validate_configs.py     # Cross-validate all configs
└── check_consistency.py    # Pre-commit hook
```

**Workflow:**
1. Change Pydantic model → Run script → TS types updated
2. Change config → Validation script checks compatibility
3. Pre-commit hook prevents inconsistent commits

### Phase 4: Consistency Tests ✅

**Add `tests/test_consistency.py`:**

```python
def test_all_themes_have_config():
    """Verify each Theme class has config entry"""

def test_all_config_keys_used():
    """Verify no orphaned config keys"""

def test_typescript_matches_python():
    """Verify generated TS types are up to date"""

def test_cli_options_match_config():
    """Verify CLI defaults match config"""

def test_api_schema_matches_models():
    """Verify OpenAPI spec matches Pydantic"""
```

### Phase 5: Refactor Modules ✅

**Migration path:**

1. **factors.py**: Import from `shortscreen.models.core`
2. **themes.py**: Import from `shortscreen.models.core` + load config
3. **engine.py**: Import from `shortscreen.models.screening`
4. **API**: Import from `shortscreen.models` (already Pydantic)
5. **Mobile**: Use generated TypeScript types

### Phase 6: Documentation Sync ✅

**Update all docs:**
- Reference central models location
- Document generation scripts
- Add "How to add X" guides
- Ensure examples match current code

---

## Implementation Order

### Day 1: Models Migration

**Morning:**
- [ ] Create `shortscreen/models/` structure
- [ ] Define all models with Pydantic
- [ ] Add JSON schema export

**Afternoon:**
- [ ] Refactor `data.py` to use new models
- [ ] Refactor `factors.py` to use new models
- [ ] Run tests, fix breaks

### Day 2: Config Consolidation

**Morning:**
- [ ] Create unified config structure
- [ ] Move all hard-coded values to YAML
- [ ] Create config loader with validation

**Afternoon:**
- [ ] Refactor `themes.py` to load from config
- [ ] Refactor `cli.py` to use config defaults
- [ ] Run tests, fix breaks

### Day 3: Auto-Generation

**Morning:**
- [ ] Write `gen_typescript_types.py`
- [ ] Write `gen_openapi.py`
- [ ] Generate and verify outputs

**Afternoon:**
- [ ] Write `validate_configs.py`
- [ ] Add to test suite
- [ ] Document usage

### Day 4: Consistency Tests

**Morning:**
- [ ] Write `test_consistency.py`
- [ ] Add cross-file validation
- [ ] Add to CI/CD

**Afternoon:**
- [ ] Refactor remaining modules
- [ ] Update FastAPI backend
- [ ] Run full test suite

### Day 5: Documentation & Validation

**Morning:**
- [ ] Update all READMEs
- [ ] Add "How to" guides
- [ ] Verify all examples work

**Afternoon:**
- [ ] Run end-to-end validation
- [ ] Generate fresh types/schemas
- [ ] Final test pass

---

## Success Criteria

After refactoring, verify:

✅ **Single Source**: All models in `shortscreen/models/`
✅ **Auto-Gen**: TypeScript types generated from Python
✅ **Validation**: Config changes validated automatically
✅ **DRY**: No magic numbers in code
✅ **Consistency**: Tests verify cross-file alignment
✅ **Documentation**: Clear guides for modifications

---

## Detailed File Changes

### New Files to Create:

1. `shortscreen/models/__init__.py` - Export all models
2. `shortscreen/models/core.py` - Core domain models
3. `shortscreen/models/data.py` - Data models
4. `shortscreen/models/screening.py` - Screening models
5. `shortscreen/models/jobs.py` - Job models
6. `shortscreen/models/events.py` - Event models
7. `shortscreen/models/reports.py` - Report models
8. `shortscreen/config/defaults.py` - Python constants
9. `shortscreen/config/themes.yaml` - Consolidated themes
10. `shortscreen/config/factors.yaml` - Consolidated factors
11. `scripts/gen_typescript_types.py` - Type generator
12. `scripts/gen_openapi.py` - OpenAPI generator
13. `scripts/validate_configs.py` - Config validator
14. `tests/test_consistency.py` - Consistency tests

### Files to Refactor:

1. `shortscreen/data.py` - Use models.data
2. `shortscreen/factors.py` - Use models.core + config
3. `shortscreen/themes.py` - Use models.core + config
4. `shortscreen/engine.py` - Use models.screening
5. `shortscreen/macro.py` - Use models.core + config
6. `shortscreen/jobs.py` - Use models.jobs
7. `shortscreen/cli.py` - Use config defaults
8. `shortscreen-mobile/backend/main.py` - Use shortscreen.models
9. `shortscreen-mobile/src/types/index.ts` - Use generated types

### Files to Update:

1. All READMEs - Reference new structure
2. `requirements.txt` - Add pydantic
3. `.gitignore` - Ignore generated files
4. `setup.py` - Include models package

---

## Risk Mitigation

**Backward Compatibility:**
- Keep old imports working initially
- Add deprecation warnings
- Remove in next major version

**Testing:**
- Run full test suite after each phase
- Keep tests passing continuously
- Add new tests before refactoring

**Rollback Plan:**
- Each phase is a separate commit
- Can rollback to any phase
- Feature branches for each day

---

## Expected Outcomes

**Before Refactor:**
- Add new factor: Edit 6 files, manually sync types
- Change theme weight: Edit YAML + validate manually
- Update API: Edit Python + TypeScript separately

**After Refactor:**
- Add new factor: Edit 1 Pydantic model, run script → TS updated
- Change theme weight: Edit YAML → validation runs automatically
- Update API: Edit Pydantic model → OpenAPI + TS regenerated

**Time Savings:**
- New feature: 50% faster (less coordination)
- Bug fixes: 70% faster (single location)
- Onboarding: 80% faster (clear structure)

---

This refactoring is the foundation for scaling ShortScreen to production.
