import sys
import time
import cv2
from models.detector import YOLODetector
import cv2
import numpy as np
import json
from matplotlib import pyplot as plt
from tqdm import tqdm
from models.utils.my_math import *
from models.utils.draw import *
from models.utils.excel import *


if __name__ == "__main__":
    # unet = UnetDetector()
    # img = cv2.imread('./img/test.jpg')
    # results = unet.detect(img)
    # result_img = np.uint8(results * 255)
    # cv2.imshow('demo', result_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # a = {'name': 'jzy'}
    # b = {'old': 23}
    # c = {**a, **b}
    # print(c)
    # result = get_individual_math_results(trk_seq_path='./models/cache/video_01/cache.txt')
    # print(result)
    # get_food_area(input_video_path='./img/video_01.mp4', png_result_path='./img')
    # mask = unet.detect(img)
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))  # 获取矩形结构元
    # dst = cv2.morphologyEx(np.uint8(mask * 255), cv2.MORPH_CLOSE, kernel, iterations=10)
    # cv2.imwrite('./img/food_area.png', dst)
    # get_excel_results('./models/cache/video_01/math/result.json', './img')
    # worm_ids = np.array([i for i in range(1, 10+1)])
    # print(worm_ids)
    draw_math_results(
        json_path='./models/cache/video_01/math/result.json',
        out_image_dir='./img',
        colors=[
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
    )

