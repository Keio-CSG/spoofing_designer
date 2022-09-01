"""
出来上がったcsvデータをFGの入力データに変換する
"""

import csv
import math

from util.load_csv_with_mask import load_csv_with_mask

FIRST_LASER_ID = 15
SAMPLING_RATE_NS = 32

MAX_PULSE_LENGTH = (131072 * SAMPLING_RATE_NS) // 2304

VERTICAL_ANGLES = [
    -15, 1, -13, 3, -11, 5, -9, 7, -7, 9, -5, 11, -3, 13, -1, 15,
    None, None, None, None, None, None, None, None
]

def vertical_to_angle(vertical):
    return VERTICAL_ANGLES[FIRST_LASER_ID - 24 + vertical]

def vertical_angle_to_img_index(vertical_angle):
    return (15-vertical_angle) // 2

masked_data = load_csv_with_mask("yoshi.csv")

# 一旦1ns間隔でパルスを生成
data_one_nano = []
print("sampling rate:", SAMPLING_RATE_NS, "ns")
azimuth_size = math.ceil(MAX_PULSE_LENGTH / 24)
print(f"canvas size is 16x{azimuth_size}")
for azimuth in range(0, azimuth_size):
    for vertical in range(0, 24):
        vertical_angle = vertical_to_angle(vertical)
        if vertical_angle is not None:
            if masked_data.mask[vertical_angle_to_img_index(vertical_angle), azimuth]:
                delay = masked_data[vertical_angle_to_img_index(vertical_angle), azimuth]
                for _ in range(delay * SAMPLING_RATE_NS):
                    data_one_nano.append(False)
                for _ in range(200):
                    data_one_nano.append(True)
                for _ in range(2304-200 - delay * SAMPLING_RATE_NS):
                    data_one_nano.append(False)
                continue
        
        # パルスを出さない場合は0で埋める
        for _ in range(2304):
            data_one_nano.append(False)

max_ns = len(data_one_nano) - 1

# サンプリングレートに合わせてパルスをサンプル
data_sampled = []
pulse_delay = [0]
is_invalid = False
for i in range(0, max_ns, SAMPLING_RATE_NS):
    if data_one_nano[i]:
        if not is_invalid:
            data_sampled.append([1,1])
        else:
            data_sampled.append([-1,-1])
        if len(data_sampled) >= 2 and data_sampled[-2][0] == -1:
            back = i - 1
            count = 0
            while back >= 0 and data_one_nano[back]:
                back -= 1
                count += 1
            pulse_delay.append(count)
    else:
        data_sampled.append([-1,-1])
        is_invalid = False

if len(data_sampled) > 131072:
    data_sampled = data_sampled[:131072]
print(len(data_sampled))
print(len(data_sampled) * SAMPLING_RATE_NS, 'ns')

with open("wall_freq.txt", "w") as f:
    f.write(str(10**9 / (len(data_sampled) * SAMPLING_RATE_NS)))

with open("wall.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data_sampled)