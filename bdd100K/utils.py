import json
import os
from typing import List, Optional, Dict
from scalabel.label.transforms import rle_to_mask
import numpy as np


def create_pan_mask_dict(pan_json_path: str) -> Dict[str, np.array]:
    if not os.path.exists(pan_json_path):
        return None
    with open(pan_json_path, "rb") as fp:
        fp_content = json.load(fp)
    frames = fp_content["frames"]
    result = dict()
    for frame in frames:
        img_name = frame['name']
        labels = frame["labels"]
        pan_dict = {
            "person":[], "rider":[], "bicycle":[], "bus":[], "car":[], 
            "caravan":[], "motorcycle":[], "trailer":[], "train":[], 
            "truck":[], "dynamic":[], "ego vehicle":[], "ground":[], 
            "static":[], "parking":[], "rail track":[], "road":[], 
            "sidewalk":[], "bridge":[], "building":[], "fence":[], 
            "garage":[], "guard rail":[], "tunnel":[], "wall":[], 
            "banner":[], "billboard":[], "lane divider":[], 
            "parking sign":[], "pole":[], "polegroup":[], "street light":[], 
            "traffic cone":[], "traffic device":[], "traffic light":[], 
            "traffic sign":[], "traffic sign frame":[], "terrain":[], 
            "vegetation":[], "sky":[], "unlabeled":[]
        }
        result[img_name] = pan_dict
        for label in labels:
            result[img_name][label["category"]].append(rle_to_mask(label["rle"]))
    return result


def get_transient_mask(pan_seg_dict, image_name, shape):
    """
    Create transient mask that contains transient objects(car, bike so on) and ego vehicle
    """
    mask = np.zeros(shape)
    if len(pan_seg_dict[image_name]['ego vehicle']) != 0:
        mask += pan_seg_dict[image_name]['ego vehicle'][0]
    transient_instances = pan_seg_dict[image_name]['car'] + pan_seg_dict[image_name]['bus'] + pan_seg_dict[image_name]['truck'] + \
                          pan_seg_dict[image_name]['person'] + pan_seg_dict[image_name]['rider'] + pan_seg_dict[image_name]['bicycle']
    if len(transient_instances)!=0:    
        for instance_mask in transient_instances:
            mask += instance_mask 
    return 1-mask
