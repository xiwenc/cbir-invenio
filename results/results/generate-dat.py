import sys
import os
import random

sys.path.append('../src/')
from utils import result_test_ukbench, recall, precision, result_test_mirflickr, mirflickr_images, extract_fname_id_test  # noqa
import utils

if len(sys.argv) == 2:
    tokens = sys.argv[1].split("-")
    dataset_path = tokens[0]
    dataset = dataset_path.split("/")[1]
    output = tokens[1].replace(".dat", "").replace(".tex", "")
else:
    dataset = sys.argv[1]
    dataset_path = os.path.join("build", dataset)
    output = sys.argv[2]

all_files = os.listdir(dataset_path)
configs = filter(lambda x: x.endswith('.results'), all_files)

precisions = {}
recalls = {}
image_names = []
labels = []
results = {}
for config in configs:
    label = config.replace(".results", "")
#    label = label.replace('surf', 'sur')
#    label = label.replace('sift', 'sif')
#    label = label.replace('kmeans', 'kme')
#    label = label.replace('images', 'img')
#    label = label.replace('segments', 'seg')
#    label = label.replace('000', 'k')
    labels.append(label)
    results[label] = {}
    recalls[label] = {}
    precisions[label] = {}
    path = os.path.join(dataset_path, config)
    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    for line in lines:
        if line.startswith('# '):
            tokens = line.split()
            image_name = os.path.basename(tokens[1])
            name = os.path.basename(tokens[2])
            similarity = float(tokens[3])
            if image_name not in results[label]:
                results[label][image_name] = []
            results[label][image_name].append(name)
            if image_name not in image_names:
                image_names.append(image_name)

recalls_image_names = {}
precisions_image_names = {}
for image_name in image_names:
    recalls_image_names[image_name] = []
    precisions_image_names[image_name] = []

if dataset == 'mirflickr':
    image_names, _, image_matches = mirflickr_images()

absolute_matches = {}
for label, s in results.iteritems():
    absolute_matches[label] = {}
    for target_image, retrieved in s.iteritems():
        if dataset == 'ukbench':
            retrieved_filenames = retrieved[:3]
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
            relevant, retrieved = result_test_ukbench(target_image, retrieved_filenames, retrieved)
        elif dataset == 'mirflickr':
            retrieved_filenames = retrieved[:image_matches[target_image]]
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
            relevant, retrieved = result_test_mirflickr(target_image, retrieved_filenames, retrieved)
        else:
            raise Exception("Unsupported dataset")
        absolute_matches[label][target_image] = len(set(relevant) & set(retrieved))

fscore = {}
fscore_avg = {}
for label in labels:
    fscore[label] = {}
    current_fscore = 0
    for image_name in image_names:
        try:
            precision = precisions[label][image_name]
        except KeyError:
            precisions[label][image_name] = precision = 0
        try:
            recall = recalls[label][image_name]
        except KeyError:
            recalls[label][image_name] = recall = 0
        d = precision + recall
        if d == 0:
            value = 0.
        else:
            value = 2. * (precision * recall) / d
        fscore[label][image_name] = value
        current_fscore = current_fscore + value
    fscore_avg[label] = current_fscore / len(image_names)

if output == "recalltranspose":
    print("x\t%s" % "\t".join(image_names))
    for label in labels:
        line = "%s" % label
        for image_name in image_names:
            line = line + "\t%f" % recalls[label][image_name]
        print(line)

if output == "precisiontranspose":
    print("x\t%s" % "\t".join(image_names))
    for label in labels:
        line = "%s" % label
        for image_name in image_names:
            line = line + "\t%f" % precisions[label][image_name]
        print(line)

if output == "fscoretranspose":
    print("x\t%s" % "\t".join(image_names))
    for label in labels:
        line = "%s" % label
        for image_name in image_names:
            line = line + "\t%f" % fscore[label][image_name]
        print(line)

if output == "recall":
    print("x\t%s" % "\t".join(labels))
    for image_name in image_names:
        line = "%s" % image_name
        for label in labels:
            line = line + "\t%f" % recalls[label][image_name]
        print(line)

if output == "precision":
    print("x\t%s" % "\t".join(labels))
    for image_name in image_names:
        line = "%s" % image_name
        for label in labels:
            line = line + "\t%f" % precisions[label][image_name]
        print(line)

if output == "fscore":
    print("x\t%s" % "\t".join(labels))
    for image_name in image_names:
        line = "%s" % image_name
        for label in labels:
            line = line + "\t%f" % fscore[label][image_name]
        print(line)

if output == "fscoreavg":
    print("x\tAverage F-score")
    for label in labels:
        print("%s\t%f" % (label, fscore_avg[label]))

if output == "retrieval":
    print("x\t%s" % "\t".join(labels))
    for image_name in image_names:
        line = "%s" % image_name
        for label in labels:
            try:
                value = absolute_matches[label][image_name]
            except KeyError:
                value = 0
            line = line + "\t%d" % value
        print(line)


def generate_graphics_statement(image_path, width='.5in'):
    return "\\includegraphics[keepaspectratio=false, height=%s, width=%s]{%s}" % (
            width, width, image_path)


def tex_image_table(images, cols=4, width='1.3in', captions=None):
    result = ""
    result = result + "\\begin{tabular}{"
    for i in range(cols):
        result = result + "p{%s} " % width
    result = result + "}\n"
    row = []
    for image in images:
        image_path = get_image_path(image)
        result = result + generate_graphics_statement(image_path, width=width)
        row.append(image)
        if len(row) == cols:
            result = result + "\\\\\n"
            if captions is not None:
                row = [i + ": " + captions[i] for i in row]
            result = result + " & ".join(row) + "\\\\\n"
            row = []
        else:
            result = result + " & "
    result = result + "\\end{tabular}\n"
    return result


def get_image_path(fname):
    dirs = ['ukbench-test', 'ukbench-training', 'mirflickr-test', 'mirflickr-training']

    for d in dirs:
        attempt = os.path.join("../datasets", d, fname)
        if os.path.exists(attempt):
            return attempt
    raise Exception("Not found: " + fname)

if output == "imagesamples":
    if dataset == 'ukbench':
        groupsize = 4
        candidate_id = random.sample(range(len(image_names)), 1)[0]
        selected = extract_fname_id_test(image_names[candidate_id])
        base_id = int(selected / groupsize) * groupsize
        targets = ["ukbench%05d.jpg" % i for i in range(base_id, base_id + groupsize)]
        captions = None
    elif dataset == 'mirflickr':
        training_images = utils.read_image_tags("../datasets/mirflickr", "-training")
        target_id = random.sample(range(len(image_names) / 2, len(image_names)), 3)[0]
        target = image_names[target_id]
        matches = utils.retrieve_matches(utils.extract_tags(target), training_images)
        targets = []
        targets.append(target)
        for i in range(3):
            targets.append(matches[i])
        captions = {}
        for target in targets:
            captions[target] = ", ".join(utils.extract_tags(target))
    else:
        raise Exception('Unsupported')
    print(tex_image_table(targets, captions=captions))

if output in ["results1", "results2"]:
    if dataset == 'ukbench':
        captions = None
        if output == "results1":
            label = "sift-kmeans-2000-02-canny-tfidf-segments"
            target = "ukbench00125.jpg"
        elif output == "results2":
            label = "surf-som-2000-02-slic-lsi-segments"
            target = "ukbench00118.jpg"
        targets = []
        targets.append(target)
        for i in range(3):
            targets.append(results[label][target][i])
    elif dataset == 'mirflickr':
        if output == "results1":
            label = "surf-kmeans-2000-02-canny-tfidf-segments"
            target = "im6856.jpg"
        elif output == "results2":
            label = "sift-kmeans-1000-02-otsu-tfidf-segments"
            target = "im7959.jpg"
        targets = []
        targets.append(target)
        for i in range(3):
            targets.append(results[label][target][i])
        captions = {}
        for target in targets:
            captions[target] = ", ".join(utils.extract_tags(target))
    else:
        raise Exception('Unsupported')
    print(tex_image_table(targets, captions=captions))

if output == "resultsamples":
    width = '.35in'
    for label in labels[:4]:
        print("\\begin{minipage}{.45\\textwidth}")
        print("\\subfloat[%s]{\\begin{tabular}{p{%s} p{%s} p{%s} p{%s} p{%s}}" % (
            label, width, width, width, width, width))
        print("Target & 1st & 2nd & 3rd & 4th \\\\")
        for image_name in image_names:
            line = generate_graphics_statement("../datasets/" + dataset + "/" + image_name,
                                               width=width)
            for r in results[label][image_name][:4]:
                image_path = "../datasets/" + dataset + "/" + r
                line = line + " & " + generate_graphics_statement(image_path, width=width)
            print(line + " \\\\")
        print("\\end{tabular}}")
        print("\\hfill")
        print("\\end{minipage}")
