#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @file: yolo.py
# @author: jerrzzy
# @date: 2023/9/6


import torch
import cv2
import numpy as np
from PIL import Image
from torch import nn
from models.detector.utils.utils import cvtColor, get_anchors, get_classes, preprocess_input, resize_image
from models.detector.utils.utils_bbox import DecodeBox
from models.detector.nets.yolo import YoloBody


class YOLODetector(object):
    _defaults = {
        "model_path": 'models/detector/model_data/last_epoch_weights.pth',
        "classes_path": 'models/detector/model_data/worm_classes.txt',
        "anchors_path": 'models/detector/model_data/yolo_anchors.txt',
        "anchors_mask": [[6, 7, 8], [3, 4, 5], [0, 1, 2]],
        "input_shape": [960, 1280],
        "phi": 'l',
        "confidence": 0.35,
        "nms_iou": 0.3,
        "cuda": True,
    }

    @classmethod
    def get_defaults(cls, n):
        if n in cls._defaults:
            return cls._defaults[n]
        else:
            return "Unrecognized attribute name '" + n + "'"

    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults)
        for name, value in kwargs.items():
            setattr(self, name, value)
            self._defaults[name] = value
        self.class_names, self.num_classes = get_classes(self.classes_path)
        self.anchors, self.num_anchors = get_anchors(self.anchors_path)
        self.bbox_util = DecodeBox(self.anchors, self.num_classes, (self.input_shape[0], self.input_shape[1]),
                                   self.anchors_mask)
        self.generate()

    def generate(self):
        self.net = YoloBody(self.anchors_mask, self.num_classes, self.phi)
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.net.load_state_dict(torch.load(self.model_path, map_location=device))
        self.net = self.net.fuse().eval()
        if self.cuda:
            self.net = nn.DataParallel(self.net)
            self.net = self.net.cuda()

    def detect(self, ori_img):
        image = Image.fromarray(cv2.cvtColor(ori_img, cv2.COLOR_BGR2RGB))
        image_shape = np.array(np.shape(image)[0:2])
        image = cvtColor(image)
        image_data, nw, nh = resize_image(image, (self.input_shape[1], self.input_shape[0]))
        image_data = np.expand_dims(np.transpose(preprocess_input(np.array(image_data, dtype='float32')), (2, 0, 1)), 0)
        with torch.no_grad():
            images = torch.from_numpy(image_data)
            if self.cuda:
                images = images.cuda()
            outputs = self.net(images)
            outputs = self.bbox_util.decode_box(outputs)
            results = self.bbox_util.non_max_suppression(torch.cat(outputs, 1), self.num_classes, self.input_shape,
                                                         image_shape, conf_thres=self.confidence,
                                                         nms_thres=self.nms_iou)
            if results[0] is None:
                return []
            else:
                top_boxes = results[0][:, :4]
                bboxes = []
                for (top, left, bottom, right) in top_boxes:
                    top = max(0, np.floor(top).astype('int32'))
                    left = max(0, np.floor(left).astype('int32'))
                    bottom = min(image.size[1], np.floor(bottom).astype('int32'))
                    right = min(image.size[0], np.floor(right).astype('int32'))
                    bboxes.append([top, left, bottom, right])
                return bboxes