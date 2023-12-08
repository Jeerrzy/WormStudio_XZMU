#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @file: config.py
# @author: jerrzzy
# @date: 2023/7/17


import json


config_file_path = './database/config/config.json'


if __name__ == "__main__":
    cfg = {
        "input_shape": [960, 1280],
        "cuda": True,
        "confidence": 0.5,
        "nms_iou": 0.3,
        "max_age": 30,
        "min_hints": 0,
        "iou_threshold": 0.1,
        "optimize_rate": 0.2,
        "st_ratio": 0.5,
        "center_x": 0.5,
        "center_y": 0.5,
        "radius": 0.5,
        "contact_iou_threshold": 0.3,
        "contact_interval_threshold": 10,
        "colors": [
            [127, 0, 85],
            [0, 85, 170],
            [0, 255, 255],
            [255, 170, 85],
            [0, 85, 0],
            [184, 212, 255],
            [166, 255, 219],
            [127, 0, 0],
            [142, 255, 134],
            [0, 85, 85],
            [158, 255, 200],
            [127, 0, 255],
            [127, 0, 255],
            [171, 255, 219],
            [255, 85, 255],
            [255, 0, 85]
        ]
    }
    with open(config_file_path, 'w') as f:
        json.dump(cfg, f, indent=2)

