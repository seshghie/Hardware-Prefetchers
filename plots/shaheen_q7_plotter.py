import os
import re
import matplotlib.pyplot as plt

def parse_prefetch_stats(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        
        # Extract only useful prefetches
        useful_match = re.search(r'Core_0_L2C_prefetch_useful (\d+)', content)
        
        if useful_match:
            return int(useful_match.group(1))
    return None

def analyze_prefetch_sizes(benchmarks, sizes, results_dir):
    useful_counts = {benchmark: [] for benchmark in benchmarks}
    
    for benchmark in benchmarks:
        for size in sizes:
            file_name = f"{benchmark}.champsimtrace.xz-perceptron-no-shaheen_ghb_d{size}-no-lru-1core.txt"
            file_path = os.path.join(results_dir, file_name)
            
            useful_count = parse_prefetch_stats(file_path)
            if useful_count is not None:
                useful_counts[benchmark].append(useful_count)
            else:
                useful_counts[benchmark].append(0)
    
    return useful_counts

def plot_useful_counts(useful_counts, sizes):
    plt.figure(figsize=(10, 6))
    
    # Plot line for each benchmark with different markers
    markers = ['o', 's', 'D', '+', '<', '>']
    for (benchmark, counts), marker in zip(useful_counts.items(), markers):
        # Extract benchmark name without the full path
        bench_name = benchmark.split('/')[-1].split('.')[0]
        plt.plot(sizes, counts, marker=marker, label=bench_name, linewidth=1.5, markersize=8)
    
    plt.xscale('log', base=2)  # Use log scale base 2 for x-axis
    plt.yscale('log')  # Use log scale for y-axis
    
    plt.xlabel('log2(byte size)')
    plt.ylabel('Number of Useful Prefetches')
    plt.title('Global History Stride L2C Useful Prefetches vs. Prefetch degree on 256')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.savefig('q7_ghb_d_perf.png', bbox_inches='tight', dpi=300)

# Benchmark list
benchmarks = [
    "600.perlbench_s-210B",
    "602.gcc_s-734B",
    "628.pop2_s-17B",
    "638.imagick_s-10316B",
    "649.fotonik3d_s-1176B"
]

# Prefetch sizes to analyze
sizes = [1, 2, 4, 8, 16]

# Results directory
results_dir = "../results_10M/"

# Analyze results
useful_counts = analyze_prefetch_sizes(benchmarks, sizes, results_dir)

# Create plot
plot_useful_counts(useful_counts, sizes)
