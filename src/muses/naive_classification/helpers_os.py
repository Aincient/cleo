import numpy as np
import os
from muses.naive_classification.definitions_os import classes
from collections import OrderedDict
from keras.models import model_from_json
from PIL import Image
from django.conf import settings

LOADED_MODELS = {}

json_path = settings.PROJECT_DIR(
                    os.path.join(
                        '..', '..', '..',
                        'src',
                        'muses',
                        'naive_classification',
                        'model_architecture.json',
                    )
                )


def predict_image_paths(image_paths, model_path, target_size=(128, 128)):
    """Use a trained classifier to predict the class probabilities of a list of images
    Returns most likely class and its probability

    :param image_paths: list of path(s) to the image(s)
    :param model_path: path to the pre-trained model
    :param target_size:
    :type image_paths: list
    :return:
    :rtype: list
    """
    desired_size = target_size[0]

    if model_path in LOADED_MODELS:
        loaded_model = LOADED_MODELS[model_path]

    else:
        with open(json_path, 'r') as json_file:
            loaded_model = model_from_json(json_file.read())
        loaded_model.load_weights(model_path)
        LOADED_MODELS[model_path] = loaded_model

    img_list = []
    for image_path in image_paths:
        im = Image.open(image_path)
        old_size = im.size

        ratio = float(desired_size) / max(old_size)
        new_size = tuple([int(x * ratio) for x in old_size])

        im = im.resize(new_size, Image.ANTIALIAS)

        new_im = Image.new("RGB", (desired_size, desired_size), color='White')
        new_im.paste(im, ((desired_size - new_size[0]) // 2,
                          (desired_size - new_size[1]) // 2))

        img_array = np.asarray(new_im)
        img_array = img_array.astype('float32')
        img_array = (img_array / 255)
        img_list.append(img_array)

    predictions = loaded_model.predict(np.array(img_list))
    return predictions


def predict_image_path_dict(image_path, model_path, target_size=(128, 128)):
    """Use a trained classifier to predict the class probabilities of a list of images
    Returns ordered dict of classes ordered by their probability

    :param image_path: list of path(s) to the image(s)
    :param model_path: path to the pre-trained model
    :param target_size:
    :type image_path: list
    :return:
    :rtype: OrderedDict
    """
    if not isinstance(image_path, (list, tuple)):
        image_path = [image_path]
    if len(image_path) <= 1:
        prediction = predict_image_paths(image_path, model_path, target_size)[0]
    else:
        prediction = np.mean(predict_image_paths(image_path, model_path, target_size), axis=0)
    named_prediction = {}
    for idx, p in enumerate(prediction):
        named_prediction[classes[str(idx)]] = p

    return OrderedDict(
        sorted(list(named_prediction.items()), key=lambda x: x[1], reverse=True)
    )


def predict_items(items, model_path, target_size=(128, 128)):
    """Use a trained classifier to predict the class probabilities of an item or multiple items
    Returns ordered dict of classes ordered by their probability

    :param items: the item(s) that need to be classified
    :param model_path: path to the pre-trained model
    :param target_size:
    :type items: CollectionItemDocument
    :return:
    :rtype: OrderedDict
    """
    named_prediction = {}
    total = []
    if not isinstance(items, (list, tuple)):
        items = [items]
    for item in items:
        if item.images:
            image_list = list(item.images)
            predictions = predict_image_paths(image_list, model_path, target_size)
            average_prediction = np.mean(predictions, axis=0)
            total.append(average_prediction)

    if total:
        total_average = np.mean(total, axis=0)
        for idx, p in enumerate(total_average):
            named_prediction[classes[str(idx)]] = p
        return OrderedDict(
            sorted(list(named_prediction.items()), key=lambda x: x[1], reverse=True)
        )
