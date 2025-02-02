import os
import matplotlib.pyplot as plt

# Function to parse useful and useless prefetch counts from result files
def parse_prefetch_counts(file_path, useful_key, useless_key):
    useful_prefetches = 0
    useless_prefetches = 0
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith(useful_key):
                useful_prefetches = int(line.split()[-1])
            elif line.startswith(useless_key):
                useless_prefetches = int(line.split()[-1])
    return useful_prefetches, useless_prefetches

# Function to process benchmark results for each config
def process_results(benchmarks, config_1_suffix, config_2_suffix, results_dir):
    l1_useful, l1_useless = [], []
    l2_useful, l2_useless = [], []
    
    for benchmark in benchmarks:
        # File path for L1 config (suffix 1)
        file_1 = os.path.join(results_dir, f'{benchmark}{config_1_suffix}.txt')
        useful_1, useless_1 = parse_prefetch_counts(file_1, 'Core_0_L1D_prefetch_useful', 'Core_0_L1D_prefetch_useless')
        l1_useful.append(useful_1)
        l1_useless.append(useless_1)
        
        # File path for L2 config (suffix 2)
        file_2 = os.path.join(results_dir, f'{benchmark}{config_2_suffix}.txt')
        useful_2, useless_2 = parse_prefetch_counts(file_2, 'Core_0_L2C_prefetch_useful', 'Core_0_L2C_prefetch_useless')
        l2_useful.append(useful_2)
        l2_useless.append(useless_2)
    
    return l1_useful, l1_useless, l2_useful, l2_useless


# Function to plot prefetch counts
def plot_prefetch_counts(benchmarks, l1_useful, l1_useless, l2_useful, l2_useless):
    x = range(len(benchmarks))
    width = 0.2

    plt.figure(figsize=(12, 6))
    
    # L1 Prefetcher
    plt.bar([i - width for i in x], l1_useful, width=width, color='blue', label="L1 Useful")
    plt.bar([i for i in x], l1_useless, width=width, color='cyan', label="L1 Useless")
    
    # L2 Prefetcher
    plt.bar([i + width for i in x], l2_useful, width=width, color='red', label="L2 Useful")
    plt.bar([i + 2*width for i in x], l2_useless, width=width, color='orange', label="L2 Useless")

    plt.xticks(x, benchmarks, rotation=45)
    plt.xlabel('Benchmarks')
    plt.ylabel('Prefetch Counts')
    plt.title('Useful/Useless Prefetch Counts for L1 and L2 Prefetcher Configs')
    plt.legend()
    plt.tight_layout()
    plt.savefig("q2_prefetch_counts.png")

benchmarks = [
    "600.perlbench_s-210B",
    "602.gcc_s-734B",
    "628.pop2_s-17B",
    "638.imagick_s-10316B",
    "649.fotonik3d_s-1176B"
]

# Suffixes for each config
config_1_suffix = '.champsimtrace.xz-perceptron-next_line-no-no-lru-1core'
config_2_suffix = '.champsimtrace.xz-perceptron-no-next_line-no-lru-1core'

results_dir = "../results_50M/"

# Process result files for useful/useless prefetch counts
l1_useful, l1_useless, l2_useful, l2_useless = process_results(benchmarks, config_1_suffix, config_2_suffix, results_dir)

# Plot prefetch counts
plot_prefetch_counts(benchmarks, l1_useful, l1_useless, l2_useful, l2_useless)