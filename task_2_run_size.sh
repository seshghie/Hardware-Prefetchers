#!/bin/bash
#
#SBATCH --cpus-per-task=8
#SBATCH --time=40:00
#SBATCH --mem=4G

export TRACE_DIR=/data/dpc3_traces/
branch="perceptron"
L1_prefetcher="vinh_stride"
binary="perceptron-vinh_stride"

# Define an array of values to process
values=(64 128 256 512 1024)

# Loop through each value
for value in "${values[@]}"; do
    # Construct the binary name with the current value
    ./build_champsim.sh ${branch} ${L1_prefetcher}_${value} no no lru 1  

    full_binary="${binary}_${value}-no-no-lru-1core"
    
    # Run the command for each trace file
    ./run_champsim.sh ${full_binary} 1 10 600.perlbench_s-210B.champsimtrace.xz
    ./run_champsim.sh ${full_binary} 1 10 602.gcc_s-734B.champsimtrace.xz
    ./run_champsim.sh ${full_binary} 1 10 628.pop2_s-17B.champsimtrace.xz
    ./run_champsim.sh ${full_binary} 1 10 638.imagick_s-10316B.champsimtrace.xz
    ./run_champsim.sh ${full_binary} 1 10 649.fotonik3d_s-1176B.champsimtrace.xz
done
