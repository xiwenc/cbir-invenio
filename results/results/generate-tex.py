import sys
import os

sys.path.append('src/')
from utils import extract_tags

if len(sys.argv) == 2:
    tokens = sys.argv[1].split("-")
    dataset_path = tokens[0]
    dataset = dataset_path.split("/")[1]
    output = tokens[1].replace(".dat", "")
else:
    dataset = sys.argv[1]
    dataset_path = os.path.join("build", dataset)
    output = sys.argv[2]

def generate_graphics_statement(image_path, width='.5in'):
    return "\\includegraphics[keepaspectratio=false, height=%s, width=%s]{%s}" % (width, width, image_path)


def generate

print('\\begin{tabularx}{.48\\textwidth}{ X X X X }\\\\')
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
            print(' & ')
            tags_line = tags_line + ' & '
        print(generate_graphics_statement('../' + image_path))
        tags_line = tags_line + tags
    print('\\\\')
    tags_line = tags_line + '\\\\'
    print(tags_line)
print('\\end{tabularx}')
