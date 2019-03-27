#!/bin/bash

echo "--- Test png2train ---"

echo "Test 1: Error: number of argument != 2 (1)"
python ../src_final/png2train.py
echo -e "\n"

echo "Test 2: Error: number of argument != 2 (3)"
python ../src_final/png2train.py test-png2train.png a/
echo -e "\n"

echo "Test 3: Error: image dir is not a png file"
python ../src_final/png2train.py notpng.jpg
echo -e "\n"

echo "Test 4: Error: image dir is not a valid image"
python ../src_final/png2train.py notvalidpng.png
echo -e "\n"

echo "Test 5: Good, check the result tree view"
python ../src_final/png2train.py test-png2train.png
echo -e "\n"
