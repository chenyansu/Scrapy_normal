#!/usr/bin/env python3
#coding:utf-8

__author__ = "chenyansu"

import platform
import os

def find_in_Path_no_print(file):
    """ 发现某文件是否在PATH里，此处用以判断selenium驱动 """
    if platform.system() == 'Windows':
        split_1 = '\\'
        split_2 = ';'
        # 会在windows系统后自动添加.exe后缀，可以删除postfix改正
        postfix = '.exe'
    else:
        split_1 = '/'
        split_2 = ':'
        postfix = ''
    pathes = os.getenv('PATH')
    path_list = pathes.split(split_2)
    judge_num = 0
    for i in path_list:
        exist_test = os.path.exists(i + split_1 + file + postfix)
        if exist_test == True:
            judge_num += 1
    if judge_num == 0:
        return False
    else:
        return True