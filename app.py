from flask import Flask, request

app = Flask(__name__)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        oriImg= request.files['oriImg'] #原始图片
        wmImg = request.files['wmImg'] #水印图片
        oriImg.save("pic/" + oriImg.filename) #存储
        wmImg.save("pic/" + wmImg.filename)
        print(f"save origin {oriImg.filename} succesfully")
        print(f"save wm {wmImg.filename} succesfully")
    return "hello world"

app.run(debug=True)
