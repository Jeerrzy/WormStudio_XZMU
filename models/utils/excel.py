#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @file: excel.py
# @author: jerrzzy
# @date: 2023/9/8


import os
import json
import xlsxwriter as xw


def get_excel_results(json_path, result_dir):
    """
    :param result_dir: 保存excel的结果路径
    :param json_path: 缓存数学结果的json路径
    """
    with open(json_path, 'r') as f:
        data = json.load(f)
    workbook = xw.Workbook(os.path.join(result_dir, f'result.xlsx'))
    # 1.记录数学结果
    worksheet = workbook.add_worksheet('math')
    worksheet.activate()
    header_names = ['WormID', 'Frames', 'Speed', 'Swing', 'ContactTime', 'ContactNumber', 'InOutFoodNumber']
    worksheet.set_column('A:B', 10)
    worksheet.set_column('B:C', 20)
    worksheet.set_column('C:D', 20)
    worksheet.set_column('D:E', 20)
    worksheet.set_column('E:F', 20)
    worksheet.set_column('F:G', 20)
    worksheet.set_column('G:H', 20)
    head_format = {
        'font_size': 15,  # 字体大小
        'bold': True,  # 是否粗体
        'font_color': '#9400D3',  # 字体颜色
        'align': 'center',  # 水平居中对齐
        'valign': 'vcenter',  # 垂直居中对齐
        'border': 1,  # 边框宽度
        'top': 1,  # 上边框
        'left': 1,  # 左边框
        'right': 1,  # 右边框
        'bottom': 1  # 底边框
    }
    content_format = {
        'font_size': 10,  # 字体大小
        'align': 'center',  # 水平居中对齐
        'valign': 'vcenter'  # 垂直居中对齐
    }
    head_style = workbook.add_format(head_format)
    worksheet.write_row('A1', header_names, head_style)
    content_style = workbook.add_format(content_format)
    for i in range(1, data['number']+1):
        id_dict = data[str(i)]
        worksheet.write(i, 0, str(i), content_style)
        worksheet.write(i, 1, str(id_dict['frame']), content_style)
        worksheet.write(i, 2, str(id_dict['speed']), content_style)
        worksheet.write(i, 3, str(id_dict['swing']), content_style)
        worksheet.write(i, 4, str(id_dict['contact_time']), content_style)
        worksheet.write(i, 5, str(id_dict['contact_num']), content_style)
        worksheet.write(i, 6, str(id_dict['in_out']), content_style)
    # 2.接触时间
    worksheet = workbook.add_worksheet('contact_time')
    worksheet.activate()
    contact_time_matrix = data['contact_time_matrix']
    for i in range(1, data['number']+1):
        worksheet.write(0, i, str(i), head_style)
        worksheet.write(i, 0, str(i), head_style)
    for i in range(data['number']):
        for j in range(data['number']):
            worksheet.write(i+1, j+1, str(contact_time_matrix[i][j]), content_style)
    # 3.接触次数
    worksheet = workbook.add_worksheet('contact_num')
    worksheet.activate()
    contact_num_matrix = data['contact_num_matrix']
    for i in range(1, data['number']+1):
        worksheet.write(0, i, str(i), head_style)
        worksheet.write(i, 0, str(i), head_style)
    for i in range(data['number']):
        for j in range(data['number']):
            worksheet.write(i+1, j+1, str(contact_num_matrix[i][j]), content_style)
    workbook.close()

