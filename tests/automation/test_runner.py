#!/usr/bin/env python3
"""
Intelligent Test Runner - Automatically selects tests based on code changes
"""
import os
import sys
import subprocess
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Set

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "scripts"))

from version_manager import VersionManager

class TestRunner:
    def __init__(self):
        self.project_root = project_root
        self.version_manager = VersionManager(str(project_root / "version.json"))
        self.test_results_dir = project_root / "tests" / "results"
        self.test_results_dir.mkdir(exist_ok=True)
        
        # Test categories and their triggers
        self.test_mapping = {
            "ai_behavior": {
                "triggers": [
                    "backend/engine/ai_integration.py",
                    "backend/engine/strict_narrative_engine.py", 
                    "backend/claude_direct/",
                    "prompts/"
                ],
                "tests": [
                    "tests/ai_behavior/ai_behavior_validation_test.py"
                ],
                "description": "AI constraint and behavior validation"
            },
            "integration": {
                "triggers": [
                    "backend/engine/",
                    "backend/utils/",
                    "backend/testing/"
                ],
                "tests": [
                    "tests/integration/hybrid_game_test.py",
                    "tests/integration/enhanced_game_test.py",
                    "tests/integration/deterministic_game_test.py"
                ],
                "description": "Full system integration tests"
            },
            "performance": {
                "triggers": [
                    "backend/engine/",
                    "backend/claude_direct/",
                    "backend/amazon/",
                    "backend/mistral/"
                ],
                "tests": [
                    "tests/performance/comprehensive_stress_test.py"
                ],
                "description": "Performance and stress testing"
            }
        }
    
    def detect_changes(self) -> Set[str]:
        """Detect changed files using git"""
        try:
            # Get changed files since last commit
            result = subprocess.run(
                ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                return set(result.stdout.strip().split('\n')) if result.stdout.strip() else set()
            else:
                # Fallback: get all modified files
                result = subprocess.run(
                    ["git", "diff", "--name-only"],
                    capture_output=True,
                    text=True,
                    cwd=self.project_root
                )
                return set(result.stdout.strip().split('\n')) if result.stdout.strip() else set()
        except Exception as e:
            print(f"⚠️ Could not detect git changes: {e}")
            return set()
    
    def determine_tests_to_run(self, changed_files: Set[str] = None) -> Dict[str, List[str]]:
        """Determine which tests to run based on changed files"""
        if changed_files is None:
            changed_files = self.detect_changes()
        
        if not changed_files:
            print("🔍 No changes detected, running all tests")
            return {category: info["tests"] for category, info in self.test_mapping.items()}
        
        tests_to_run = {}
        
        for category, info in self.test_mapping.items():
            should_run = False
            
            for trigger in info["triggers"]:
                for changed_file in changed_files:
                    if changed_file.startswith(trigger):
                        should_run = True
                        break
                if should_run:
                    break
            
            if should_run:
                tests_to_run[category] = info["tests"]
        
        return tests_to_run
    
    def run_test_category(self, category: str, test_files: List[str]) -> Dict:
        """Run tests in a specific category"""
        print(f"\n🧪 Running {category.upper()} tests...")
        print(f"📝 {self.test_mapping[category]['description']}")
        
        results = {
            "category": category,
            "tests_run": [],
            "passed": 0,
            "failed": 0,
            "errors": []
        }
        
        for test_file in test_files:
            test_path = self.project_root / test_file
            if not test_path.exists():
                print(f"⚠️ Test file not found: {test_file}")
                results["errors"].append(f"Test file not found: {test_file}")
                continue
            
            print(f"   Running: {test_file}")
            
            try:
                result = subprocess.run(
                    ["python3", str(test_path)],
                    capture_output=True,
                    text=True,
                    cwd=self.project_root
                )
                
                test_result = {
                    "file": test_file,
                    "exit_code": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "passed": result.returncode == 0
                }
                
                results["tests_run"].append(test_result)
                
                if result.returncode == 0:
                    results["passed"] += 1
                    print(f"      ✅ PASSED")
                else:
                    results["failed"] += 1
                    print(f"      ❌ FAILED (exit code: {result.returncode})")
                    if result.stderr:
                        print(f"         Error: {result.stderr[:200]}...")
                
            except Exception as e:
                results["failed"] += 1
                results["errors"].append(f"Exception running {test_file}: {str(e)}")
                print(f"      💥 ERROR: {e}")
        
        return results
    
    def save_test_results(self, all_results: Dict, version: str):
        """Save test results to versioned file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = self.test_results_dir / f"test_results_v{version}_{timestamp}.json"
        
        test_summary = {
            "version": version,
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_categories": len(all_results),
                "total_tests": sum(len(r["tests_run"]) for r in all_results.values()),
                "total_passed": sum(r["passed"] for r in all_results.values()),
                "total_failed": sum(r["failed"] for r in all_results.values()),
                "overall_status": "PASS" if sum(r["failed"] for r in all_results.values()) == 0 else "FAIL"
            },
            "results": all_results
        }
        
        with open(results_file, 'w') as f:
            json.dump(test_summary, f, indent=2)
        
        print(f"\n💾 Test results saved: {results_file}")
        return results_file
    
    def run_tests(self, categories: List[str] = None, changed_files: Set[str] = None) -> Dict:
        """Run tests based on categories or auto-detection"""
        current_version = self.version_manager.get_current_version()
        
        print(f"🚀 Fire Whisper Test Runner")
        print(f"🏷️  Version: {current_version}")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if categories:
            tests_to_run = {cat: self.test_mapping[cat]["tests"] for cat in categories if cat in self.test_mapping}
        else:
            tests_to_run = self.determine_tests_to_run(changed_files)
        
        if not tests_to_run:
            print("🤷 No tests to run based on changes detected")
            return {}
        
        print(f"\n📋 Tests to run: {', '.join(tests_to_run.keys())}")
        
        all_results = {}
        
        for category, test_files in tests_to_run.items():
            category_results = self.run_test_category(category, test_files)
            all_results[category] = category_results
        
        # Save results
        results_file = self.save_test_results(all_results, current_version)
        
        # Print summary
        self.print_test_summary(all_results)
        
        return all_results
    
    def print_test_summary(self, all_results: Dict):
        """Print test execution summary"""
        total_tests = sum(len(r["tests_run"]) for r in all_results.values())
        total_passed = sum(r["passed"] for r in all_results.values())
        total_failed = sum(r["failed"] for r in all_results.values())
        
        print(f"\n📊 TEST SUMMARY")
        print("=" * 50)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {total_passed}")
        print(f"❌ Failed: {total_failed}")
        
        if total_failed == 0:
            print(f"\n🎉 ALL TESTS PASSED!")
            print(f"✅ Code is ready for deployment")
        else:
            print(f"\n⚠️ {total_failed} TESTS FAILED")
            print(f"🔧 Fix issues before deployment")
        
        print("=" * 50)

if __name__ == "__main__":
    runner = TestRunner()
    
    if len(sys.argv) > 1:
        # Run specific categories
        categories = sys.argv[1:]
        runner.run_tests(categories=categories)
    else:
        # Auto-detect based on changes
        runner.run_tests()