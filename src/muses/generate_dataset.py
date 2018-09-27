import os
import sys
import numpy as np
from six.moves import cPickle
from imageio import imread


__all__ = (
    'get_single',
    'load_batch',
    'load_data',
    'prepare_image_list',
    'write_batch',
)


def get_single(im_path):
    arr = imread(im_path, as_gray=False, pilmode="RGB")
    return arr


def prepare_image_list(images_list):
    #Go through images in list, load them and get right representation
    data = []
    filenames = []  # correspondent to `filenames` in CIFAR10
    for im_path, categories in images_list:
        try:
            single = get_single(im_path)

        except (IndexError, IOError) as err:
            continue

        data.append(single)
        filenames.append(im_path)

    return {
        'batch_label': 'muses',
        'data': data,
        'filenames': filenames,
    }


def write_batch(images_list, dest_filename, text_labels):
    """Write single batch.

    :param images_list: List of tuples consisting of the full image path
                        as the first element and list of labels/categories of
                        the image as second argument.
    :param dest_filename: Output filename.
    :param text_labels: Text labels - mapping between numerical and textual
                        representation of the labels/categories.
    :return:
    """
    cifar10_data = prepare_image_list(images_list)
    dest = open(dest_filename, 'wb')
    cPickle.dump(cifar10_data, dest)
    dest.close()


def load_batch(file_path):
    """Load batch.

    :param file_path: Path to the batch to load data from.
    :return: Tuple of 3 elements: data,
                                  labels (numerical),
                                  text_labels (mapping between numerical
                                               and textual representation of
                                               the label/category)
    """
    f = open(file_path, 'rb')
    if sys.version_info < (3,):
        d = cPickle.load(f)
    else:
        d = cPickle.load(f, encoding='bytes')
    f.close()
    data = d['data']

    data = np.array(data)
    return data


def load_data(source_dir):
    """Load data.

    :param source_dir: Full path to directory to read the data from.
    :param num_train_samples:
    :return: Tuple of 3 elements: data,
                                  labels (numerical),
                                  text_labels (mapping between numerical
                                               and textual representation of
                                               the label/category)
    """
    files = [
        os.path.join(source_dir, _file)
        for _file
        in os.listdir(source_dir)
        if os.path.isfile('{}/{}'.format(source_dir, _file)) and _file.startswith('data_batch')
    ]

    for i in range(1, len(files)+1):
        file_path = os.path.join(source_dir, 'data_batch_' + str(i))

        x_train = load_batch(file_path)

    return x_train
