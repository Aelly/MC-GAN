#!/bin/bash

echo "--- Test chars2png ---"

echo "Test 1: Error: number of argument != 2 (1)"
python ../src_final/chars2png.py
echo -e "\n"

echo "Test 2: Error: number of argument != 2 (3)"
python ../src_final/chars2png.py test-manto-sample/ a/
echo -e "\n"

echo "Test 3: Error: image dir is not a directory"
python ../src_final/chars2png.py a/
echo -e "\n"

echo "Test 4: Error: dataset name can't contain '_' "
python ../src_final/chars2png.py test_manto_sample/
echo -e "\n"

echo "Test 5: Error: not enough png file in image dir"
python ../src_final/chars2png.py test-manto-sample-1/
echo -e "\n"

echo "Test 6: Good: (without / at the end of dir)"
python ../src_final/chars2png.py test-manto-sample
echo -e "\n"

echo "Test 7: Good, check the result image"
python ../src_final/chars2png.py test-manto-sample/
echo -e "\n"
