import threading
import time

from PIL import Image
import sys
import os
import shutil
import numpy as np

"""通过直方图计算两张图图片的相似度，适用于测试截图的比对"""
g_pic_dir = "F:\screenshots\screen"
g_ok_pic = "F:\screenshots\screen\screen1.jpg"
g_base_his = []
group_size = 50
THRESHOLD = 0.995
result = []


def hist_similar(lh, rh):
    print("checking...")
    if len(lh) != len(rh):
        return -1
    _sum = 0
    for l, r in zip(lh, rh):
        _res = 0.0
        if l == r:
            _res = 0
        else:
            _res = abs(l - r) / max(l, r)
        _sum += 1 - _res
    print(_sum / len(lh))
    return _sum / len(lh)
    # return sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r)) for l, r in zip(lh, rh)) / len(lh)


# I = Image.open(g_ok_pic).convert('L')
# I_array_ok = np.array(I)
def mtx_similar3(arr1: np.ndarray, arr2: np.ndarray) -> float:
    # 判断图片矩阵的相似度，将图片先转换为灰度图，然后转换位numpy矩阵传入,速度较直方图慢
    '''
    From CS231n: There are many ways to decide whether
    two matrices are similar; one of the simplest is the Frobenius norm. In case
    you haven't seen it before, the Frobenius norm of two matrices is the square
    root of the squared sum of differences of all elements; in other words, reshape
    the matrices into vectors and compute the Euclidean distance between them.
    difference = np.linalg.norm(dists - dists_one, ord='fro')
    :param arr1:矩阵1
    :param arr2:矩阵2
    :return:相似度（0~1之间）
    '''
    if arr1.shape != arr2.shape:
        minx = min(arr1.shape[0], arr2.shape[0])
        miny = min(arr1.shape[1], arr2.shape[1])
        differ = arr1[:minx, :miny] - arr2[:minx, :miny]
    else:
        differ = arr1 - arr2
    dist = np.linalg.norm(differ, ord='fro')
    len1 = np.linalg.norm(arr1)
    len2 = np.linalg.norm(arr2)  # 普通模长
    denom = (len1 + len2) / 2
    similar = 1 - (dist / denom)
    print(similar)
    return similar


def task(lists, _id):
    print("start thread id = %d" % _id)
    for file in lists:
        filename = os.path.join(g_pic_dir, file)
        if filename == g_ok_pic:
            continue
        try:
            img = Image.open(filename)
        except Exception as error:
            print(error)
            continue
        if hist_similar(g_base_his, img.histogram()) < THRESHOLD:
            result.append(filename)
        # i_array = np.array(img.convert('L'))
        # if mtx_similar3(I_array_ok, i_array) < 0.98:
        #    result.append(filename)


if __name__ == "__main__":
    # python findpic [截图保存的文件夹] [正确结果的截图]
    # 例如: python findpic.py F:\screenshots\screen screen1.jpg
    g_pic_dir = sys.argv[1]
    g_ok_pic_name = sys.argv[2]
    g_ok_pic = os.path.join(g_pic_dir, g_ok_pic_name)
    try:
        g_base_his = Image.open(g_ok_pic).histogram()
    except Exception as e:
        print(e)

    pic_lists = os.listdir(g_pic_dir)
    pic_lists_size = len(pic_lists)
    start = time.time()

    # 图片数量超过group_size的时候启用多线程
    if pic_lists_size > group_size:
        t_obj = []
        for i in range(0, pic_lists_size, group_size):
            b = pic_lists[i:i + group_size]
            t = threading.Thread(target=task, args=(b, int(i / group_size)))
            t.start()
            t_obj.append(t)
        # 等待子线程结束
        for t in t_obj:
            t.join()
    else:
        task(pic_lists, 0)
    # 打印并保存结果
    print(result)
    res_dir = os.path.join(g_pic_dir, 'res')
    if not os.path.exists(res_dir):
        os.mkdir(res_dir)
    for res in result:
        shutil.copy(res, res_dir)
    end = time.time()
    print("Exit after:{time}s".format(time=end - start))
