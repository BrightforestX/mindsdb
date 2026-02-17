# MindsDB Git Workflow Plan: Nango Authentication Integration

## Overview
This document outlines the steps to properly manage the Nango authentication flow changes in the MindsDB project, including creating feature branches, pulling upstream changes, and selectively merging modifications.

## Current Repository State Assessment

### Step 1: Check Current Status
```bash
cd /Users/clifforddalsoniii/Documents/Brightforest/projects/development/active/ml/mindsdb

# Assess current git status
git status
git branch -a
git remote -v

# Check for uncommitted changes
git diff --name-only
git diff --cached --name-only
```

**Expected Output:**
- Current branch: main
- Remotes: origin (your fork), upstream (mindsdb/mindsdb)
- Working directory: clean or with known modifications

## Phase 1: Feature Branch Creation and Push

### Step 2: Create and Push Feature Branch
```bash
# Ensure we're on main and working directory is clean
git checkout main
git status

# Create feature branch for Nango authentication work
git checkout -b github_handler

# Add and commit current changes
git add .
git commit -m "feat: Add Nango authentication flow support

- Add authentication bypass for development
- Modify check_auth function to support Nango integration
- Update API initialization to handle Nango connections
- Configure local MindsDB instance for Nango testing"

# Push feature branch to origin
git push -u origin github_handler
```

**Verification:**
```bash
git branch -vv
git log --oneline -5
```

## Phase 2: Update Main Branch with Latest Upstream

### Step 3: Switch to Main and Pull Upstream Changes
```bash
# Switch back to main branch
git checkout main

# Fetch latest changes from upstream
git fetch upstream

# Review what will be merged
git log --oneline upstream/main -10
git diff --stat upstream/main..HEAD

# Merge upstream changes
git merge upstream/main
```

**Conflict Resolution (if needed):**
```bash
# If conflicts occur, resolve them manually
git status
# Edit conflicted files
git add <resolved-files>
git commit
```

### Step 4: Verify Main Branch Health
```bash
# Run basic tests to ensure main still works
python -m pytest tests/unit/test_config.py -v
python -c "import mindsdb; print('Import successful')"

# Check that basic functionality works
python -m mindsdb --help
```

## Phase 3: Selective Merge Options

### Option A: Interactive Rebase (Recommended)
```bash
# Create clean integration branch
git checkout github_handler
git checkout -b github_handler_integration

# Perform interactive rebase to select commits
git rebase -i main

# In editor, mark desired commits as 'pick', others as 'drop'
# Save and exit editor

# If conflicts, resolve and continue
git rebase --continue

# Merge clean branch to main
git checkout main
git merge github_handler_integration --no-ff -m "feat: Integrate Nango authentication flow

Selective merge of Nango authentication changes:
- Authentication bypass for development testing
- Nango connection handling
- API endpoint modifications"
```

### Option B: Cherry-Pick Specific Commits
```bash
# Identify specific commits to cherry-pick
git log --oneline github_handler

# Example cherry-pick commands:
git checkout main
git cherry-pick abc1234  # Authentication bypass commit
git cherry-pick def5678  # API modification commit
git cherry-pick ghi9012  # Configuration changes commit
```

### Option C: Manual Selective Merge
```bash
# Perform merge without auto-commit
git checkout main
git merge github_handler --no-commit --no-ff

# Selectively stage only desired files
git reset HEAD -- .  # Unstage everything

# Stage only specific files
git add mindsdb/api/http/initialize.py
git add mindsdb/api/http/namespaces/default.py
git add mindsdb/api/http/namespaces/config.py  # If exists

# Commit selective changes
git commit -m "feat: Add selective Nango authentication support

Includes:
- mindsdb/api/http/initialize.py: Authentication bypass
- mindsdb/api/http/namespaces/default.py: check_auth modifications
- Configuration updates for Nango integration"
```

## Phase 4: Comprehensive Verification

### Step 5: Test the Integration
```bash
# Test basic MindsDB functionality
python -c "import mindsdb; print('✓ Import successful')"

# Test configuration loading
python -c "from mindsdb.utilities.config import Config; c = Config(); print('✓ Config loaded')"

# Test API endpoints (if applicable)
python -c "
import requests
try:
    response = requests.get('http://localhost:47334/api/status')
    print(f'✓ API status: {response.status_code}')
except:
    print('⚠ API not running (expected for unit tests)')
"

# Run relevant unit tests
python -m pytest tests/unit/api/test_auth.py -v --tb=short
python -m pytest tests/unit/api/test_config.py -v --tb=short
```

### Step 6: Verify Nango Integration Points
```bash
# Check that modified files contain expected changes
grep -n "TEMPORARILY DISABLE AUTH" mindsdb/api/http/initialize.py
grep -n "return True" mindsdb/api/http/namespaces/default.py

# Verify no unintended changes
git diff main..HEAD --name-only
git diff main..HEAD --stat
```

### Step 7: Push Updated Main Branch
```bash
# Push the merged changes
git push origin main

# Tag the integration if significant
git tag -a "v1.0.0-nango-integration" -m "Nango authentication flow integration"
git push origin --tags
```

## Phase 5: Cleanup and Documentation

### Step 8: Clean Up Branches
```bash
# Delete feature branches if no longer needed
git branch -d github_handler
git branch -d github_handler_integration
git push origin --delete github_handler
git push origin --delete github_handler_integration
```

### Step 9: Update Documentation
```bash
# Create or update documentation about the Nango integration
echo "# Nango Authentication Integration

## Overview
This integration adds support for Nango authentication flow in MindsDB.

## Changes Made
- Modified authentication checks in API initialization
- Updated check_auth function for Nango compatibility
- Added configuration support for Nango connections

## Testing
Run the following to verify integration:
\`\`\`bash
python -m pytest tests/unit/api/test_auth.py -v
\`\`\`
" > docs/nango_integration.md

git add docs/nango_integration.md
git commit -m "docs: Add Nango integration documentation"
git push origin main
```

## Risk Assessment and Rollback Plan

### Potential Issues
1. **Authentication Bypass**: The temporary auth bypass may cause security issues
2. **API Compatibility**: Changes may break existing API consumers
3. **Configuration Conflicts**: Local config changes may not apply upstream

### Rollback Plan
```bash
# If issues arise, rollback the merge
git revert HEAD --no-edit
git push origin main

# Or reset to before merge
git reset --hard HEAD~1
git push origin main --force-with-lease
```

## Files Modified in This Integration

### Core Authentication Files
- `mindsdb/api/http/initialize.py`: Authentication middleware modifications
- `mindsdb/api/http/namespaces/default.py`: check_auth function changes

### Configuration Files (Local Only)
- `~/.mindsdb/config.json`: Local MindsDB configuration
- `scripts/restart-mindsdb.sh`: Local restart script

### Test Files (if any)
- Any new test files for Nango integration

## Success Criteria

- [ ] Feature branch created and pushed successfully
- [ ] Main branch updated with latest upstream changes
- [ ] Selective merge completed without conflicts
- [ ] Basic MindsDB functionality verified
- [ ] Nango authentication flow operational
- [ ] Documentation updated
- [ ] No security vulnerabilities introduced

## Next Steps

1. Test the Nango integration end-to-end
2. Remove temporary authentication bypasses
3. Implement proper authentication for Nango connections
4. Add comprehensive integration tests
5. Submit changes upstream if appropriate

---

**Note**: This plan assumes you have proper permissions to push to the origin remote and that upstream changes don't conflict significantly with your modifications.
