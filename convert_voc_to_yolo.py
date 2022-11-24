import xml.etree.ElementTree as ET
import glob
import os
import json
import sys


def xml_to_yolo_bbox(bbox, w, h):
    # xmin, ymin, xmax, ymax
    x_center = ((bbox[2] + bbox[0]) / 2) / w
    y_center = ((bbox[3] + bbox[1]) / 2) / h
    width = (bbox[2] - bbox[0]) / w
    height = (bbox[3] - bbox[1]) / h
    return [x_center, y_center, width, height]


def yolo_to_xml_bbox(bbox, w, h):
    # x_center, y_center width heigth
    w_half_len = (bbox[2] * w) / 2
    h_half_len = (bbox[3] * h) / 2
    xmin = int((bbox[0] * w) - w_half_len)
    ymin = int((bbox[1] * h) - h_half_len)
    xmax = int((bbox[0] * w) + w_half_len)
    ymax = int((bbox[1] * h) + h_half_len)
    return [xmin, ymin, xmax, ymax]


classes = [" ", "D00", "D10", "D20", "D40"]
input_dir = sys.argv[1]
output_dir = sys.argv[2]

count_files_used = 0

d00 = 0
d10 = 0
d20 = 0
d40 = 0

# create the labels folder (output directory)
os.mkdir(output_dir)

# identify all the xml files in the annotations folder (input directory)
files = glob.glob(os.path.join(input_dir, '*.xml'))
# loop through each 
for fil in files:
    basename = os.path.basename(fil)
    filename = os.path.splitext(basename)[0]

    result = []

    # parse the content of the xml file
    tree = ET.parse(fil)
    root = tree.getroot()
    #width = 2044
    width = int(root.find("size").find("width").text)
    height = int(root.find("size").find("height").text)

    for obj in root.findall('object'):
        label = obj.find("name").text
        pil_bbox = [int(float(x.text)) for x in obj.find("bndbox")]

        #if (pil_bbox[2] > 2044):
         #   continue

        if label == 'D00':
            d00 += 1
        
        if label == 'D10':
            d10 += 1

        if label == 'D20':
            d20 += 1

        if label == 'D40':
            d40 += 1

        if label == 'D00' or label == 'D10' or label == 'D20' or label == 'D40':
            # check for new classes and append to list
            if label not in classes:
                classes.append(label)
            index = classes.index(label)
            yolo_bbox = xml_to_yolo_bbox(pil_bbox, width, height)
            # convert data to string
            bbox_string = " ".join([str(x) for x in yolo_bbox])
            result.append(f"{index} {bbox_string}")

    if result:
        count_files_used += 1
        # generate a YOLO format text file for each xml file
        with open(os.path.join(output_dir, f"{filename}.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(result))

# generate the classes file as reference
with open('classes.txt', 'w', encoding='utf8') as f:
    f.write(json.dumps(classes))

print("count imaged used: " + str(count_files_used))
print("D00: " + str(d00))
print("D10: " + str(d10))
print("D20: " + str(d20))
print("D40: " + str(d40))