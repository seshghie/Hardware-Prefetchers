#!/bin/bash
#
#SBATCH --cpus-per-task=8
#SBATCH --time=40:00
#SBATCH --mem=4G

export TRACE_DIR=/data/dpc3_traces/
binary="perceptron-no-shaheen_ghb_d16-no-lru-1core"
./run_champsim.sh ${binary} 1 10 600.perlbench_s-210B.champsimtrace.xz
./run_champsim.sh ${binary} 1 10 602.gcc_s-734B.champsimtrace.xz
./run_champsim.sh ${binary} 1 10 628.pop2_s-17B.champsimtrace.xz
./run_champsim.sh ${binary} 1 10 638.imagick_s-10316B.champsimtrace.xz
./run_champsim.sh ${binary} 1 10 649.fotonik3d_s-1176B.champsimtrace.xz






