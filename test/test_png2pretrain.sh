#!/bin/bash

echo "--- Test png2pretrain ---"

echo "Test 1: Error: number of argument != 3 (2)"
python ../process/png2pretrain.py test-png2pretrain/
echo -e "\n"

echo "Test 2: Error: number of argument != 3 (4)"
python ../process/png2pretrain.py test-png2pretrain/ test-png2pretrain/ test-png2pretrain/
echo -e "\n"

echo "Test 3: Error: image dir is not a directory"
python ../process/png2pretrain.py blankfile test-png2pretrain/
echo -e "\n"

echo "Test 4: Error: output dir is not a directory "
python ../process/png2pretrain.py test-png2pretrain/ blankfile
echo -e "\n"

echo "Test 5: Good: output dir do not exist"
python ../process/png2pretrain.py test-png2pretrain/1/ test-png2pretrain3/
echo -e "\n"

echo "Test 6: Good: output dir exist"
python ../process/png2pretrain.py test-png2pretrain/2/ test-png2pretrain2/
echo -e "\n"
