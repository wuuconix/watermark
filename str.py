from blind_watermark import WaterMark
import sys

if (sys.argv[1] == "embed"):
    bwm1 = WaterMark(password_img=1, password_wm=1)
    bwm1.read_img('origin/origin.jpg')
    wm = 'flag{wuuconix yyds!}'
    bwm1.read_wm(wm, mode='str')
    bwm1.embed('embedded/embedded_str.png')
    len_wm = len(bwm1.wm_bit)
    print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))

elif (sys.argv[1] == "extract"):
    bwm1 = WaterMark(password_img=1, password_wm=1)
    wm_extract = bwm1.extract('embedded/embedded_str.png', wm_shape=159, mode='str')
    print(wm_extract)

else:
    print("try like python3 str.py embed/extract")