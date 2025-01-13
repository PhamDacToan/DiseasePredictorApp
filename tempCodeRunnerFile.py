from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Cấu hình thư mục tải lên file
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Chỉ cho phép các định dạng file hình ảnh
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
@app.route('/')
def index():
    return render_template('layout.html')
# Hàm kiểm tra định dạng file
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/model1", methods=["GET", "POST"])
def model1():
    if request.method == "POST":
        # Kiểm tra xem có file hình ảnh trong request không
        if 'image' not in request.files:
            return redirect(request.url)
        
        file = request.files['image']
        
        # Kiểm tra xem file có hợp lệ không
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            # Lưu file vào thư mục uploads
            file.save(filename)
            return render_template("model1.html", filename=file.filename)
    
    return render_template("model1.html")

@app.route("/model2", methods=["GET", "POST"])
def model2():
    if request.method == "POST":
        if 'image' not in request.files:
            return redirect(request.url)
        
        file = request.files['image']
        
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            return render_template("model2.html", filename=file.filename)
    
    return render_template("model2.html")

@app.route("/model3", methods=["GET", "POST"])
def model3():
    if request.method == "POST":
        if 'image' not in request.files:
            return redirect(request.url)
        
        file = request.files['image']
        
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            return render_template("model3.html", filename=file.filename)
    
    return render_template("model3.html")

if __name__ == "__main__":
    app.run(debug=True)
