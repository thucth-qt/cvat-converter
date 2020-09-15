import os
import glob
import argparse
from collections import defaultdict
import xml.etree.ElementTree as ET

import cv2
import numpy as np


class ImageLabel:
    def __init__(self, img_path, lb_path):
        self.img_path = img_path
        self.lb = self._get_label(img_path, lb_path)
        self.shape = self._get_shape(img_path)

    def __str__(self):
        return str(self.__dict__)

    def _get_label(self, img_path, lb_path):
        with open(lb_path) as f:
            lines = [x.strip() for x in f.readlines()]
            labels = []
            for line in lines:
                line = line.split(',')[1:-2]
                labels.append([float(x) for x in line])
        labels = self._unnormalize(img_path, labels)
        return labels

    def _get_shape(self, img_path):
        image = cv2.imread(img_path)
        h, w, c = image.shape
        return h, w, c

    def _unnormalize(self, img_path, labels):
        h, w, _ = cv2.imread(img_path).shape
        
        new_labels = []
        for label in labels:
            label[0] = round(label[0] * w, 2)
            label[1] = round(label[1] * w, 2)
            label[2] = round(label[2] * w, 2)
            label[3] = round(label[3] * w, 2)
            label[4] = round(label[4] * h, 2)
            label[5] = round(label[5] * h, 2)
            label[6] = round(label[6] * h, 2)
            label[7] = round(label[7] * h, 2)
            
            tl = label[0], label[4]
            tr = label[1], label[5]
            bl = label[2], label[6]
            br = label[3], label[7]

            new_labels.append([tl, tr, bl, br])
        return new_labels


def get_image_label_paths(input_dir):
    img_formats = ['.png', '.jpg', '.jpeg', '.webp']

    # Get image paths
    image_paths = glob.glob(os.path.join(input_dir, '*'))
    image_paths = [path for path in image_paths if os.path.splitext(path)[-1] in img_formats]

    # Get image label paths
    image_label_paths = []
    for img_path in image_paths:
        img_file, ext = os.path.splitext(img_path)
        lb_path = img_file + ".txt"

        if os.path.isfile(lb_path):
            img_lb_path = ImageLabel(img_path, lb_path)
            image_label_paths.append(img_lb_path)
    return image_label_paths


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument('--input-dir', type=str, required=True)
    parse.add_argument('--output-dir', type=str, default="./")
    opt = parse.parse_args()

    image_label_paths = get_image_label_paths(opt.input_dir)

    root = ET.Element("annotations")
    for idx, image_label in enumerate(image_label_paths):
        img_path = os.path.split(image_label.img_path)[-1]
        h, w, _ = image_label.shape
        for lb in image_label.lb:
            pts = np.array([lb]).flatten()
            pts = ','.join(str(x) for x in pts.tolist())

            image = ET.SubElement(root, "image", id=str(idx), name=img_path, width=str(w), height=str(h))
            polygon = ET.SubElement(image, "polygon", label="license_plate", occluded="0", source="manual",
                        points=pts)
            image.text = polygon

    tree = ET.ElementTree(root)
    tree.write(os.path.join("annotations_cvat.xml"))
    