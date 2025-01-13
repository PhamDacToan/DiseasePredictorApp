from flask import Flask, render_template, request, redirect, url_for
import os
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import load_model
import numpy as np

# Load mô hình đã huấn luyện
resnet_model1 = load_model('models/best_model_resnet50.keras')
brain_model2 = load_model('models/brain_predict_model.h5')
app = Flask(__name__)

# Cấu hình thư mục tải lên file
UPLOAD_FOLDER = 'static/uploads'
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
    prediction = None
    advice = None
    filename = None

    if request.method == "POST":
        # Kiểm tra xem có file hình ảnh trong request không
        if 'image' not in request.files:
            return redirect(request.url)

        file = request.files['image']

        # Kiểm tra xem file có hợp lệ không
        if file and allowed_file(file.filename):
            # Lưu file vào thư mục uploads
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Tiền xử lý ảnh để đưa vào mô hình
            img = load_img(filepath, target_size=(224, 224))  # Resize ảnh về 224x224
            img_array = img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)  # Thêm batch dimension
            img_array = img_array / 255.0  # Áp dụng preprocess của ResNet50

            # Thực hiện dự đoán
            preds = resnet_model1.predict(img_array)
            class_idx = np.argmax(preds)  # Lấy nhãn dự đoán cao nhất

            # Dựa vào class_idx để đưa ra kết quả và gợi ý
            if class_idx == 0:
                prediction = "Bình thường"
                advice = "Chúc mừng bạn không bị bệnh"
            elif class_idx == 1:
                prediction = "Viêm phổi"
                advice = "Nếu kết quả dự đoán cho thấy bạn có thể bị viêm phổi, lời khuyên là bạn nên đến bác sĩ để được thăm khám và thực hiện các xét nghiệm cần thiết, như chụp X-quang hoặc xét nghiệm máu, để xác định nguyên nhân gây bệnh. Viêm phổi có thể do vi khuẩn, virus hoặc nấm, và việc xác định đúng tác nhân sẽ giúp bác sĩ chỉ định phương pháp điều trị phù hợp, như kháng sinh hoặc thuốc kháng virus. Ngoài ra, bạn cần nghỉ ngơi đầy đủ, uống nhiều nước và tuân thủ đúng phác đồ điều trị để nhanh chóng phục hồi. Trong thời gian điều trị, nếu có bất kỳ dấu hiệu nặng thêm nào, bạn nên thông báo ngay cho bác sĩ để được can thiệp kịp thời."
            else:
                prediction = "Bệnh Lao"
                advice = "Nếu kết quả dự đoán cho thấy bạn có thể bị bệnh lao, lời khuyên đầu tiên là bạn nên đến bác sĩ để thực hiện các xét nghiệm bổ sung, như chụp X-quang phổi hoặc xét nghiệm đờm, để xác nhận chẩn đoán. Bệnh lao có thể được điều trị hiệu quả nếu phát hiện sớm và tuân thủ đúng phác đồ điều trị. Bạn cần kiên trì uống thuốc theo hướng dẫn của bác sĩ để ngăn ngừa vi khuẩn lao phát triển và lây lan. Ngoài ra, việc giữ gìn vệ sinh cá nhân, đeo khẩu trang và hạn chế tiếp xúc với người khác trong giai đoạn điều trị là rất quan trọng để bảo vệ sức khỏe cộng đồng."

            # Render lại template với kết quả
            return render_template(
                "model1.html",
                filename=filename,
                prediction=prediction,
                advice=advice,
            )

    return render_template("model1.html", filename=filename, prediction=prediction, advice=advice)

@app.route("/model2", methods=["GET", "POST"])
def model2():
    prediction = None
    advice = None
    filename = None

    if request.method == "POST":
        # Kiểm tra xem có file hình ảnh trong request không
        if 'image' not in request.files:
            return redirect(request.url)

        file = request.files['image']

        # Kiểm tra xem file có hợp lệ không
        if file and allowed_file(file.filename):
            # Lưu file vào thư mục uploads
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Tiền xử lý ảnh để đưa vào mô hình
            img = load_img(filepath, target_size=(299, 299))  # Resize ảnh về 224x224
            img_array = img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)  # Thêm batch dimension
            img_array = img_array / 255.0  # Áp dụng preprocess của ResNet50

            # Thực hiện dự đoán
            preds = brain_model2.predict(img_array)
            class_idx = np.argmax(preds)  # Lấy nhãn dự đoán cao nhất

            # Dựa vào class_idx để đưa ra kết quả và gợi ý
            if class_idx == 0:
                prediction = "Ung thư tế bào não"
                advice = "Nếu kết quả dự đoán cho thấy bạn có thể mắc ung thư tế bào não, lời khuyên là bạn cần đi khám và thực hiện các xét nghiệm chuyên sâu ngay lập tức. Chẩn đoán ung thư tế bào não yêu cầu các phương pháp như chụp MRI, CT scan và sinh thiết để xác định chính xác loại ung thư, mức độ lan rộng và giai đoạn bệnh. Việc điều trị ung thư tế bào não có thể bao gồm phẫu thuật, xạ trị, hóa trị hoặc các phương pháp điều trị mới như liệu pháp nhắm mục tiêu. Điều quan trọng là bạn cần hợp tác chặt chẽ với bác sĩ để lựa chọn phương pháp điều trị tối ưu, đồng thời duy trì chế độ dinh dưỡng hợp lý và tinh thần lạc quan để hỗ trợ quá trình điều trị. Hãy nhớ rằng, phát hiện sớm và điều trị kịp thời sẽ tăng cơ hội điều trị thành công."
            elif class_idx == 1:
                prediction = "Khối u màng não"
                advice = "Nếu kết quả dự đoán cho thấy bạn có thể bị khối u màng não, điều quan trọng là bạn nên đi khám bác sĩ chuyên khoa thần kinh hoặc bác sĩ ung bướu để xác nhận chẩn đoán. Khối u màng não thường phát triển chậm và có thể không gây ra triệu chứng rõ rệt trong giai đoạn đầu. Tuy nhiên, để có kế hoạch điều trị hiệu quả, bạn sẽ cần thực hiện các xét nghiệm như chụp MRI, CT scan hoặc sinh thiết. Phương pháp điều trị khối u màng não có thể bao gồm phẫu thuật để loại bỏ u, xạ trị hoặc hóa trị, tùy thuộc vào vị trí, kích thước và tính chất của khối u. Việc theo dõi thường xuyên và hợp tác với đội ngũ y tế trong suốt quá trình điều trị là rất quan trọng. Nếu khối u được phát hiện sớm, cơ hội điều trị thành công và giảm thiểu biến chứng là rất cao."
            elif class_idx == 2:
                prediction = "Bình thường"
                advice = "Chúc mừng bạn"
            else:
                prediction = "Khối u tuyến yên"
                acvice = "Nếu kết quả dự đoán cho thấy bạn có thể bị khối u tuyến yên, việc thăm khám và chẩn đoán chính xác từ bác sĩ chuyên khoa nội tiết hoặc bác sĩ ung bướu là rất quan trọng. Khối u tuyến yên có thể ảnh hưởng đến sự sản xuất hormone của tuyến yên, dẫn đến các vấn đề về hormone trong cơ thể như tăng trưởng không bình thường, vấn đề sinh sản, hoặc sự thay đổi trong chuyển hóa. Các xét nghiệm chẩn đoán như chụp MRI, xét nghiệm hormone trong máu, hoặc sinh thiết có thể giúp xác định chính xác tình trạng của bạn. Điều trị khối u tuyến yên có thể bao gồm phẫu thuật để loại bỏ u, xạ trị hoặc dùng thuốc để kiểm soát sản xuất hormone. Phương pháp điều trị cụ thể sẽ phụ thuộc vào loại khối u (lành tính hay ác tính), kích thước và vị trí của khối u. Theo dõi và tái khám định kỳ là rất quan trọng để đảm bảo tình trạng không tái phát và để điều chỉnh phương pháp điều trị nếu cần thiết. Khi được phát hiện và điều trị kịp thời, tỷ lệ thành công trong việc kiểm soát khối u tuyến yên là khá cao."

            # Render lại template với kết quả
            return render_template(
                "model2.html",
                filename=filename,
                prediction=prediction,
                advice=advice,
            )

    return render_template("model2.html", filename=filename, prediction=prediction, advice=advice)


if __name__ == "__main__":
    app.run(debug=True)
