import numpy as np
from multiprocessing import Pool

h, w = 1080, 1920

def draw_pixel():
    pixel = np.zeros(24, dtype=np.uint8)
    for i in range(24):
        pixel[i] = np.random.randint(0, 2)
    return pixel

def draw_row(p):
    row = np.zeros((24, w), dtype=np.uint8)
    row[:, 0] = draw_pixel()
    for j in range(1, w):
        if np.random.binomial(1, p):
            row[:, j] = draw_pixel()
        else:
            row[:, j] = row[:, j-1]
    return row

def draw(p, pool_size=4, chunk_size=10):
    with Pool(pool_size) as pool:
        rows = pool.map(draw_row, [p]*h, chunksize=chunk_size)
    imgs = np.zeros((24, h, w), dtype=np.uint8)
    for i, row in enumerate(rows):
        imgs[:, i, :] = row
    return imgs

def draw_single_process(p):
    imgs = np.zeros((24, h, w), dtype=np.uint8)
    for i in range(h):
        imgs[:, i, :] = draw_row(p)
    return imgs