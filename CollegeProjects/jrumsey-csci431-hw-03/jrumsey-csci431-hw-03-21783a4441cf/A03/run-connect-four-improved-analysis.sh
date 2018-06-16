#!/bin/sh

python connect-four.py | tee connect-four-improved-experiment.csv

echo
echo "Running R..."
Rscript connect-four-improved-analysis.R

