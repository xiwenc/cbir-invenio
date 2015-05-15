import os
import operator

outfile = os.path.join('build', 'tags.dat')
mirflickr = os.path.join('datasets', 'mirflickr')

images = {}

for i in os.listdir(mirflickr):
    if i.startswith('tags'):
        with open(os.path.join(mirflickr, i), "r") as f:
            tags = [l.strip() for l in f.readlines()]
        images[i] = tags

all_tags = {}

for k, tags in images.iteritems():
    for tag in tags:
        if tag in all_tags:
            all_tags[tag] = all_tags[tag] + 1
        else:
            all_tags[tag] = 1


sorted_tags = sorted(all_tags.iteritems(), key=operator.itemgetter(1), reverse=True)[:20]

with open(outfile, 'w') as f:
    f.write('Tags\tFrequency\n')
    for k, v in sorted_tags:
        f.write('{name}\t{count}\n'.format(name=k, count=v))
