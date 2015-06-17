import sys
import os

sys.path.append('src/')
from utils import extract_tags

file1 = sys.argv[1]

with open(file1, 'r') as f1:
    lines1 = [l.strip() for l in f1.readlines()]

def generate_graphics_statement(image_path, width='.5in'):
    return "\\includegraphics[keepaspectratio=false, height=%s, width=%s]{%s}" % (width, width, image_path)


targets = {}
current_tags = None
for line in lines1:
    if line.startswith('src'):
        continue

    if 'datasets' in line:
        if line.startswith('datasets'):
            current = line.split()[0]
            targets[current] = []
            current_tags = extract_tags(current)
        else:
            image_path = line.split()[1]
            if len(targets[current]) >= 4:
                continue
            tags = extract_tags(image_path)
            targets[current].append((image_path, set(tags).intersection(set(current_tags))))

from pprint import pprint

# fix up self
for k, v in targets.iteritems():
    others = []
    for i in range(1, 4):
        image_path, tags = targets[k][i]
        others.extend(tags)
    me_path, me_tags = targets[k][0]
    assert len(me_tags) > 0
    targets[k][0] = (me_path, set(me_tags) & set(others))

print '\\begin{tabularx}{.48\\textwidth}{ X X X X }\\\\\n'
for k, v in targets.iteritems():
    tags_line = ''
    first = True
    for image in targets[k]:
        image_path, image_tags = image
        tags = ', '.join(image_tags)
        if tags == '':
            tags = '--'
        if first:
            first = False
        else:
            print ' & '
            tags_line = tags_line + ' & '
        print generate_graphics_statement('../' + image_path)
        tags_line = tags_line + tags
    print '\\\\'
    tags_line = tags_line + '\\\\'
    print tags_line
print '\\end{tabularx}\n'
