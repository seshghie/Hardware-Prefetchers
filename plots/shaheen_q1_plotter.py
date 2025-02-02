import os
import re
import matplotlib.pyplot as plt

# Function to parse execution time from correct line in result files
def parse_exec_time(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            # Look for line starting with "Finished CPU 0 instructions"
            if line.startswith('Finished CPU 0 instructions'):
                # Extract total sim time
                match = re.search(r'Simulation time: (\d+) hr (\d+) min (\d+) sec', line)
                if match:
                    hours = int(match.group(1))
                    minutes = int(match.group(2))
                    seconds = int(match.group(3))
                    # Convert sim time to seconds
                    total_seconds = hours * 3600 + minutes * 60 + seconds
                    return total_seconds
    return None

# Function to process benchmark results for each config
def process_results(benchmarks, config_1_suffix, config_2_suffix, results_dir):
    exec_times_1 = []
    exec_times_2 = []
    
    for benchmark in benchmarks:
        # File paths for each config
        file_1 = os.path.join(results_dir, f'{benchmark}{config_1_suffix}.txt')
        file_2 = os.path.join(results_dir, f'{benchmark}{config_2_suffix}.txt')
        
        # Parse exec times from both files
        time_1 = parse_exec_time(file_1)
        time_2 = parse_exec_time(file_2)
        
        if time_1 is not None and time_2 is not None:
            exec_times_1.append(time_1)
            exec_times_2.append(time_2)
    
    return exec_times_1, exec_times_2

# Function to plot exec times
def plot_exec_times(benchmarks, exec_times_1, exec_times_2):
    plt.figure(figsize=(12, 6))
    
    # Calculate bar positions
    x = range(len(benchmarks))
    width = 0.35  # Width of the bars
    
    # Create bars with proper offsets
    plt.bar([i - width/2 for i in x], exec_times_1, width, label="L1 next_line prefetcher")
    plt.bar([i + width/2 for i in x], exec_times_2, width, label="L2 next_line prefetcher")

    # Customize plot
    plt.xticks(x, benchmarks, rotation=45, ha='right')
    plt.xlabel('Benchmarks')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Execution Time for Different next_line Prefetcher Configs')
    plt.legend()
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    plt.savefig("q1_l1_vs_l2.png", bbox_inches='tight', dpi=300)

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

# Process result files
exec_times_1, exec_times_2 = process_results(benchmarks, config_1_suffix, config_2_suffix, results_dir)

# Plot exec times
plot_exec_times(benchmarks, exec_times_1, exec_times_2)