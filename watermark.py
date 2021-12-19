from blind_watermark import WaterMark

def embed(oriImg:str, wmImg:str):
    bwm1 = WaterMark(password_wm=1, password_img=1)
    bwm1.read_img(f'pic/{oriImg}') # 原图位置
    bwm1.read_wm(f'pic/{wmImg}') # 水印位置
    embedImg = oriImg[: -4] + "_embed" + oriImg[-4:] #在原图文件名基础上加上 _embed 表示该图片已经被嵌入了水印
    bwm1.embed(f'pic/{embedImg}') # 嵌入水印后的图片
    return embedImg

def extract(syncImg:str, width:int, height:int):
    bwm1 = WaterMark(password_wm=1, password_img=1)
    extrImg = syncImg[: -4] + "_extract" + syncImg[-4:] #在原sync文件名基础上加上 _extract 表示该图片是已经被提取出来的水印
    bwm1.extract(filename=f'pic/{syncImg}', wm_shape=(width, height), out_wm_name=f'pic/{extrImg}', ) # wm_shape 指定水印大小
    return extrImg
