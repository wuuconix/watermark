from flask import Flask, request
from watermark import embed, extract

app = Flask(__name__)

@app.route('/embed', methods=['GET', 'POST'])
def embedPic():
    if request.method == 'POST':
        oriImg= request.files['oriImg'] #原始图片对象
        wmImg = request.files['wmImg'] #水印图片对象
        oriImg.save("pic/" + oriImg.filename) #存储
        wmImg.save("pic/" + wmImg.filename)
        print(f"save origin {oriImg.filename} succesfully")
        print(f"save wm {wmImg.filename} succesfully")
        embedImg = embed(oriImg.filename, wmImg.filename) #嵌入后的文件名
        print(f"embed {embedImg} successfully")
        url = f"https://watermark.wuuconix.link/pic/{embedImg}"
    return {'filename': embedImg, 'url': url}

@app.route('/extract', methods=['GET', 'POST'])
def extractPic():
    if request.method == 'POST':
        syncImg= request.files['syncImg'] #sync，即有水印的图像
        width = int(request.form['width']) #水印宽度
        height = int(request.form['height']) #水印高度
        syncImg.save("pic/" + syncImg.filename) #存储
        print(f"save sync {syncImg.filename} succesfully")
        extrImg = extract(syncImg.filename, width, height) #提取得到的水印名
        print(f"extract {extrImg} successfully")
        url = f"https://watermark.wuuconix.link/pic/{extrImg}"
    return {'filename': extrImg, 'url': url}

app.run(debug=True)
