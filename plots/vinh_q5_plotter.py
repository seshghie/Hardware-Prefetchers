import os
import numpy as np
import matplotlib.pyplot as plt

def parse_stride_file(file_path):
    """Parse stride values from a file and return non-zero values."""
    with open(file_path, 'r') as file:
        # Read all lines and convert to integers, filtering out empty lines
        strides = [int(line.strip()) for line in file if line.strip()]
        # Filter out zeros since they're not interesting for the histogram
        non_zero_strides = [s for s in strides if s != 0]
    return non_zero_strides

def analyze_stride_patterns(benchmark_files):
    """Analyze stride patterns for all benchmarks."""
    stride_data = {}
    
    for file_name in benchmark_files:
        try:
            if os.path.exists(file_name):
                strides = parse_stride_file(file_name)
                if strides:  # Only add if we have non-zero strides
                    # Extract benchmark name from file name
                    bench_name = file_name.split('_stride.txt')[0]
                    stride_data[bench_name] = strides
            else:
                print(f"Warning: Stride file not found: {file_name}")
        except Exception as e:
            print(f"Error processing {file_name}: {str(e)}")
    
    return stride_data

def plot_single_histogram(benchmark, strides, output_dir='stride_plots'):
    """Create and save histogram for a single benchmark."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create new figure
    plt.figure(figsize=(12, 6))
    
    # Calculate bin edges to capture the range of values
    max_abs_stride = max(abs(min(strides)), abs(max(strides)))
    bins = np.linspace(-max_abs_stride, max_abs_stride, 50)
    
    # Create histogram
    plt.hist(strides, bins=bins, edgecolor='black', alpha=0.7)
    
    # Set title and labels
    plt.title(f'Stride Distribution - {benchmark}', fontsize=14, pad=20)
    plt.xlabel('Stride Value', fontsize=12)
    plt.ylabel('Frequency (log scale)', fontsize=12)
    
    # Add grid
    plt.grid(True, alpha=0.3)
    
    # Use log scale for y-axis
    plt.yscale('log')
    
    # Add mean and median lines
    mean_stride = np.mean(strides)
    median_stride = np.median(strides)
    plt.axvline(mean_stride, color='r', linestyle='--', alpha=0.5, label=f'Mean: {mean_stride:.2f}')
    plt.axvline(median_stride, color='g', linestyle='--', alpha=0.5, label=f'Median: {median_stride:.2f}')
    
    # Add legend
    plt.legend()
    
    # Adjust layout
    plt.tight_layout()
    
    # Save plot
    output_file = os.path.join(output_dir, f'{benchmark}_stride_histogram.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_file

# List your benchmark files with exact names
benchmark_files = [
    "600.perlbench_s-210B_stride.txt",
    "602.gcc_s-734B_stride.txt",
    "628.pop2_s-17B_stride.txt",
    "638.imagick_s-10316B_stride.txt",
    "649.fotonik3d_s-1176B_stride.txt"
]

# Print current directory and list files for debugging
print("Current directory:", os.getcwd())
print("Files in directory:", os.listdir())

# Analyze stride patterns
stride_data = analyze_stride_patterns(benchmark_files)

if stride_data:
    # Create individual plots and print statistics
    print("\nStride Pattern Summary Statistics:")
    print("-" * 50)
    
    for benchmark, strides in stride_data.items():
        if strides:
            # Create and save plot
            output_file = plot_single_histogram(benchmark, strides)
            print(f"\n{benchmark}:")
            print(f"Plot saved as: {output_file}")
            print(f"Total non-zero strides: {len(strides)}")
            print(f"Mean stride: {np.mean(strides):.2f}")
            print(f"Median stride: {np.median(strides):.2f}")
            print(f"Min stride: {min(strides)}")
            print(f"Max stride: {max(strides)}")
            print(f"Standard deviation: {np.std(strides):.2f}")
else:
    print("No stride data was found to analyze!")