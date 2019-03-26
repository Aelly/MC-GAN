#!/bin/bash

echo "--- Test chars2png ---"

echo "Test 1: Error: number of argument != 3 (2)"
python ../src_final/font2png.py test-font/
echo -e "\n"

echo "Test 2: Error: number of argument != 3 (4)"
python ../src_final/font2png.py test-font/ test-font/ test-font/
echo -e "\n"

echo "Test 3: Error: font dir is not a directory"
python ../src_final/font2png.py a/ test-font/
echo -e "\n"

echo "Test 4: Error: output dir is not a directory"
python ../src_final/font2png.py test-font/ blankfile
echo -e "\n"

echo "Test 5: Good: output dir do not exist"
python ../src_final/font2png.py test-font/ test-fontpng2/
echo -e "\n"

echo "Test 6: Good: output dir exist"
python ../src_final/font2png.py test-font/ test-fontpng/
echo -e "\n"
