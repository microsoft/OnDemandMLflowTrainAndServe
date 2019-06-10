#!/bin/bash
set -e

# Adding new *.whl files to the requirements of the Prediction service
cd model-runner

echo "" >> requirements-dev.txt
ls *.whl -p | grep -v / >> requirements-dev.txt

echo "Contents of requirements-dev.txt:"
cat requirements-dev.txt

echo "" >> requirements.txt
ls *.whl -p | grep -v / >> requirements.txt

echo "Contents of requirements.txt:"
cat requirements.txt

cd ..
