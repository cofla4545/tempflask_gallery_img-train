from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import base64
import image

app = Flask(__name__)

# 파일 업로드를 위한 디렉토리 설정
TRAIN_FOLDER = './static/train/'
INPUT_FOLDER = './static/input/'
OUTPUT_FOLDER = './static/output/'
app.config['TRAIN_FOLDER'] = TRAIN_FOLDER
app.config['INPUT_FOLDER'] = INPUT_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/train')
def train():
    return render_template('train.html')

@app.route('/train_camera')
def train_camera():
    return render_template('train_camera.html')

@app.route('/train_gallery')
def train_gallery():
    return render_template('train_gallery.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/gallery_convert')
def gallery_convert():
    return render_template('gallery_convert.html')

# 새로운 save_image 라우트 추가
@app.route('/save_image', methods=['POST'])
def save_image():
    image_data = request.form['image']
    # 데이터 URL에서 이미지 데이터만 추출
    image_data = image_data.replace('data:image/png;base64,', '')
    image_data = base64.b64decode(image_data)

    # 이미지 저장 경로 설정
    image_dir = app.config['TRAIN_FOLDER']
    image_path = os.path.join(image_dir, 'train_image.jpg')

    # 폴더가 존재하지 않으면 생성
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    # 이미지 저장
    with open(image_path, 'wb') as f:
        f.write(image_data)

    return redirect(url_for('index'))  # 이미지 저장 후 index.html로 리디렉션

# 이미지 변환 라우트 추가
@app.route('/convert_image', methods=['POST'])
def convert_image():
    image_data = request.files['image']
    image_path = os.path.join(app.config['INPUT_FOLDER'], 'input_image.jpg')
    image_data.save(image_path)

    # 이미지 변환 코드 실행
    try:
        learning_image_path = os.path.join(app.config['TRAIN_FOLDER'], 'train_image.jpg')
        output_image_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output_image.jpg')
        image.process_images(learning_image_path, image_path, output_image_path)
    except Exception as e:
        print(f"Error occurred: {e}")
        return f"An error occurred while processing the image: {e}", 500

    return redirect(url_for('gallery_convert'))

@app.route('/output/<filename>')
def send_output(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
