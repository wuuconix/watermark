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

def resize_att(oriImgName, out_shape=(500, 500)):
    # 缩放攻击：因为攻击和还原都是缩放，所以攻击和还原都调用这个函数
    oriImg = cv2.imread(f"pic/{oriImgName}")
    rstImg = cv2.resize(oriImg, dsize=out_shape)
    rstImgName = oriImgName[0: -4] + f"_resize_{out_shape[0]}_{out_shape[1]}" + oriImgName[-4:]
    cv2.imwrite(f"pic/{rstImgName}", rstImg)
    return rstImgName

def bright_att(oriImgName, ratio=0.8):
    # 亮度调整攻击，ratio应当多于0
    # ratio>1是调得更亮，ratio<1是亮度更暗
    oriImg = cv2.imread(f"pic/{oriImgName}")
    rstImg = oriImg * ratio
    rstImg[rstImg > 255] = 255
    rstImgName = oriImgName
    cv2.imwrite(rstImgName, rstImg)

def shelter_att(oriImgName, ratio=0.1, n=3):
    # 遮挡攻击：遮挡图像中的一部分
    # n个遮挡块
    # 每个遮挡块所占比例为ratio
    oriImg = cv2.imread(f"pic/{oriImgName}")
    oriImg_shape = oriImg.shape
    rstImg = oriImg.copy()
    for i in range(n):
        tmp = np.random.rand() * (1 - ratio)  # 随机选择一个地方，1-ratio是为了防止溢出
        start_height, end_height = int(tmp * oriImg_shape[0]), int((tmp + ratio) * oriImg_shape[0])
        tmp = np.random.rand() * (1 - ratio)
        start_width, end_width = int(tmp * oriImg_shape[1]), int((tmp + ratio) * oriImg_shape[1])
        rstImg[start_height:end_height, start_width:end_width, :] = 0
    rstImgName = oriImgName
    cv2.imwrite(rstImgName, rstImg)

def rot_att(oriImgName, angle=45):
    # 旋转攻击
    oriImg = cv2.imread(f"pic/{oriImgName}")
    rows, cols, _ = oriImg.shape
    M = cv2.getRotationMatrix2D(center=(cols / 2, rows / 2), angle=angle, scale=1)
    rstImg = cv2.warpAffine(oriImg, M, (cols, rows))
    rstImgName = oriImgName[0: -4] + f"_rot{angle}" + oriImgName[-4:]
    cv2.imwrite(f"pic/{rstImgName}", rstImg)
    return rstImgName

# resize_att('a.jpg', (400, 400))