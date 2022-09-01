"""
白黒の画像をdesignerで使えるcsv形式に変換する
"""

import cv2
import math
import numpy as np

TARGET_IMG = "images/yoshi.png"
FIRST_LASER_ID = 12
SAMPLING_RATE_NS = 32
EXPAND_IMAGE = True

# 必要なパルス数
MAX_PULSE_LENGTH = math.ceil((131072 * SAMPLING_RATE_NS) / 2304)

azimuth_size = math.ceil((MAX_PULSE_LENGTH + FIRST_LASER_ID) / 24)

# 表示可能なキャンバスを定義
canvas = np.full((16, azimuth_size), False, dtype=bool)

im_gray = cv2.imread(TARGET_IMG, cv2.IMREAD_GRAYSCALE)
if im_gray.shape[0] != 16:
    im_gray = cv2.resize(im_gray, (im_gray.shape[1], 16))
if EXPAND_IMAGE:
    im_gray = cv2.resize(im_gray, (azimuth_size, 16))
if im_gray.shape[1] > azimuth_size:
    im_gray = im_gray[:, :azimuth_size]

# 閾値は画像ごとにいい感じに指定すること
canvas[:, :im_gray.shape[1]] = im_gray < 200

bin_csv = np.where(canvas, "0", "-")

# ファイル出力
np.savetxt("yoshi.csv", bin_csv, fmt="%s", delimiter=",")