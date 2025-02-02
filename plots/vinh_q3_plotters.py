import os
import re
import matplotlib.pyplot as plt

def parse_prefetch_stats(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        
        # Extract only useful prefetches
        useful_match = re.search(r'Core_0_L1D_prefetch_useful (\d+)', content)
        
        if useful_match:
            return int(useful_match.group(1))
    return None

def analyze_prefetch_sizes(benchmarks, sizes, results_dir):
    useful_counts = {benchmark: [] for benchmark in benchmarks}
    
    for benchmark in benchmarks:
        for size in sizes:
            file_name = f"{benchmark}.champsimtrace.xz-perceptron-vinh_stride_{size}-no-no-lru-1core.txt"
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
    
    # Custom x-ticks
    x_ticks = [64, 128, 256, 512, 1024]
    x_labels = ['2^6', '2^7', '2^8', '2^9', '2^10']
    
    plt.xticks(x_ticks, x_labels)  # Set custom labels for x-axis
    
    plt.xscale('log', base=2)  # Use log scale base 2 for x-axis
    plt.yscale('log')  # Use log scale for y-axis
    
    plt.xlabel('log2(byte size)')
    plt.ylabel('Number of Useful Prefetches')
    plt.title('L1 D-cache Useful Prefetches vs. Table Prefetch Size')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.savefig('prefetch_useful_counts_log.png', bbox_inches='tight', dpi=300)

# Benchmark list
benchmarks = [
    "600.perlbench_s-210B",
    "602.gcc_s-734B",
    "628.pop2_s-17B",
    "638.imagick_s-10316B",
    "649.fotonik3d_s-1176B"
]

# Prefetch sizes to analyze
sizes = [64, 128, 256, 512, 1024]

# Results directory
results_dir = "../results_10M/"

# Analyze results
useful_counts = analyze_prefetch_sizes(benchmarks, sizes, results_dir)

# Create plot
plot_useful_counts(useful_counts, sizes)
