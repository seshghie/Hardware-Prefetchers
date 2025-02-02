import os
import re
import matplotlib.pyplot as plt
import numpy as np

def extract_prefetch_stats(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

        # Extract prefetch hit, miss, and issued statistics
        prefetch_hit_match = re.search(r'Core_0_L1D_prefetch_hit (\d+)', content)
        prefetch_miss_match = re.search(r'Core_0_L1D_prefetch_miss (\d+)', content)
        prefetch_issued_match = re.search(r'Core_0_L1D_prefetch_issued (\d+)', content)

        if prefetch_hit_match and prefetch_miss_match and prefetch_issued_match:
            prefetch_hit = int(prefetch_hit_match.group(1))
            prefetch_miss = int(prefetch_miss_match.group(1))
            prefetch_issued = int(prefetch_issued_match.group(1))
            return prefetch_hit, prefetch_miss, prefetch_issued
    return None, None, None

def extract_prefetch_stats_on_L2(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

        # Extract prefetch hit, miss, and issued statistics
        prefetch_hit_match = re.search(r'Core_0_L2C_prefetch_hit (\d+)', content)
        prefetch_miss_match = re.search(r'Core_0_L2C_prefetch_miss (\d+)', content)
        prefetch_issued_match = re.search(r'Core_0_L2C_prefetch_issued (\d+)', content)

        if prefetch_hit_match and prefetch_miss_match and prefetch_issued_match:
            prefetch_hit = int(prefetch_hit_match.group(1))
            prefetch_miss = int(prefetch_miss_match.group(1))
            prefetch_issued = int(prefetch_issued_match.group(1))
            return prefetch_hit, prefetch_miss, prefetch_issued
    return None, None, None

def compare_prefetch_stats(benchmarks, results_dir):
    stats = {}

    for benchmark in benchmarks:
        stride_stats = extract_prefetch_stats(os.path.join(results_dir, f"{benchmark}.champsimtrace.xz-perceptron-vinh_stride_256_4-no-no-lru-1core.txt"))
        ghb_stats = extract_prefetch_stats_on_L2(os.path.join(results_dir, f"{benchmark}.champsimtrace.xz-perceptron-no-shaheen_ghb-no-lru-1core.txt"))

        if stride_stats[2] > 0:
            stride_hit_issued_ratio = stride_stats[0] / stride_stats[2]
        else:
            stride_hit_issued_ratio = 0

        if ghb_stats[2] > 0:
            ghb_hit_issued_ratio = ghb_stats[0] / ghb_stats[2]
        else:
            ghb_hit_issued_ratio = 0

        stats[benchmark] = {
            'stride_hit_issued_ratio': stride_hit_issued_ratio,
            'ghb_hit_issued_ratio': ghb_hit_issued_ratio
        }

    return stats

def plot_prefetch_stats(prefetch_stats):
    plt.figure(figsize=(12, 8))

    # Extract benchmark names
    benchmarks = list(prefetch_stats.keys())

    # Plot prefetch hit/issued ratio for each benchmark
    x = np.arange(len(benchmarks))
    width = 0.4

    plt.bar(x - width/2, [prefetch_stats[b]['stride_hit_issued_ratio'] for b in benchmarks], width, label='Stride Hit/Issued Ratio')
    plt.bar(x + width/2, [prefetch_stats[b]['ghb_hit_issued_ratio'] for b in benchmarks], width, label='GHB Hit/Issued Ratio')

    plt.xticks(x, benchmarks, rotation=45, ha='right')
    plt.xlabel('Benchmark')
    plt.ylabel('Prefetch Hit/Issued Ratio')
    plt.title('Prefetch Statistics: Stride vs GHB')
    plt.legend()
    plt.tight_layout()
    plt.savefig('ghb_vs_stride.png', dpi=300)

# Benchmark list
benchmarks = [
    "600.perlbench_s-210B",
    "602.gcc_s-734B",
    "628.pop2_s-17B",
    "638.imagick_s-10316B",
    "649.fotonik3d_s-1176B"
]

# Results directory
results_dir = "../results_10M/"

# Compare prefetch stats
prefetch_stats = compare_prefetch_stats(benchmarks, results_dir)

# Plot prefetch statistics
plot_prefetch_stats(prefetch_stats)