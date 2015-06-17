import multiprocessing
import threading
import math
import os
import cv2
import numpy
from logger import logger
import re
import operator


def distribute(f, obj, targets, use_threading=False):
    numprocs = int(multiprocessing.cpu_count())
    queue = multiprocessing.Queue()
    total = len(targets)
    chunksize = int(math.ceil(total / float(numprocs)))
    procs = []
    for i in range(numprocs):
        start = i * chunksize
        end = start + chunksize
        if end >= total:
            end = total

        if use_threading:
            p = threading.Thread(
                target=f,
                args=(obj, targets[start:end], queue)
            )
        else:
            p = multiprocessing.Process(
                target=f,
                args=(obj, targets[start:end], queue)
            )
        procs.append(p)
        p.start()

    result = []
    for i in range(numprocs):
        result.extend(queue.get())
    for p in procs:
        p.join()

    return result


def recursive_list_dir(target, everything=False):
    allowed = ['png', 'jpg', 'jpeg']
    fname, ext = os.path.splitext(target)
    if os.path.isfile(target) and (
        ext.lower().replace('.', '') in allowed or everything
    ):
        return [target]
    elif os.path.isdir(target):
        result = []
        for entry in os.listdir(target):
            result.extend(recursive_list_dir(os.path.join(target, entry),
                                             everything))
        return result
    else:
        return []


def clean_dir(target, everything=False):
    files = recursive_list_dir(target, everything)
    for f in files:
        os.remove(f)


def draw_text(image, text, pos, font_scale=2, thickness=3, color=(255, 0, 0)):
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    ret, baseline = cv2.getTextSize(text, font_face, font_scale, thickness)

    cv2.rectangle(
        image,
        (pos[0], pos[1]),
        (pos[0] + ret[0], pos[1] + ret[1] + baseline * 2),
        (0, 0, 0),
        -1
    )
    cv2.putText(
        image,
        text,
        (pos[0], pos[1] + ret[1] + baseline),
        font_face,
        font_scale,
        color,
        thickness,
        cv2.CV_AA,
    )


def extract_fname_id_test(name):
    m = re.match(r".*ukbench([0-9]+)*", name)
    if m is None:
        return -1
    else:
        num = int(m.group(1))
        return num


def extract_tags(fname):
    tags_file = fname.replace(".jpg", ".txt").replace("/im", "/tags")
    if not os.path.exists(tags_file):
        tags_file = "../datasets/mirflickr/" + tags_file.replace("im", "tags")
    if not os.path.exists(tags_file):
        tags_file = tags_file.replace("/mirflickr/", "/mirflickr-test/")
    if not os.path.exists(tags_file):
        tags_file = tags_file.replace("/mirflickr-test/", "/mirflickr-training/")
    with open(tags_file, "r") as f:
        tags = [i.strip() for i in f.readlines()]
    return tags


def extract_id(fname):
    m = re.match(r".*im([0-9]+)*", fname)
    if m is None:
        return -1
    else:
        num = int(m.group(1))
        return num


def result_test_ukbench(target, retrieved, everything, groupsize=4):
    target_id = extract_fname_id_test(target)
    base_id = int(target_id / groupsize) * groupsize
    assert target_id >= 0
    retrieved_ids = map(extract_fname_id_test, retrieved)
    everything_ids = map(extract_fname_id_test, everything)
    relevant_ids = filter(
        lambda x: x - base_id < groupsize and x - base_id >= 0,
        everything_ids
    )
    return (relevant_ids, retrieved_ids)


def result_test_mirflickr(target, retrieved, everything, min_common_tags=1):
    target_tags = extract_tags(target)
    retrieved_ids = map(extract_id, retrieved)

    relevant_ids = []
    for fname in everything:
        current_tags = extract_tags(fname)
        common = set(target_tags) & set(current_tags)
        if len(common) >= min_common_tags:
            relevant_ids.append(extract_id(fname))
    return (relevant_ids, retrieved_ids)


def recall(target, retrieved, everything, method=result_test_ukbench):
    (relevant_ids, retrieved_ids) = method(target, retrieved, everything)
    return recall_canonical(relevant_ids, retrieved_ids)


def precision(target, retrieved, everything, method=result_test_ukbench):
    (relevant_ids, retrieved_ids) = method(target, retrieved, everything)
    return precision_canonical(relevant_ids, retrieved_ids)


def recall_canonical(relevant, retrieved):
    intersect = set(relevant) & set(retrieved)
    relevant_count = len(relevant)
    if relevant_count == 0:
        return 0
    else:
        return float(len(intersect)) / relevant_count


def precision_canonical(relevant, retrieved):
    intersect = set(relevant) & set(retrieved)
    retrieved_count = len(retrieved)
    if retrieved_count == 0:
        return 0
    else:
        return float(len(intersect)) / retrieved_count


def extract_color_mask(segmented, color_code):
    mask = numpy.zeros(segmented.shape, numpy.uint8)
    for x in numpy.arange(segmented.shape[0]):
        for y in numpy.arange(segmented.shape[1]):
            if segmented[x][y] == color_code:
                mask[x][y] = 255
    return mask


def rectangle_center(rectangle):
    (x, y, w, h) = rectangle
    return (x + int(w / 2), y + int(h / 2))


def is_point_in_rectangle(point, rectangle):
    (x, y, w, h) = rectangle
    (px, py) = point
    x_in_range = px <= x + w and px >= x
    y_in_range = py <= y + h and py >= y
    return x_in_range and y_in_range


def is_rectangle_unwrapped(rectangle, rectangles):
    point = rectangle_center(rectangle)
    for c, r in rectangles:
        # skip self reflection
        if rectangle == r:
            continue
        elif is_point_in_rectangle(point, r):
            return False
    return True


def compute_similarities(target, images, distance_function,
                         indexer=None, corpora=None):
    image1 = target
    results = {}
    if indexer and corpora:
        results = corpora.similarity(indexer, image1)
    else:
        for image2 in images:
            if len(image2.words) <= 0:
                results[image2.filename] = 0
            else:
                results[image2.filename] = distance_function(image1, image2)

    results_sorted = sorted(
        results.iteritems(),
        key=operator.itemgetter(1),
        reverse=True
    )
    return results_sorted


def recall_and_precision_mirflickr(target, images, distance_function,
                                   indexer=None, corpora=None):
    image1 = target
    results_sorted = compute_similarities(target, images, distance_function,
                                          indexer=indexer, corpora=corpora)

    all_filenames = [k for k, v in results_sorted]
    relevant, _ = result_test_mirflickr(target.filename, [], all_filenames)

    top = []
    count = 0
    for k, v in results_sorted:
        count = count + 1
        top.append((k, v))
        if count == 10:
            break

    top_filenames = [k for k, v in top]

    target_recall = recall(
        image1.filename,
        top_filenames,
        all_filenames,
        method=result_test_mirflickr
    )
    target_precision = precision(
        image1.filename,
        top_filenames,
        all_filenames,
        method=result_test_mirflickr
    )

    return target_recall, target_precision, top


def recall_and_precision_ukbench(target, images, distance_function,
                                 indexer=None, corpora=None):
    image1 = target
    results_sorted = compute_similarities(target, images, distance_function,
                                          indexer=indexer, corpora=corpora)

    all_filenames = [k for k, v in results_sorted]
    relevant, _ = result_test_ukbench(target.filename, [], all_filenames)

    top = []
    count = 0
    for k, v in results_sorted:
        count = count + 1
        top.append((k, v))
        if count == 10:
            break

    top_filenames = [k for k, v in top]

    target_recall = recall(
        image1.filename,
        top_filenames,
        all_filenames,
        method=result_test_ukbench
    )
    target_precision = precision(
        image1.filename,
        top_filenames,
        all_filenames,
        method=result_test_ukbench
    )
    return target_recall, target_precision, top


def recall_and_precision(images, distance_function, indexer=None,
                         corpora=None):
    recalls = {}
    precisions = {}
    for image1 in images:
        results = {}
        if indexer and corpora:
            results = corpora.similarity(indexer, image1)
        else:
            for image2 in images:
                results[image2.filename] = distance_function(image1, image2)

        results_sorted = sorted(
            results.iteritems(),
            key=operator.itemgetter(1),
            reverse=True
        )

        top = results_sorted[0:8]
        top_filenames = [k for k, v in top]
        recalls[image1.filename] = recall(
            image1.filename,
            top_filenames
        )
        precisions[image1.filename] = precision(
            image1.filename,
            top_filenames
        )

        logger.info("===> {image1}".format(image1=image1.filename))

        for k, v in results_sorted:
            logger.info("{image2}\t{similar}".format(
                image2=k,
                similar=v)
            )
            assert v >= 0

    logger.info("Recall and precision of topN")
    for k, v in recalls.iteritems():
        logger.info("{image}\t{recall}\t{precision}".format(
            image=k,
            recall=recalls[k],
            precision=precisions[k]
        ))
        assert recalls[k] >= 0
        assert precisions[k] >= 0


def tagname_to_imagename(name):
    return name.replace('tags', 'im').replace('.txt', '.jpg')


def retrieve_matches(targets, basket):
    matches = []
    targets_set = set(targets)
    for name, tags in basket.iteritems():
        if len(targets_set & set(tags)) > 0:
            matches.append(name)
    return matches


def read_image_tags(mirflickr, suffix):
    training_images = {}
    training_path = mirflickr + suffix
    for i in os.listdir(training_path):
        if i.startswith('tags'):
            with open(os.path.join(training_path, i), "r") as f:
                tags = [l.strip() for l in f.readlines()]
            training_images[tagname_to_imagename(i)] = tags
    return training_images


def mirflickr_images():
    mirflickr = os.path.join('..', 'datasets', 'mirflickr')
    test_images = read_image_tags(mirflickr, "-test")
    training_images = read_image_tags(mirflickr, "-training")

    results_tags = {}
    results_matches = {}
    for name, tags in test_images.iteritems():
        tags_count = len(tags)
        image_matches = retrieve_matches(tags, training_images)
        matches_count = len(image_matches)
        results_tags[name] = tags_count
        results_matches[name] = matches_count

    sorted_results_matches = sorted(results_matches.iteritems(), key=operator.itemgetter(1))
    sorted_names = [name for name, matches in sorted_results_matches]
    return sorted_names, results_tags, results_matches
