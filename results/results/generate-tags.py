import sys

sys.path.append('../src/')
from utils import mirflickr_images  # noqa

sorted_names, results_tags, results_matches = mirflickr_images()

print("x\tTags_Count\tPerfect_Matches")
for name in sorted_names:
    print("%s\t%d\t%d" % (name, results_tags[name], results_matches[name]))
