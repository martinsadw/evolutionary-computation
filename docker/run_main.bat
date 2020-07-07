@echo off
cls
python -m generate_comparison instances\andre\500\instance.txt -n results\test.pickle -b 100000 -r 5
