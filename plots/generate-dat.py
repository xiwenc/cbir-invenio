import sys
import os
import operator

sys.path.append('src/')
from utils import result_test_ukbench, recall, precision, result_test_mirflickr


dataset = sys.argv[1]
dataset_path = os.path.join("build", dataset)

all_files = os.listdir(dataset_path)
configs = filter(lambda x: x.endswith('.txt'), all_files)

recalls = {}
precisions = {}
image_names = []
labels = []
results = {}
for config in configs:
    label = config.replace(".txt", "")
#    label = label.replace('surf', 'sur')
#    label = label.replace('sift', 'sif')
#    label = label.replace('kmeans', 'kme')
#    label = label.replace('images', 'img')
#    label = label.replace('segments', 'seg')
    labels.append(label)
    recalls[label] = {}
    precisions[label] = {}
    results[label] = {}
    path = os.path.join(dataset_path, config)
    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    for line in lines:
        if line.startswith('# '):
            tokens = line.split()
            name = os.path.basename(tokens[1])
            results[label][image_name].append(name)

        if line.startswith('datasets'):
            tokens = line.split("\t")
            image_name = os.path.basename(tokens[0])
            recalls[label][image_name] = float(tokens[1])
            precisions[label][image_name] = float(tokens[2])
            results[label][image_name] = []
            if image_name not in image_names:
                image_names.append(image_name)

recalls_image_names = {}
precisions_image_names = {}
for image_name in image_names:
    recalls_image_names[image_name] = []
    precisions_image_names[image_name] = []

for k, v in recalls.iteritems():
    for r, s in v.iteritems():
        recalls_image_names[r].append(s)

for k, v in precisions.iteritems():
    for r, s in v.iteritems():
        precisions_image_names[r].append(s)


for label, s in results.iteritems():
    for target_image, retrieved in s.iteritems():
        if dataset == 'ukbench':
            retrieved_filenames = retrieved[:4]
            recall_value = recall(target_image,
                                  retrieved_filenames,
                                  retrieved,
                                  method=result_test_ukbench
                                  )
            precision_value = precision(target_image,
                                        retrieved_filenames,
                                        retrieved,
                                        method=result_test_ukbench
                                        )
            recalls[label][target_image] = recall_value
            precisions[label][target_image] = precision_value
        elif dataset == 'mirflickr':
            retrieved_filenames = retrieved[:4]
            recall_value = recall(target_image,
                                  retrieved_filenames,
                                  retrieved,
                                  method=result_test_mirflickr
                                  )
            precision_value = precision(target_image,
                                        retrieved_filenames,
                                        retrieved,
                                        method=result_test_mirflickr
                                        )
            recalls[label][target_image] = recall_value
            precisions[label][target_image] = precision_value
        else:
            raise Exception("Unsupported dataset")

fscore = {}
fscore_avg = {}
for label in labels:
    fscore[label] = {}
    current_fscore = 0
    for image_name in image_names:
        precision = precisions[label][image_name]
        recall = recalls[label][image_name]
        value = 2 * (precision * recall) / (precision + recall)
        fscore[label][image_name] = value
        current_fscore = current_fscore + value
    fscore_avg[label] = current_fscore / len(image_names)

with open("build/recall.dat", "w") as f:
    f.write("Image\t%s\n" % "\t".join(image_names))
    for label in labels:
        line = "%s" % label
        for image_name in image_names:
            line = line + "\t%f" % recalls[label][image_name]
        f.write(line + "\n")

with open("build/precision.dat", "w") as f:
    f.write("Image\t%s\n" % "\t".join(image_names))
    for label in labels:
        line = "%s" % label
        for image_name in image_names:
            line = line + "\t%f" % precisions[label][image_name]
        f.write(line + "\n")

with open("build/fmeasure.dat", "w") as f:
    f.write("Image\t%s\n" % "\t".join(image_names))
    for label in labels:
        line = "%s" % label
        for image_name in image_names:
            line = line + "\t%f" % fscore[label][image_name]
        f.write(line + "\n")

with open("build/fmeasure-avg.dat", "w") as f:
    f.write("Configuration\tAverage F-score\n")
    for label in labels:
        f.write("%s\t%f\n" % (label, fscore_avg[label]))

def generate_graphics_statement(image_path, width='.5in'):
    return "\\includegraphics[keepaspectratio=false, height=%s, width=%s]{%s}" % (width, width, image_path)

with open("build/results.tex", "w") as f:
    width = '.35in'
    for label in labels[:4]:
        f.write("\\begin{minipage}{.45\\textwidth}")
        f.write("\\subfloat[%s]{\\begin{tabular}{p{%s} p{%s} p{%s} p{%s} p{%s}}\n" % (label, width, width, width, width, width))
        f.write("Target & 1st & 2nd & 3rd & 4th \\\\\n")
        for image_name in image_names:
            line = generate_graphics_statement("../datasets/" + dataset + "/" + image_name, width=width)
            for r in results[label][image_name][:4]:
                image_path = "../datasets/" + dataset + "/" + r
                line = line + " & " + generate_graphics_statement(image_path, width=width)
            f.write(line + " \\\\\n")
        f.write("\\end{tabular}}\n")
        f.write("\\hfill\n")
        f.write("\\end{minipage}\n")
