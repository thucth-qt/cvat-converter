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
                "tl_x": points[0],
                "tl_y": points[1],
                "tr_x": points[2],
                "tr_y": points[3],
                "br_x": points[4],
                "br_y": points[5],
                "bl_x": points[6],
                "bl_y": points[7],
                "width": int(attrib["width"]),
                "height": int(attrib["height"]),
                "class_name": polygon_elm.attrib["label"]
            }

            lst.append(row)
    
    df = pd.DataFrame(lst)

    return df


def save_annotation(df, output_dir):
    for idx, row in df.iterrows():
        tl_x = row["tl_x"] / row["width"]
        tl_y = row["tl_y"] / row["height"]

        tr_x = row["tr_x"] / row["width"]
        tr_y = row["tr_y"] / row["height"]

        br_x = row["br_x"] / row["width"]
        br_y = row["br_y"] / row["height"]

        bl_x = row["bl_x"] / row["width"]
        bl_y = row["bl_y"] / row["height"]

        label = [4, tl_x, tl_y, tr_x, tr_y, br_x, br_y, bl_x, bl_y, '', '']
        label_txt = ','.join(str(x) for x in label)

        ext = os.path.splitext(row["path"])[-1]
        filename = row["path"].replace(ext, ".txt")
        with open(os.path.join(output_dir, filename), 'a') as f:
            f.write(label_txt + '\n')



if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument('--annotation', type=str, default="data/annotations.xml")
    parse.add_argument('--output-dir', type=str, default="./")
    opt = parse.parse_args()

    root_xml = parseXML(opt.annotation)
    df = cvat2c9(root_xml)
    save_annotation(df, opt.output_dir)
