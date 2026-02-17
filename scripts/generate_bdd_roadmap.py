#!/usr/bin/env python3
"""
Generate BDD-aligned roadmap from feature files and test results.

This script:
1. Parses all .feature files using gherkin-official
2. Extracts scenarios and their status
3. Maps to test execution results from pytest JSON reports
4. Generates a markdown roadmap document
"""
import json
import os
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Try to import gherkin-official, but fall back to simple parser if not available
USE_GHERKIN_OFFICIAL = False
try:
    from gherkin import GherkinParser
    from gherkin.streams import GherkinStreams
    USE_GHERKIN_OFFICIAL = True
except ImportError:
    # Will use simple parser instead
    pass


class BDDRoadmapGenerator:
    """Generate roadmap from BDD feature files and test results."""

    def __init__(self, project_root: Path, test_results_dir: Optional[Path] = None, strict: bool = False, verbose: bool = False):
        self.project_root = project_root
        self.features_dir = project_root / "features"
        self.bdd_features_dir = project_root / "tests" / "bdd" / "features"
        self.reports_dir = test_results_dir or project_root / "reports"
        self.strict = strict
        self.verbose = verbose
        self.unmapped_scenarios = []
        # Parser only used if gherkin-official is available
        self.parser = GherkinParser() if USE_GHERKIN_OFFICIAL else None

    def find_feature_files(self) -> List[Path]:
        """Find all .feature files in the project."""
        feature_files = []
        
        # Find Behave feature files
        if self.features_dir.exists():
            feature_files.extend(self.features_dir.rglob("*.feature"))
        
        # Find pytest-bdd-ng feature files
        if self.bdd_features_dir.exists():
            feature_files.extend(self.bdd_features_dir.rglob("*.feature"))
        
        return sorted(feature_files)

    def parse_feature_file(self, feature_path: Path) -> Optional[Dict]:
        """Parse a feature file and extract scenarios."""
        try:
            with open(feature_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Parse using simple parser (gherkin-official integration can be added later)
            # For now, use a simple parser that works reliably
            parsed = self._simple_parse_feature(content, feature_path)
            
            if not parsed or not parsed.get("name"):
                return None
            
            return {
                "path": str(feature_path.relative_to(self.project_root)),
                "name": parsed["name"],
                "description": parsed.get("description", ""),
                "tags": parsed.get("tags", []),
                "scenarios": parsed.get("scenarios", []),
            }
        except Exception as e:
            print(f"Warning: Failed to parse {feature_path}: {e}", file=sys.stderr)
            return None

    def parse_pytest_results(self, json_path: Path) -> Dict[str, Dict[str, str]]:
        """
        Parse pytest-json-report format.
        
        Returns a dictionary mapping (feature_path, scenario_name) to outcome.
        """
        if not json_path.exists():
            if self.verbose:
                print(f"Info: pytest report not found: {json_path}", file=sys.stderr)
            return {}
        
        try:
            with open(json_path, "r") as f:
                report = json.load(f)
        except Exception as e:
            print(f"Warning: Failed to parse pytest report: {e}", file=sys.stderr)
            return {}
        
        results = {}
        tests = report.get("tests", [])
        
        for test in tests:
            nodeid = test.get("nodeid", "")
            outcome = test.get("outcome", "unknown")
            
            # Parse nodeid format: tests/bdd/features/api/mysql_api.feature::test_scenario_name
            # or: features/api/mysql_api.feature::test_scenario_name
            if "::" in nodeid and nodeid.endswith(".feature"):
                # This is a feature file test
                parts = nodeid.split("::")
                if len(parts) >= 2:
                    feature_path = parts[0]
                    scenario_name = "::".join(parts[1:])  # Handle multiple :: separators
                    
                    # Normalize feature path
                    feature_path = str(Path(feature_path).as_posix())
                    normalized_name = self.normalize_name(scenario_name)
                    
                    key = (feature_path, normalized_name)
                    results[key] = outcome
        
        if self.verbose:
            print(f"Parsed {len(results)} pytest test results", file=sys.stderr)
        
        return results
    
    def parse_behave_results(self, json_path: Path) -> Dict[str, Dict[str, str]]:
        """
        Parse Behave JSON report format.
        
        Returns a dictionary mapping (feature_path, scenario_name) to status.
        """
        if not json_path.exists():
            if self.verbose:
                print(f"Info: Behave report not found: {json_path}", file=sys.stderr)
            return {}
        
        try:
            with open(json_path, "r") as f:
                features = json.load(f)
        except Exception as e:
            print(f"Warning: Failed to parse Behave report: {e}", file=sys.stderr)
            return {}
        
        if not isinstance(features, list):
            print(f"Warning: Behave report is not a list: {type(features)}", file=sys.stderr)
            return {}
        
        results = {}
        
        for feature in features:
            uri = feature.get("uri", "")
            elements = feature.get("elements", [])
            
            for element in elements:
                if element.get("type") != "scenario":
                    continue
                
                scenario_name = element.get("name", "")
                steps = element.get("steps", [])
                
                # Determine scenario status from step results
                step_statuses = []
                for step in steps:
                    result = step.get("result", {})
                    status = result.get("status", "unknown")
                    step_statuses.append(status)
                
                # Determine overall scenario status
                if not step_statuses:
                    scenario_status = "unknown"
                elif all(s == "passed" for s in step_statuses):
                    scenario_status = "passed"
                elif any(s == "failed" for s in step_statuses):
                    scenario_status = "failed"
                elif any(s == "skipped" for s in step_statuses):
                    scenario_status = "skipped"
                elif any(s == "undefined" for s in step_statuses):
                    scenario_status = "undefined"
                else:
                    scenario_status = "partial"  # Mixed statuses
                
                # Normalize paths and names
                feature_path = str(Path(uri).as_posix())
                normalized_name = self.normalize_name(scenario_name)
                
                key = (feature_path, normalized_name)
                results[key] = scenario_status
        
        if self.verbose:
            print(f"Parsed {len(results)} Behave test results", file=sys.stderr)
        
        return results
    
    def normalize_name(self, name: str) -> str:
        """Normalize scenario/test name for matching."""
        # Remove special characters, lowercase, normalize spaces
        normalized = re.sub(r'[^\w\s]', '', name.lower()).strip()
        normalized = re.sub(r'\s+', '_', normalized)
        return normalized
    
    def match_scenario_to_test_result(self, feature_path: str, scenario_name: str, test_results: Dict) -> Optional[str]:
        """
        Match a scenario to test results.
        
        Returns: "passed", "failed", "skipped", "partial", or None
        """
        # Normalize feature path and scenario name
        feature_path_norm = str(Path(feature_path).as_posix())
        scenario_name_norm = self.normalize_name(scenario_name)
        
        # Try pytest-bdd-ng results first
        pytest_results = test_results.get("pytest_bdd", {})
        if isinstance(pytest_results, dict):
            key = (feature_path_norm, scenario_name_norm)
            if key in pytest_results:
                outcome = pytest_results[key]
                # Map pytest outcomes to our status
                if outcome == "passed":
                    return "passed"
                elif outcome == "failed":
                    return "failed"
                elif outcome == "skipped":
                    return "skipped"
        
        # Try Behave results
        behave_results = test_results.get("behave", {})
        if isinstance(behave_results, dict):
            key = (feature_path_norm, scenario_name_norm)
            if key in behave_results:
                return behave_results[key]
        
        # Try fuzzy matching - check if feature path matches (without exact scenario name)
        for (test_feature_path, test_scenario_name), status in pytest_results.items():
            if feature_path_norm in test_feature_path or test_feature_path in feature_path_norm:
                # Feature paths match, try scenario name similarity
                if scenario_name_norm in test_scenario_name or test_scenario_name in scenario_name_norm:
                    return status
        
        for (test_feature_path, test_scenario_name), status in behave_results.items():
            if feature_path_norm in test_feature_path or test_feature_path in feature_path_norm:
                if scenario_name_norm in test_scenario_name or test_scenario_name in scenario_name_norm:
                    return status
        
        # No match found
        self.unmapped_scenarios.append((feature_path, scenario_name))
        return None
    
    def load_test_results(self) -> Dict:
        """Load test results from JSON reports."""
        results = {
            "pytest_bdd": {},
            "behave": {},
        }
        
        # Load pytest-bdd-ng results
        pytest_report = self.reports_dir / "pytest-bdd-report.json"
        if pytest_report.exists():
            results["pytest_bdd"] = self.parse_pytest_results(pytest_report)
        elif self.verbose:
            print(f"Info: pytest report not found: {pytest_report}", file=sys.stderr)
        
        # Load Behave results
        behave_report = self.reports_dir / "behave.json"
        if behave_report.exists():
            results["behave"] = self.parse_behave_results(behave_report)
        elif self.verbose:
            print(f"Info: Behave report not found: {behave_report}", file=sys.stderr)
        
        return results

    def _simple_parse_feature(self, content: str, feature_path: Path) -> Dict:
        """Simple fallback parser for feature files when gherkin-official fails."""
        lines = content.split("\n")
        feature_name = ""
        feature_tags = []
        description = []
        scenarios = []
        current_scenario = None
        in_feature = False
        in_scenario = False
        in_background = False
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            
            if stripped.startswith("@") and not in_scenario and not in_background:
                # Feature-level tags
                tag = stripped.replace("@", "").strip()
                feature_tags.append(tag)
            elif stripped.startswith("Feature:"):
                feature_name = stripped.replace("Feature:", "").strip()
                in_feature = True
                in_scenario = False
                in_background = False
            elif in_feature and stripped.startswith("Background:"):
                in_background = True
                in_scenario = False
            elif in_feature and stripped.startswith(("Scenario", "Scenario Outline")):
                if current_scenario:
                    scenarios.append(current_scenario)
                scenario_name = stripped.replace("Scenario:", "").replace("Scenario Outline:", "").strip()
                current_scenario = {
                    "name": scenario_name,
                    "tags": feature_tags.copy(),  # Start with feature tags
                    "steps": [],
                    "line": i,
                }
                in_scenario = True
                in_background = False
            elif in_scenario and stripped.startswith("@") and current_scenario:
                # Scenario-level tags
                tag = stripped.replace("@", "").strip()
                if tag not in current_scenario["tags"]:
                    current_scenario["tags"].append(tag)
            elif (in_scenario or in_background) and stripped.startswith(("Given", "When", "Then", "And", "But")):
                keyword = stripped.split()[0]
                text = " ".join(stripped.split()[1:])
                if current_scenario:
                    current_scenario["steps"].append({"keyword": keyword, "text": text})
            elif in_feature and not in_scenario and not in_background and stripped and not stripped.startswith(("Feature", "@")):
                # Description lines
                description.append(stripped)
        
        if current_scenario:
            scenarios.append(current_scenario)
        
        return {
            "name": feature_name,
            "description": "\n".join(description).strip(),
            "tags": feature_tags,
            "scenarios": scenarios,
        }
    
    def get_scenario_status(self, feature_path: str, scenario_name: str, test_results: Dict) -> str:
        """Determine scenario status from test results."""
        status = self.match_scenario_to_test_result(feature_path, scenario_name, test_results)
        return status if status else "not_implemented"

    def generate_roadmap(self, output_path: Optional[Path] = None) -> str:
        """Generate roadmap markdown document."""
        feature_files = self.find_feature_files()
        test_results = self.load_test_results()
        self.unmapped_scenarios = []  # Reset for this generation
        
        features = []
        for feature_file in feature_files:
            feature_data = self.parse_feature_file(feature_file)
            if feature_data:
                features.append(feature_data)
        
        # Calculate coverage statistics
        total_scenarios = sum(len(f["scenarios"]) for f in features)
        passing = 0
        failing = 0
        skipped = 0
        not_implemented = 0
        partial = 0
        
        # Group features by category
        categories = {
            "API": [],
            "Models": [],
            "Handlers": [],
            "Integrations": [],
            "Other": [],
        }
        
        for feature in features:
            path = feature["path"]
            if "/api/" in path:
                categories["API"].append(feature)
            elif "/models/" in path:
                categories["Models"].append(feature)
            elif "/handlers/" in path:
                categories["Handlers"].append(feature)
            elif "/integrations/" in path:
                categories["Integrations"].append(feature)
            else:
                categories["Other"].append(feature)
        
        # Generate markdown
        markdown = []
        markdown.append("# BDD Test Roadmap")
        markdown.append("")
        markdown.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        markdown.append("")
        markdown.append("## Overview")
        markdown.append("")
        markdown.append(f"- **Total Features**: {len(features)}")
        total_scenarios = sum(len(f["scenarios"]) for f in features)
        markdown.append(f"- **Total Scenarios**: {total_scenarios}")
        markdown.append("")
        
        # Summary by category
        markdown.append("## Summary by Category")
        markdown.append("")
        for category, category_features in categories.items():
            if category_features:
                category_scenarios = sum(len(f["scenarios"]) for f in category_features)
                markdown.append(f"- **{category}**: {len(category_features)} features, {category_scenarios} scenarios")
        markdown.append("")
        
        # Features by category
        for category, category_features in categories.items():
            if not category_features:
                continue
            
            markdown.append(f"## {category} Features")
            markdown.append("")
            
            for feature in category_features:
                markdown.append(f"### {feature['name']}")
                markdown.append("")
                markdown.append(f"**File**: `{feature['path']}`")
                markdown.append("")
                
                # Format description nicely - preserve multi-line
                if feature["description"]:
                    desc_lines = feature["description"].strip().split("\n")
                    for desc_line in desc_lines:
                        if desc_line.strip():
                            markdown.append(f"*{desc_line.strip()}*")
                    markdown.append("")
                
                if feature["tags"]:
                    tags_str = ", ".join(f"`{tag}`" for tag in feature["tags"])
                    markdown.append(f"**Tags**: {tags_str}")
                    markdown.append("")
                
                total_steps = sum(len(s.get("steps", [])) for s in feature["scenarios"])
                markdown.append(f"**Scenarios**: {len(feature['scenarios'])} ({total_steps} total steps)")
                markdown.append("")
                
                for scenario in feature["scenarios"]:
                    # Get scenario status from test results
                    status = self.get_scenario_status(feature["path"], scenario["name"], test_results)
                    
                    # Update statistics
                    if status == "passed":
                        passing += 1
                        checkbox = "[x]"
                    elif status == "failed":
                        failing += 1
                        checkbox = "[ ]"
                    elif status == "skipped":
                        skipped += 1
                        checkbox = "[S]"
                    elif status == "partial":
                        partial += 1
                        checkbox = "[~]"
                    else:  # not_implemented or None
                        not_implemented += 1
                        checkbox = "[ ]"
                    
                    markdown.append(f"- {checkbox} **{scenario['name']}**")
                    if scenario["tags"]:
                        scenario_tags = [t for t in scenario["tags"] if t not in feature["tags"]]
                        if scenario_tags:
                            tags_str = ", ".join(f"`{tag}`" for tag in scenario_tags)
                            markdown.append(f"  - Tags: {tags_str}")
                    if scenario.get("steps"):
                        markdown.append(f"  - Steps: {len(scenario['steps'])}")
                    if status and status != "not_implemented":
                        markdown.append(f"  - Status: {status}")
                    markdown.append("")
                
                markdown.append("---")
                markdown.append("")
        
        # Test Coverage Statistics
        markdown.append("## Test Coverage Statistics")
        markdown.append("")
        markdown.append(f"- **Total Scenarios**: {total_scenarios}")
        if total_scenarios > 0:
            coverage_pct = ((passing + partial) / total_scenarios) * 100
            markdown.append(f"- **Passing**: {passing} ({passing/total_scenarios*100:.1f}%)")
            markdown.append(f"- **Failing**: {failing} ({failing/total_scenarios*100:.1f}%)")
            markdown.append(f"- **Not Implemented**: {not_implemented} ({not_implemented/total_scenarios*100:.1f}%)")
            markdown.append(f"- **Skipped**: {skipped} ({skipped/total_scenarios*100:.1f}%)")
            if partial > 0:
                markdown.append(f"- **Partial**: {partial} ({partial/total_scenarios*100:.1f}%)")
            markdown.append(f"- **Coverage**: {coverage_pct:.1f}%")
        markdown.append("")
        
        # Test Results Section
        markdown.append("## Test Results")
        markdown.append("")
        
        pytest_count = len(test_results.get("pytest_bdd", {}))
        behave_count = len(test_results.get("behave", {}))
        
        if pytest_count > 0:
            markdown.append(f"- **pytest-bdd-ng**: {pytest_count} test results loaded")
        else:
            markdown.append("- **pytest-bdd-ng**: No results found (run `make bdd_tests`)")
        
        if behave_count > 0:
            markdown.append(f"- **Behave**: {behave_count} test results loaded")
        else:
            markdown.append("- **Behave**: No results found (run `make behave_tests`)")
        
        markdown.append("")
        
        # Unmapped scenarios warning
        if self.unmapped_scenarios:
            markdown.append("### Unmapped Scenarios")
            markdown.append("")
            markdown.append(f"The following {len(self.unmapped_scenarios)} scenarios could not be matched to test results:")
            markdown.append("")
            for feature_path, scenario_name in self.unmapped_scenarios[:10]:  # Show first 10
                markdown.append(f"- `{feature_path}`: {scenario_name}")
            if len(self.unmapped_scenarios) > 10:
                markdown.append(f"- ... and {len(self.unmapped_scenarios) - 10} more")
            markdown.append("")
        
        markdown.append("### How to Update")
        markdown.append("")
        markdown.append("1. Run BDD tests: `make bdd_tests` and `make behave_tests`")
        markdown.append("2. Generate roadmap: `python scripts/generate_bdd_roadmap.py`")
        markdown.append("3. Review and commit the updated roadmap")
        markdown.append("")
        
        roadmap_content = "\n".join(markdown)
        
        # Write to file if output path specified
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(roadmap_content)
            print(f"Roadmap generated: {output_path}")
        else:
            print(roadmap_content)
        
        return roadmap_content


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate BDD roadmap from feature files and test results")
    parser.add_argument(
        "--test-results-dir",
        type=str,
        help="Custom directory for test result files (default: reports/)"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Only mark as passing if all tests pass (no partial passes)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed matching information"
    )
    
    args = parser.parse_args()
    
    # Get project root (assuming script is in scripts/ directory)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    test_results_dir = Path(args.test_results_dir) if args.test_results_dir else None
    
    generator = BDDRoadmapGenerator(
        project_root,
        test_results_dir=test_results_dir,
        strict=args.strict,
        verbose=args.verbose
    )
    
    # Output to docs/BDD_ROADMAP.md or stdout
    output_path = project_root / "docs" / "BDD_ROADMAP.md"
    
    generator.generate_roadmap(output_path)


if __name__ == "__main__":
    main()
