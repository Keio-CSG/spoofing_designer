import numpy as np

def is_integer(s):
    try:
        int(s)
    except ValueError:
        return False
    else:
        return True

v_is_integer = np.vectorize(is_integer)

def load_csv_with_mask(path: str):
    """
    数字の部分だけマスクして読み込む
    """
    data = np.loadtxt(path, delimiter=",", dtype=np.object_)
    mask = v_is_integer(data)
    data = np.where(mask, data, 0).astype(np.int32)
    return np.ma.masked_array(data, mask)
