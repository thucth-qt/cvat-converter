import os
import argparse
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd


def parseXML(xml_path):
    root_xml = ET.parse(xml_path)
    return root_xml


def cvat2yolo(root_xml):
    lst = []

    for idx, image_tag in enumerate(root_xml.findall("image")):
        attrib = image_tag.attrib
        
        polygons = [elem for elem in image_tag.iter() if elem is not image_tag]
        for polygon_elm in polygons:
            try:
                points = polygon_elm.attrib["points"].replace(';', ',').split(',')
                points = [float(x) for x in points]
                points = np.array(points).reshape(-1, 2)

                tl_x, tl_y = np.min(points, axis=0)
                br_x, br_y = np.max(points, axis=0)
            except AttributeError:
                print("Annotation for %s not exists." % attrib["name"])
                continue

            row = {
                "path": attrib["name"],
                "tl_x": tl_x,
                "tl_y": tl_y,
                "br_x": br_x,
                "br_y": br_y,
                "width": int(attrib["width"]),
                "height": int(attrib["height"]),
                "class_name": polygon_elm.attrib["label"]
            }

            lst.append(row)
    
    df = pd.DataFrame(lst)
    
    return df


def save_annotation(df, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        import shutil
        shutil.rmtree(output_dir)
        os.makedirs(output_dir)

    for idx, row in df.iterrows():
        tl_x = row["tl_x"] / row["width"]
        tl_y = row["tl_y"] / row["height"]

        br_x = row["br_x"] / row["width"]
        br_y = row["br_y"] / row["height"]

        center_x = (tl_x + br_x) / 2
        center_y = (tl_y + br_y) / 2

        w, h = (br_x - tl_x), (br_y - tl_y)

        file_name, ext = os.path.splitext(row["path"])
        file_path = os.path.join(output_dir, file_name + ".txt")

        with open(file_path, "a") as f:
            data = [0, center_x, center_y, w, h]
            f.write(' '.join(str(round(x, 6)) for x in data) + '\n')


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument('--annotation', type=str, default="data/annotations.xml")
    parse.add_argument('--output-dir', type=str, default="./")
    opt = parse.parse_args()

    root_xml = parseXML(opt.annotation)
    df = cvat2yolo(root_xml)
    save_annotation(df, opt.output_dir)
