#!/usr/bin/env python3
"""
Prime Number RT Experiment - Data Analysis Script
Python version

This script analyzes data from the Prime Number RT experiment
Usage: python analyze_data.py <data_file.csv>
"""

import sys
import pandas as pd
import numpy as np
from scipy import stats


def analyze_participant(data_file):
    """Analyze a single participant's data from the Prime Number RT experiment."""

    print("=" * 50)
    print("Prime Number RT Experiment Analysis")
    print("=" * 50)
    print()

    # Load data
    print(f"Loading data from: {data_file}\n")
    data = pd.read_csv(data_file)

    # Basic info
    print(f"Participant ID: {data['participantId'].unique()[0]}")
    print(f"Total trials: {len(data)}")
    print(f"Blocks completed: {data['block'].max()}\n")

    # Overall accuracy
    accuracy = data['accuracy'].mean() * 100
    print(f"Overall Accuracy: {accuracy:.2f}%\n")

    # Filter to correct trials for RT analysis
    correct_data = data[data['accuracy'] == 1].copy()

    # Overall RT
    print("--- Reaction Time Analysis (Correct Trials Only) ---")
    print(f"Mean RT: {correct_data['reactionTime'].mean():.1f} ms")
    print(f"Median RT: {correct_data['reactionTime'].median():.1f} ms")
    print(f"SD RT: {correct_data['reactionTime'].std():.1f} ms\n")

    # RT by response type
    print("--- RT by Number Type ---")
    rt_by_type = correct_data.groupby('correctResponse')['reactionTime'].agg([
        ('n', 'count'),
        ('mean_rt', 'mean'),
        ('sd_rt', 'std'),
        ('median_rt', 'median')
    ]).round(1)
    print(rt_by_type)

    # Prime effect
    prime_rt = rt_by_type.loc['prime', 'mean_rt']
    not_prime_rt = rt_by_type.loc['not_prime', 'mean_rt']
    prime_effect = prime_rt - not_prime_rt
    print(f"\nPrime Effect (Prime - Not Prime): {prime_effect:.1f} ms\n")

    # Magnitude effect (for primes only)
    print("--- RT by Prime Magnitude ---")
    prime_data = correct_data[correct_data['correctResponse'] == 'prime'].copy()
    prime_data['magnitude'] = prime_data['stimulus'].apply(
        lambda x: 'small (<20)' if x < 20 else 'large (≥20)'
    )

    prime_magnitude = prime_data.groupby('magnitude')['reactionTime'].agg([
        ('n', 'count'),
        ('mean_rt', 'mean'),
        ('sd_rt', 'std'),
        ('median_rt', 'median')
    ]).round(1)
    print(prime_magnitude)

    # Magnitude effect
    if len(prime_magnitude) == 2:
        small_rt = prime_magnitude.loc['small (<20)', 'mean_rt']
        large_rt = prime_magnitude.loc['large (≥20)', 'mean_rt']
        magnitude_effect = large_rt - small_rt
        print(f"\nMagnitude Effect (Large - Small): {magnitude_effect:.1f} ms\n")

    # Accuracy by number type
    print("--- Accuracy by Number Type ---")
    acc_by_type = data.groupby('correctResponse').agg({
        'accuracy': ['count', lambda x: (x.mean() * 100)]
    }).round(2)
    acc_by_type.columns = ['n', 'accuracy (%)']
    print(acc_by_type)
    print()

    # Block-by-block performance
    print("--- Performance by Block ---")
    main_blocks = data[data['block'] != 'practice'].copy()
    block_performance = main_blocks.groupby('block').agg({
        'accuracy': ['count', lambda x: (x.mean() * 100)],
        'reactionTime': lambda x: x[main_blocks.loc[x.index, 'accuracy'] == 1].mean()
    }).round(1)
    block_performance.columns = ['n', 'accuracy (%)', 'mean_rt (correct)']
    print(block_performance)
    print()

    # Individual stimulus analysis
    print("--- Performance by Stimulus ---")
    stimulus_performance = correct_data.groupby(['stimulus', 'correctResponse'])['reactionTime'].agg([
        ('n', 'count'),
        ('mean_rt', 'mean'),
        ('sd_rt', 'std')
    ]).round(1)
    print(stimulus_performance.sort_index())

    # Statistical tests
    print("\n--- Statistical Tests ---")

    # t-test for prime effect
    prime_rts = correct_data[correct_data['correctResponse'] == 'prime']['reactionTime']
    not_prime_rts = correct_data[correct_data['correctResponse'] == 'not_prime']['reactionTime']

    t_stat, p_value = stats.ttest_ind(prime_rts, not_prime_rts)
    print(f"\nPrime vs Not Prime (independent t-test):")
    print(f"  t = {t_stat:.3f}")
    print(f"  df = {len(prime_rts) + len(not_prime_rts) - 2}")
    print(f"  p = {p_value:.4f}")
    print(f"  Cohen's d = {cohens_d(prime_rts, not_prime_rts):.3f}")

    # t-test for magnitude effect (primes only)
    small_prime_rts = prime_data[prime_data['stimulus'] < 20]['reactionTime']
    large_prime_rts = prime_data[prime_data['stimulus'] >= 20]['reactionTime']

    if len(small_prime_rts) > 0 and len(large_prime_rts) > 0:
        t_stat_mag, p_value_mag = stats.ttest_ind(large_prime_rts, small_prime_rts)
        print(f"\nSmall vs Large Primes (independent t-test):")
        print(f"  t = {t_stat_mag:.3f}")
        print(f"  df = {len(small_prime_rts) + len(large_prime_rts) - 2}")
        print(f"  p = {p_value_mag:.4f}")
        print(f"  Cohen's d = {cohens_d(large_prime_rts, small_prime_rts):.3f}")

    print("\n" + "=" * 50)
    print("Analysis Complete")
    print("=" * 50)

    return {
        'data': data,
        'correct_data': correct_data,
        'rt_by_type': rt_by_type,
        'prime_effect': prime_effect,
        'prime_magnitude': prime_magnitude,
        'stimulus_performance': stimulus_performance
    }


def cohens_d(group1, group2):
    """Calculate Cohen's d effect size."""
    n1, n2 = len(group1), len(group2)
    var1, var2 = group1.var(), group2.var()
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    return (group1.mean() - group2.mean()) / pooled_std


def main():
    """Main entry point for command-line usage."""
    if len(sys.argv) < 2:
        print("Error: No data file specified")
        print("Usage: python analyze_data.py <data_file.csv>")
        sys.exit(1)

    data_file = sys.argv[1]

    try:
        analyze_participant(data_file)
    except FileNotFoundError:
        print(f"Error: File not found: {data_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error analyzing data: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
