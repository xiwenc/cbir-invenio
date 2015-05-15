import cv2
import numpy
import operator

from logger import logger


def watershed(image, grayed, edges, min_ratio, max_count):
    """ Applies watershed algorithm to 'image' with markers derived
        from 'edges'
    Args:
        image: original image
        grayed: grayed and optionally blurred version of 'image'
        edges: a binary image
        min_ratio: only contours in 'edges' with an area bigger are used as
                   markers
        max_count: maximum number of segments to derive
    Returns segments, markers, count
    """

    markers = edges.copy()
    _, markers1, _ = extract_segments(
        grayed,
        markers,
        min_ratio=min_ratio,
        max_count=max_count
    )
    markers32 = numpy.int32(markers1)
    cv2.watershed(image, markers32)
    watersheded = cv2.convertScaleAbs(markers32)
    _, edges = cv2.threshold(
        watersheded,
        1,
        255,
        cv2.THRESH_BINARY_INV
    )
    segments, markers, count = extract_segments(
        grayed,
        edges
    )
    return segments, markers, count


def canny(image, gaussian_ksize=(7, 7), threshold1=20, threshold2=100):
    """ Computes Gaussian blurred grayscale and Canny edges
    Args:
        image = image array; use cv2.imread(...) to load from file
        gaussian_ksize = filter size e.g. (5, 5)
        threshold1 = first threshold of the hysteresis procedure
        threshold2 = second threshold of the hysteresis procedure
    Returns (grayscale, edges)
    """
    if len(image.shape) == 3:
        grayed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif len(image.shape) == 2:
        grayed = image
    else:
        raise Exception("Unsupported input image")

    blurred = cv2.GaussianBlur(grayed, gaussian_ksize, 0)
    edges = cv2.Canny(blurred, threshold1, threshold2)
    return (grayed, edges)


def otsu(image, gaussian_ksize=(7, 7)):
    """ Computes Gaussian blurred grayscale and Otsu threshold edges
    Args:
        image = image array; use cv2.imread(...) to load from file
        gaussian_ksize = filter size e.g. (5, 5)
    Returns (grayscale, edges)
    """
    grayed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grayed, gaussian_ksize, 0)
    ret, edges = cv2.threshold(
        blurred,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    return (grayed, edges)


def seg_otsu_watershed(image, min_ratio=0.0001, max_count=100):
    grayed, edges = otsu(image)
    return watershed(image, grayed, edges, min_ratio, max_count)


def seg_canny_watershed(image, min_ratio=0.0001, max_count=100):
    grayed, edges = canny(image)
    return watershed(image, grayed, edges, min_ratio, max_count)


def seg_slic(image, min_ratio=0, max_count=100):
    from skimage.segmentation import slic
    from skimage.segmentation import mark_boundaries
    from skimage import img_as_ubyte

    grayed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    segments = slic(image, sigma=5)
    black = numpy.zeros(image.shape, numpy.uint8)
    edges_sci = mark_boundaries(black, segments, color=(1, 1, 1))
    edges_gray = cv2.cvtColor(img_as_ubyte(edges_sci), cv2.COLOR_BGR2GRAY)
    ret, edges = cv2.threshold(
        edges_gray,
        80,
        255,
        cv2.THRESH_BINARY
    )
    segments, markers, count = extract_segments(
        grayed,
        edges,
        min_ratio,
        max_count
    )
    return segments, markers, count


def extract_segments(grayed, edges, min_ratio=0, max_count=100):
    contours, hierarchy = cv2.findContours(
        edges,
        cv2.cv.CV_RETR_TREE,
        cv2.cv.CV_CHAIN_APPROX_SIMPLE
    )
    markers = numpy.zeros(grayed.shape, numpy.uint8)
    total_area = edges.shape[0] * edges.shape[1]
    contours_total = len(contours)

    contours_no_child = []
    for i in range(contours_total):
        h = hierarchy[0][i]
        if h[2] == -1:
            contours_no_child.append(contours[i])
        else:
            logger.debug('Skipped child contour {i}'.format(i=i))

    contours_filtered = []
    for contour in contours_no_child:
        area = float(cv2.contourArea(contour))
        ratio = area / total_area
        if ratio >= min_ratio:
            contours_filtered.append((contour, area))
        else:
            logger.debug('Skipped contour with ratio %f' % ratio)

    contours_filtered_sorted = sorted(
        contours_filtered,
        key=operator.itemgetter(1),
        reverse=True
    )

    assert(max_count < 255 - 2)
    contours_count = min(len(contours_filtered_sorted), max_count)
    contours_capped = contours_filtered_sorted[:contours_count]
    contours_no_tuple = [c for c, v in contours_capped]

    # color 1: border
    colors = range(2, 255)
    import random
    random.shuffle(colors)
    for i in range(contours_count):
        cv2.drawContours(markers, contours_no_tuple, i, colors[i], -1)
    logger.info(
        'Segments found {total}, {count} satisfied min_ratio'.format(
            total=contours_total,
            count=contours_count
        ))
    segments = contours_no_tuple
    return segments, markers, contours_count
