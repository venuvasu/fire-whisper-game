#!/usr/bin/env python3
"""
Architecture Balance Test
Run systematic tests to find optimal AI/Code responsibility split.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from looma.core.architecture_tester import ArchitectureTester

def main():
    """Run comprehensive architecture testing"""
    
    print("🎯 Architecture Balance Testing")
    print("=" * 50)
    print("Goal: Find optimal AI/Code responsibility split")
    print("Method: Systematic testing of different architectures")
    print()
    
    tester = ArchitectureTester()
    
    # Run comprehensive tests
    results = tester.run_comprehensive_test()
    
    # Calculate balance scores
    balance_scores = tester.calculate_balance_scores(results)
    
    print("\n🏆 BALANCE SCORES (Higher = Better Sweet Spot)")
    print("=" * 50)
    for arch_name, score in sorted(balance_scores.items(), key=lambda x: x[1], reverse=True):
        print(f"{arch_name:20} | {score:.3f}")
    
    # Generate recommendations
    recommendations = tester.generate_recommendations(results, balance_scores)
    
    print(f"\n🎯 OPTIMAL ARCHITECTURE: {recommendations['optimal_architecture']}")
    print(f"Balance Score: {recommendations['balance_score']:.3f}")
    
    print("\n💡 KEY INSIGHTS:")
    for insight in recommendations['key_insights']:
        print(f"  • {insight}")
    
    print("\n📋 RECOMMENDATIONS:")
    for rec in recommendations['specific_recommendations']:
        print(f"  • {rec}")
    
    # Save detailed results
    tester.save_results(results)
    
    print("\n✅ Architecture testing complete!")
    print("Use these results to configure your optimal game architecture.")

if __name__ == "__main__":
    main()