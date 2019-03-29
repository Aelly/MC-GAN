#!/bin/bash

echo "--- Test png2train ---"

echo "Test 1: Error: number of argument != 2 (1)"
python ../process/png2train.py
echo -e "\n"

echo "Test 2: Error: number of argument != 2 (3)"
python ../process/png2train.py test-png2train.png a/
echo -e "\n"

echo "Test 3: Error: [PNG file] is not a png file"
python ../process/png2train.py notpng.jpg
echo -e "\n"

echo "Test 4: Error: [PNG file] is not a valid image"
python ../process/png2train.py notvalidpng.png
echo -e "\n"

echo "Test 5: Good, check the result tree view"
python ../process/png2train.py test-png2train.png
echo -e "\n"
