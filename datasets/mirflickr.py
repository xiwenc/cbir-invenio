import sys
import os
import shutil
import random

source = sys.argv[1]
count = int(sys.argv[2])


def get_tags_file(im):
    return im.replace("im", "tags").replace(".jpg", ".txt")

testset_dir = "mirflickr-test"
trainingset_dir = "mirflickr-training"
fullset = [f for f in os.listdir(source) if f.startswith("im")]
random.shuffle(fullset)
sampleset = fullset[:count]
testset = sampleset[:int(count / 4)]
trainingset = set(sampleset) - set(testset)

for i in testset:
    shutil.copy2(os.path.join(source, i), testset_dir)
    shutil.copy2(os.path.join(source, "meta", "tags", get_tags_file(i)),
                 testset_dir)

for i in trainingset:
    shutil.copy2(os.path.join(source, i), trainingset_dir)
    shutil.copy2(os.path.join(source, "meta", "tags", get_tags_file(i)),
                 trainingset_dir)
