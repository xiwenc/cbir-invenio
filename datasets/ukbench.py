import sys
import os
import shutil
import random

source = sys.argv[1]
count = int(sys.argv[2])

testset_dir = "ukbench-test"
trainingset_dir = "ukbench-training"


def rand():
    return int(random.random() * 10) % 4

fullset = sorted(os.listdir(source))
sampleset = fullset[:count]
testset = ["ukbench%05d.jpg" % (i + rand()) for i in range(0, count, 4)]
trainingset = set(sampleset) - set(testset)

for i in testset:
    assert "ukbench" in i
    shutil.copy2(os.path.join(source, i), testset_dir)

for i in trainingset:
    assert "ukbench" in i
    shutil.copy2(os.path.join(source, i), trainingset_dir)
