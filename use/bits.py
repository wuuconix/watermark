from blind_watermark import WaterMark
import sys

if (sys.argv[1] == "embed"):
    bwm1 = WaterMark(password_img=1, password_wm=1)
    bwm1.read_img('origin/origin.jpg')
    bwm1.read_wm([True, False, True, True, True, False], mode='bit')
    bwm1.embed('embedded/embedded_bit.png')

elif (sys.argv[1] == "extract"):
    bwm1 = WaterMark(password_img=1, password_wm=1, wm_shape=6)
    wm_extract = bwm1.extract('embedded/embedded_bit.png', mode='bit')
    print(wm_extract)

else:
    print("try like python3 bits.py embed/extract")