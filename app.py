from flask import Flask, request
from numpy import double
from watermark import embed, extract, rot_att, resize_att, cut_att_width, cut_att_height, anti_cut_att

app = Flask(__name__)

base_url = "https://watermark.wuuconix.link/pic/" #生成出来的图片的基址

def saveImg(img): #保存img
    img.save(f'pic/{img.filename}')
    print(f"save {img.filename} successfully")

@app.route('/embed', methods=['POST'])
def embedPic():
    oriImg= request.files['oriImg'] #原始图片对象
    wmImg = request.files['wmImg'] #水印图片对象
    saveImg(oriImg)
    saveImg(wmImg)
    embedImg = embed(oriImg.filename, wmImg.filename) #嵌入后的文件名
    print(f"embed {embedImg} successfully")
    return {'filename': embedImg, 'url': base_url + embedImg}

@app.route('/extract', methods=['POST'])
def extractPic():
    oriImg= request.files['oriImg'] #欲从中提取水印的图片
    wmWidth = int(request.form['wmWidth']) #水印宽度
    wmHeight = int(request.form['wmHeight']) #水印高度
    saveImg(oriImg)
    type = request.form['type']
    if (type == 'none'): #没有攻击
        middleImg = oriImg.filename
    elif (type == 'rot'): #旋转攻击
        angle = int(request.form['angle'])
        middleImg = rot_att(oriImg.filename, -angle) #转回去后的中间产物
        print(f"rotate back to {middleImg} successfullly")
    elif (type == 'resize'): #缩放攻击
        oriWidth = int(request.form['oriWidth'])
        oriHeight = int(request.form['oriHeight'])
        middleImg = resize_att(oriImg.filename, (oriWidth, oriHeight)) #缩放回去
        print(f"resize back to {middleImg} successfullly")
    elif (type in ["cutWidth", "cutHeight"]): #裁剪攻击
        oriWidth = int(request.form['oriWidth'])
        oriHeight = int(request.form['oriHeight'])
        middleImg = anti_cut_att(oriImg.filename, (oriHeight, oriWidth))
        print(f"anti cut to {middleImg} successfullly")
    extrImg = extract(middleImg, wmWidth, wmHeight)
    print(f"extract {extrImg} successfully")
    return {'filename': extrImg, 'url': base_url + extrImg}

@app.route('/attack', methods=['POST'])
def attackPic():
    attack_type = request.form['type'] #得到攻击类型
    if attack_type == "rot":
        oriImg = request.files['oriImg']
        angle = int(request.form['angle'])
        saveImg(oriImg)
        rstImg = rot_att(oriImg.filename, angle) #旋转后的图片名称
        return {'filename': rstImg, 'url': base_url + rstImg}
    elif attack_type == "resize":
        oriImg = request.files['oriImg']
        width = int(request.form['width']) #水印宽度
        height = int(request.form['height']) #水印高度
        saveImg(oriImg)
        rstImg = resize_att(oriImg.filename, (width, height))
        return {'filename': rstImg, 'url': base_url + rstImg}
    elif attack_type == "cutWidth":
        oriImg = request.files['oriImg']
        ratio = double(request.form['ratio']) #裁切比例
        saveImg(oriImg)
        rstImg = cut_att_width(oriImg.filename, ratio)
        return {'filename': rstImg, 'url': base_url + rstImg}
    elif attack_type == "cutHeight":
        oriImg = request.files['oriImg']
        ratio = double(request.form['ratio']) #裁切比例
        saveImg(oriImg)
        rstImg = cut_att_height(oriImg.filename, ratio)
        return {'filename': rstImg, 'url': base_url + rstImg}

app.run('0.0.0.0', debug=True)
