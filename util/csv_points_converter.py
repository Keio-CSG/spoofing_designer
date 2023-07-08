import numpy as np
import math

from typing import List, Optional


FIRST_LASER_ID = 15
SAMPLING_RATE_NS = 32

MAX_PULSE_LENGTH = (131072 * SAMPLING_RATE_NS) // 2304

VERTICAL_ANGLES: List[Optional[int]] = [
    -15, 1, -13, 3, -11, 5, -9, 7, -7, 9, -5, 11, -3, 13, -1, 15,
    None, None, None, None, None, None, None, None
]

def vertical_to_angle(vertical: int) -> Optional[int]:
    return VERTICAL_ANGLES[FIRST_LASER_ID - 24 + vertical]

def vertical_angle_to_img_index(vertical_angle: int) -> int:
    return (15-vertical_angle) // 2

def spherical_to_cartesian(azimuth_deg: float, vertical_id: int, offset_m: float) -> List[float]:
    """
    球面座標から点を生成する
    """
    vertical_angle_deg = vertical_to_angle(vertical_id)
    xy = offset_m * math.cos(-azimuth_deg * math.pi / 180)
    return [xy * math.sin(vertical_angle_deg * math.pi / 180), xy * math.cos(vertical_angle_deg * math.pi / 180), offset_m * math.sin(-azimuth_deg * math.pi / 180)]

def convert_to_points(str_matrix: np.ma.masked_array, distance_m: float) -> List:
    """
    csvからパースしたデータを表示用に直交座標系の点群に変換する
    """
    points = []
    # print("sampling rate:", SAMPLING_RATE_NS, "ns")
    azimuth_size = math.ceil(MAX_PULSE_LENGTH / 24)
    # print(f"canvas size is 16x{azimuth_size}")
    for azimuth in range(0, azimuth_size):
        if azimuth >= str_matrix.shape[1]:
            continue
        for vertical in range(0, 24):
            vertical_angle = vertical_to_angle(vertical)
            if vertical_angle is not None and str_matrix.mask[vertical_angle_to_img_index(vertical_angle), azimuth]:
                delay = str_matrix.data[vertical_angle_to_img_index(vertical_angle), azimuth]
                # delayからoffsetを計算。delay [無次元] * SAMPLING_RATE_NS [ns] * 0.3 [m/ns] * 0.5 [謎のファクター] = offset [m]
                offset = delay * SAMPLING_RATE_NS * 0.5 * 0.3
                # azimuthは0.2°間隔、先頭(delay=0)をdistance_mとする
                points.append(spherical_to_cartesian(azimuth * 0.2, vertical, offset + distance_m))

    return points