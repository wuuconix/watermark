from blind_watermark import WaterMark
import sys

if (sys.argv[1] == "embed"):
    bwm1 = WaterMark(password_wm=1, password_img=1)
    bwm1.read_img('pic/origin.jpg') # 原图 1920 x 1080
    bwm1.read_wm('pic/watermark.png') # 二维码作为 水印 128 x 128
    bwm1.embed('pic/embedded.png') # 嵌入水印后的图片

elif (sys.argv[1] == "extract"):
    bwm1 = WaterMark(password_wm=1, password_img=1)
    bwm1.extract(filename='pic/embedded.png', wm_shape=(128, 128), out_wm_name='pic/extract.png', ) # wm_shape 指定水印大小

else:
    print("try like python3 test.py embed/extract")