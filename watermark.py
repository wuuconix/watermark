from blind_watermark import WaterMark
import cv2
import numpy as np

def embed(oriImg:str, wmImg:str):
    # 嵌入水印
    bwm1 = WaterMark(password_wm=1, password_img=1)
    bwm1.read_img(f'pic/{oriImg}') # 原图位置
    bwm1.read_wm(f'pic/{wmImg}') # 水印位置
    embedImg = oriImg[: -4] + "_embed" + oriImg[-4:] #在原图文件名基础上加上 _embed 表示该图片已经被嵌入了水印
    bwm1.embed(f'pic/{embedImg}') # 嵌入水印后的图片
    return embedImg

def extract(syncImg:str, width:int, height:int):
    # 提取水印
    bwm1 = WaterMark(password_wm=1, password_img=1)
    extrImg = syncImg[: -4] + "_extract" + syncImg[-4:] #在原sync文件名基础上加上 _extract 表示该图片是已经被提取出来的水印
    bwm1.extract(filename=f'pic/{syncImg}', wm_shape=(width, height), out_wm_name=f'pic/{extrImg}', ) # wm_shape 指定水印大小
    return extrImg

def cut_att_height(oriImgName, ratio=0.8):
    # 纵向剪切攻击
    oriImg = cv2.imread(f"pic/{oriImgName}")
    oriImg_shape = oriImg.shape
    height = int(oriImg_shape[0] * ratio)
    rstImgName = oriImgName[0: -4] + f"_cutHeight_{ratio}" + oriImgName[-4:]
    cv2.imwrite(f"pic/{rstImgName}", oriImg[:height, :, :])
    return rstImgName

def cut_att_width(oriImgName, ratio=0.8):
    # 横向裁剪攻击
    oriImg = cv2.imread(f"pic/{oriImgName}")
    oriImg_shape = oriImg.shape
    width = int(oriImg_shape[1] * ratio)
    rstImgName = oriImgName[0: -4] + f"_cutWidth_{ratio}" + oriImgName[-4:]
    cv2.imwrite(f"pic/{rstImgName}", oriImg[:, :width, :])
    return rstImgName

def anti_cut_att(oriImgName, origin_shape):
    # 反裁剪攻击：复制一块范围，然后补全
    # origin_shape 分辨率与约定理解的是颠倒的，约定的是列数*行数
    oriImg = cv2.imread(f"pic/{oriImgName}")
    rstImg = oriImg.copy()
    rstImg_shape = rstImg.shape
    if rstImg_shape[0] > origin_shape[0] or rstImg_shape[0] > origin_shape[0]:
        print('裁剪打击后的图片，不可能比原始图片大，检查一下')
        return
    # 还原纵向打击
    while rstImg_shape[0] < origin_shape[0]:
        rstImg = np.concatenate([rstImg, rstImg[:origin_shape[0] - rstImg_shape[0], :, :]], axis=0)
        rstImg_shape = rstImg.shape
    while rstImg_shape[1] < origin_shape[1]:
        rstImg = np.concatenate([rstImg, rstImg[:, :origin_shape[1] - rstImg_shape[1], :]], axis=1)
        rstImg_shape = rstImg.shape
    rstImgName = oriImgName[0: -4] + f"_antiCut" + oriImgName[-4:]
    cv2.imwrite(f"pic/{rstImgName}", rstImg)
    return rstImgName

def resize_att(oriImgName, out_shape=(500, 500)):
    # 缩放攻击：因为攻击和还原都是缩放，所以攻击和还原都调用这个函数
    oriImg = cv2.imread(f"pic/{oriImgName}")
    rstImg = cv2.resize(oriImg, dsize=out_shape)
    rstImgName = oriImgName[0: -4] + f"_resize_{out_shape[0]}_{out_shape[1]}" + oriImgName[-4:]
    cv2.imwrite(f"pic/{rstImgName}", rstImg)
    return rstImgName

def rot_att(oriImgName, angle=45):
    # 旋转攻击
    oriImg = cv2.imread(f"pic/{oriImgName}")
    rows, cols, _ = oriImg.shape
    M = cv2.getRotationMatrix2D(center=(cols / 2, rows / 2), angle=angle, scale=1)
    rstImg = cv2.warpAffine(oriImg, M, (cols, rows))
    rstImgName = oriImgName[0: -4] + f"_rot{angle}" + oriImgName[-4:]
    cv2.imwrite(f"pic/{rstImgName}", rstImg)
    return rstImgName
