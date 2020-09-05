from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
from cv2 import VideoCapture, CAP_PROP_FPS, imwrite, VideoWriter_fourcc, imread, VideoWriter


def videoconvert(inp):
    capture = VideoCapture(inp)
    inp_ext = inp.split(".")
    fpsin = capture.get(CAP_PROP_FPS)
    count = 0
    success = 1
    while success:
        success, image = capture.read()
        if (success == False and image == None):
            pass
        else:
            imwrite("zzimg%d.jpg" % count, image)
            count += 1
    outfile = inp_ext[0] + '_output.mp4'
    fourcc = VideoWriter_fourcc(*'DIVX')
    fpsout = fpsin
    img = imread("zzimg0.jpg")
    height, width, layers = img.shape
    size = (width, height)
    out = VideoWriter(outfile, fourcc, fpsout, size, 0)
    for i in range(count):
        img = imread("zzimg%d.jpg" % i, 0)
        out.write(img)
    print("Video Converted to Grayscale, Please check the folder for the output file: ", outfile)
    out.release()
    capture.release()

    return outfile


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'wav', 'avi'}

app = Flask(__name__)
app.config['UPLOAD_PATH'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():

    if request.method == 'POST':
        myemail = request.form['email']
        f = request.files['file']
        f.save(secure_filename(f.filename))
        out_file = videoconvert(f.filename)
        return render_template('success.html', message=out_file)
