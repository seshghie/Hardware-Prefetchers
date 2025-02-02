#!/bin/bash
#
#SBATCH --cpus-per-task=8
#SBATCH --time=40:00
#SBATCH --mem=4G

# Set trace directory
export TRACE_DIR=/data/dpc3_traces/

# Binary name
binary="perceptron-vinh_stride_256_4_histogram-no-no-lru-1core"

# Build the ChampSim binary once
echo "Building ChampSim binary..."
./build_champsim.sh perceptron vinh_stride_256_4_histogram no no lru 1

# Array of traces to run
traces=(
    "600.perlbench_s-210B.champsimtrace.xz"
    "602.gcc_s-734B.champsimtrace.xz"
    "628.pop2_s-17B.champsimtrace.xz"
    "638.imagick_s-10316B.champsimtrace.xz"
    "649.fotonik3d_s-1176B.champsimtrace.xz"
)

# Run simulations for each trace
for trace in "${traces[@]}"; do
    echo "Running simulation for ${trace}..."
    ./run_champsim.sh ${binary} 1 50 ${trace}
    
    # Extract benchmark name for the output file
    benchmark_name=$(echo ${trace} | cut -d'.' -f1,2)
    
    # Copy stride values with benchmark-specific name
    cp stride_values.txt ./plots/${benchmark_name}_stride.txt
    
    echo "Completed ${trace}"
    echo "------------------------"
done

echo "All simulations completed!"