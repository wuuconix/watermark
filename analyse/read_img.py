#!/usr/bin/env python3
# coding=utf-8
# @Time    : 2020/8/13
# @Author  : github.com/guofei9987

import numpy as np
import cv2
from pywt import dwt2

class WaterMark:
    def __init__(self, password_wm=1, password_img=1, block_shape=(4, 4), mode='common', processes=None):
        self.block_shape = np.array(block_shape)
        self.password_wm, self.password_img = password_wm, password_img  # 打乱水印和打乱原图分块的随机种子
        self.d1, self.d2 = 36, 20  # d1/d2 越大鲁棒性越强,但输出图片的失真越大

        # init data
        self.img, self.img_YUV = None, None  # self.img 是原图，self.img_YUV 对像素做了加白偶数化
        self.ca, self.hvd, = [np.array([])] * 3, [np.array([])] * 3  # 每个通道 dct 的结果
        self.ca_block = [np.array([])] * 3  # 每个 channel 存一个四维 array，代表四维分块后的结果
        self.ca_part = [np.array([])] * 3  # 四维分块后，有时因不整除而少一部分，self.ca_part 是少这一部分的 self.ca

        self.wm_size, self.block_num = 0, 0  # 水印的长度，原图片可插入信息的个数

    def read_img(self, filename):
        # 读入图片->YUV化->加白边使像素变偶数->四维分块
        self.img = cv2.imread(filename).astype(np.float32)
        print(f"img:{self.img}\n")
        self.img_shape = self.img.shape[:2]
        print(f"img_shape:{self.img_shape}\n")
        # 如果不是偶数，那么补上白边
        self.img_YUV = cv2.copyMakeBorder(cv2.cvtColor(self.img, cv2.COLOR_BGR2YUV),
                                          0, self.img.shape[0] % 2, 0, self.img.shape[1] % 2,
                                          cv2.BORDER_CONSTANT, value=(0, 0, 0))
        print(f"img_YUV:{self.img_YUV}\n")

        self.ca_shape = [(i + 1) // 2 for i in self.img_shape]

        print(f"ca_shape:{self.ca_shape}\n")
        self.ca_block_shape = (self.ca_shape[0] // self.block_shape[0], self.ca_shape[1] // self.block_shape[1],
                               self.block_shape[0], self.block_shape[1])

        print(f"ca_block_shape:{self.ca_block_shape}\n")

        strides = 4 * np.array([self.ca_shape[1] * self.block_shape[0], self.block_shape[1], self.ca_shape[1], 1])

        print(f"strides:{strides}\n")

        print(f"self.img_YUV[:, :, 0]:{self.img_YUV[:, :, 0]}\n")
        print(f"self.img_YUV[:, :, 1]:{self.img_YUV[:, :, 1]}\n")
        print(f"self.img_YUV[:, :, 2]:{self.img_YUV[:, :, 2]}\n")
        for channel in range(3):
            self.ca[channel], self.hvd[channel] = dwt2(self.img_YUV[:, :, channel], 'haar')
            print(f"self.ca[{channel}]: {self.ca[channel]}\n")
            print(f"self.hvd[{channel}]: {self.hvd[channel]}\n")
            # 转为4维度
            self.ca_block[channel] = np.lib.stride_tricks.as_strided(self.ca[channel].astype(np.float32),
                                                                     self.ca_block_shape, strides)
            print(f"self.ca_block[{channel}]: {self.ca_block[channel]}\n")

test = WaterMark()
test.read_img("/root/watermark/origin/origin.jpg")