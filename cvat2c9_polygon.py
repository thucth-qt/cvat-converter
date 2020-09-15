import os
import argparse
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd


def parseXML(xml_path):
    root_xml = ET.parse(xml_path)
    return root_xml


def cvat2c9(root_xml):
    lst = []

    for idx, image_tag in enumerate(root_xml.findall("image")):
        attrib = image_tag.attrib
        
        polygons = [elem for elem in image_tag.iter() if elem is not image_tag]
        for polygon_elm in polygons:
            try:
                points = polygon_elm.attrib["points"].replace(';', ',').split(',')
                points = [float(x) for x in points]
            except AttributeError:
                print("Annotation for %s not exists." % attrib["name"])
                continue

            row = {
                "path": attrib["name"],
                "tl_x": int(points[0]),
                "tl_y": int(points[1]),
                "tr_x": int(points[2]),
                "tr_y": int(points[3]),
                "br_x": int(points[4]),
                "br_y": int(points[5]),
                "bl_x": int(points[6]),
                "bl_y": int(points[7]),
                "class_name": polygon_elm.attrib["label"]
            }

            lst.append(row)
    
    df = pd.DataFrame(lst)
    
    return df


def save_annotation(df, output_dir):
    df.to_csv(os.path.join(output_dir, "annotations_polygon.csv"), index=False)


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument('--annotation', type=str, default="data/annotations.xml")
    parse.add_argument('--output-dir', type=str, default="./")
    opt = parse.parse_args()

    root_xml = parseXML(opt.annotation)
    df = cvat2c9(root_xml)
    save_annotation(df, opt.output_dir)
