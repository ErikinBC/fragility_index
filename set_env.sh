#!/bin/bash

# Script to set conda environment

dir_conda=$(which conda | awk '{split($0,a,"/"); print a[4]}')
dir_conda=~/$dir_conda
dir_env=$dir_conda/envs
nchar_env=$(ls $dir_env | grep fragility | wc -l)

if [[ "$nchar_env" -eq 0 ]]; then
	echo "No environment fragility found"
	conda create --name fragility --file conda.env
else
	echo "fragility found"
	conda activate fragility
fi

