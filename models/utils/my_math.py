#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @file: my_math.py
# @author: jerrzzy
# @date: 2023/7/13


import os
import json
import math
import numpy as np


def IOU(boxA, boxB):
    boxA = [int(x) for x in boxA]
    boxB = [int(x) for x in boxB]
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
    iou = interArea / float(boxAArea + boxBArea - interArea)
    return iou


def get_individual_math_results(result_dir, trk_seq_path, width, height, center_x, center_y, radius, contact_iou_threshold, contact_interval_threshold):
    """
    从MOT追踪文件格式中计算目标个体关键参数指标并保存为字典格式
    :param result_dir: 保存结果路径
    :param trk_seq_path: MOT格式追踪序列数据
    :return: None 结果以json文件保存
    """
    result_dict = dict()
    trk_data = np.loadtxt(trk_seq_path, dtype=int, delimiter=',')
    if not len(trk_data) > 0:
        return None
    # 计算每个ID号码的指标
    trajectory_num = int(trk_data[:, 1].max())
    result_dict['number'] = trajectory_num
    # 序号问题
    user_cy, user_cx = center_x * width, center_y * height
    r = radius * min(height, width)
    for worm_id in range(1, trajectory_num + 1):
        id_dict = dict()
        speed, swing, contact = [], [], []
        in_out_num = 0
        id_data = trk_data[trk_data[:, 1] == worm_id]
        _, _, x0, y0, w0, h0, _, _, _, _ = id_data[0]
        cx0, cy0 = int(x0+w0/2), int(y0+h0/2)
        state0 = (math.sqrt((cx0-user_cx)**2+(cy0-user_cy)**2)) <= r
        for f, _, x, y, w, h, _, _, _, _ in id_data:
            cx, cy = int(x + w / 2), int(y + h / 2)
            state = (math.sqrt((cx0 - user_cx) ** 2 + (cy0 - user_cy) ** 2)) <= r
            if state0 is not state:
                in_out_num += 1
            speed.append(math.sqrt((cx-cx0)**2+(cy-cy0)**2))
            swing.append(abs(w/h-w0/h0))
            cx0, cy0, w0, h0 = cx, cy, w, h
            state0 = state
        id_dict['frame'] = len(id_data)
        id_dict['speed'] = np.mean(np.array(speed))
        id_dict['swing'] = np.mean(np.array(swing))
        id_dict['contact'] = contact
        id_dict['in_out'] = in_out_num
        result_dict[str(worm_id)] = id_dict
    # 判定每个ID号码的社会行为
    contact_time_matrix = np.zeros((trajectory_num, trajectory_num))
    contact_num_matrix = np.zeros((trajectory_num, trajectory_num))
    frame_num = int(trk_data[:, 0].max())
    for frame_id in range(1, frame_num + 1):
        frame_data = trk_data[trk_data[:, 0] == frame_id]
        id_num = int(frame_data[:, 1].max())
        for i in range(1, id_num+1):
            for j in range(i+1, id_num+1):
                id_i_data = frame_data[frame_data[:, 1] == i]
                id_j_data = frame_data[frame_data[:, 1] == j]
                if len(id_i_data) == 1 and len(id_j_data) == 1:
                    _, _, x0, y0, w0, h0, _, _, _, _ = id_i_data[0]
                    _, _, x1, y1, w1, h1, _, _, _, _ = frame_data[frame_data[:, 1] == j][0]
                    bbox0 = [x0, y0, x0+w0, y0+h0]
                    bbox1 = [x1, y1, x1+w1, y1+h1]
                    if IOU(bbox0, bbox1) > contact_iou_threshold:
                        contact_time_matrix[i-1][j-1] += 1
                        contact_time_matrix[j-1][i-1] += 1
                        if len(result_dict[str(i)]['contact']) > 0:
                            last_frame_id, last_worm_id = result_dict[str(i)]['contact'][-1]
                            if last_worm_id == j and (frame_id-last_frame_id) <= contact_interval_threshold:
                                # 保持纠缠
                                pass
                            else:
                                contact_num_matrix[i - 1][j - 1] += 1
                                contact_num_matrix[j - 1][i - 1] += 1
                        else:
                            contact_num_matrix[i - 1][j - 1] += 1
                            contact_num_matrix[j - 1][i - 1] += 1
                        result_dict[str(i)]['contact'].append([frame_id, j])
                        result_dict[str(j)]['contact'].append([frame_id, i])
    # 整理社会行为指标
    for i in range(1, trajectory_num+1):
        id_dict = result_dict[str(i)]
        id_dict['contact_time'] = int(np.sum(np.array(contact_time_matrix[i-1, :])))
        id_dict['contact_num'] = int(np.sum(np.array(contact_num_matrix[i-1, :])))
    result_dict['contact_time_matrix'] = contact_time_matrix
    result_dict['contact_num_matrix'] = contact_num_matrix
    # 整理平均指标
    aver_speed, aver_swing, aver_contact_time, aver_contact_number, aver_in_out_number = [], [], [], [], []
    for i in range(1, trajectory_num+1):
        id_dict = result_dict[str(i)]
        aver_speed.append(id_dict['speed'])
        aver_swing.append(id_dict['swing'])
        aver_contact_time.append(id_dict['contact_time'])
        aver_contact_number.append(id_dict['contact_num'])
        aver_in_out_number.append(id_dict['in_out'])
    result_dict['aver_speed'] = np.mean(np.array(aver_speed))
    result_dict['aver_swing'] = np.mean(np.array(aver_swing))
    result_dict['aver_contact_time'] = np.mean(np.array(aver_contact_time))
    result_dict['aver_contact_number'] = np.mean(np.array(aver_contact_number))
    result_dict['aver_in_out_number'] = np.mean(np.array(aver_in_out_number))
    with open(os.path.join(result_dir, 'result.json'), 'w') as f:
        json.dump(result_dict, f, indent=2, cls=NumpyArrayEncoder)


class NumpyArrayEncoder(json.JSONEncoder):
    """重写JSONEncoder中的default方法"""
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
