from enum import Enum

import numpy as np

from cvbase.det.labels import read_labels
from cvbase.conversion import is_list_of

import cvbase.image as im


class Color(Enum):
    """Color associated with RGB values

    8 colors in total: red, green, blue, cyan, yellow, magenta, white and black.
    """
    red = (0, 0, 255)
    green = (0, 255, 0)
    blue = (255, 0, 0)
    cyan = (255, 255, 0)
    yellow = (0, 255, 255)
    magenta = (255, 0, 255)
    white = (255, 255, 255)
    black = (0, 0, 0)


def draw_bboxes(img, bboxes, colors=Color.green, top_k=0, thickness=1,
                show=True, win_name='', wait_time=0, out_file=None):  # yapf: disable
    """Draw bboxes on an image

    Args:
        img(str or ndarray or :obj:`cvbase.image.Image`): the image to be shown
        bboxes(list or ndarray): a list of ndarray of shape (k, 4)
        colors(list or Color or tuple): a list of colors, corresponding to bboxes
        top_k(int): draw top_k bboxes only if positive
        thickness(int): thickness of lines
        show(bool): whether to show the image
        win_name(str): the window name
        wait_time(int): value of waitKey param
        out_file(str or None): the filename to write the image
    """
    if isinstance(img, str):
        img = im.Image.open(img)
    elif isinstance(img, np.ndarray):
        img = im.Image.fromarray(img)
    assert isinstance(img, im.Image)
    draw = im.ImageDraw(img)
    if isinstance(bboxes, np.ndarray):
        bboxes = [bboxes]
    assert is_list_of(bboxes, np.ndarray)
    if isinstance(colors, (tuple, Color)):
        colors = [colors for _ in range(len(bboxes))]
    for i in range(len(colors)):
        if isinstance(colors[i], Color):
            colors[i] = colors[i].value
    assert len(bboxes) == len(colors)

    for i, _bboxes in enumerate(bboxes):
        bboxes_int = _bboxes.astype(np.int32)
        if top_k <= 0:
            _top_k = _bboxes.shape[0]
        else:
            _top_k = min(top_k, _bboxes.shape[0])
        for j in range(_top_k):
            draw.rectangle(bboxes_int[j, :], colors[i], thickness=thickness)
    if show:
        img.show(win_name, wait_time)
    if out_file is not None:
        img.save(out_file)


def draw_bboxes_with_label(img, bboxes, labels, top_k=0, bbox_color=Color.green,
                           text_color=Color.green, thickness=1, font_size=12,
                           show=True, win_name='', wait_time=0, out_file=None):  # yapf: disable
    """Draw bboxes with label text in image

    Args:
        img(str or ndarray): the image to be shown
        bboxes(list or ndarray): a list of ndarray of shape (k, 4)
        labels(str or list): label name file or list of label names
        top_k(int): draw top_k bboxes only if positive
        bbox_color(Color or tuple): color to draw bboxes
        text_color(Color or tuple): color to draw label texts
        thickness(int): thickness of bbox lines
        font_scale(float): font scales
        show(bool): whether to show the image
        win_name(str): the window name
        wait_time(int): value of waitKey param
        out_file(str or None): the filename to write the image
    """
    if isinstance(img, str):
        img = im.Image.open(img)
    elif isinstance(img, np.ndarray):
        img = im.Image.fromarray(img)
    assert isinstance(img, im.Image)
    draw = im.ImageDraw(img)
    label_names = read_labels(labels)
    if isinstance(bbox_color, Color):
        bbox_color = bbox_color.value
    if isinstance(text_color, Color):
        text_color = text_color.value
    assert len(bboxes) == len(label_names)
    for i, _bboxes in enumerate(bboxes):
        bboxes_int = _bboxes[:, :4].astype(np.int32)
        if top_k <= 0:
            _top_k = _bboxes.shape[0]
        else:
            _top_k = min(top_k, _bboxes.shape[0])
        for j in range(_top_k):
            draw.rectangle(bboxes_int, bbox_color, thickness=thickness)
            if _bboxes.shape[1] > 4:
                label_text = '{}|{:.02f}'.format(label_names[i], _bboxes[j, 4])
            else:
                label_text = label_names[i]
            draw.text(
                label_text, (bboxes_int[j, 0], bboxes_int[j, 1] - 2),
                text_color,
                font_size=font_size)
    if show:
        img.show(win_name, wait_time)
    if out_file is not None:
        img.save(out_file)
