from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
import cv2


def videoconvert(inp):
    capture = cv2.VideoCapture(inp)
    inp_ext = inp.split(".")
    fpsin = capture.get(cv2.CAP_PROP_FPS)
    count = 0
    success = 1
    while success:
        success, image = capture.read()
        if (success == False and image == None):
            pass
        else:
            cv2.imwrite("zzimg%d.jpg" % count, image)
            count += 1
    outfile = inp_ext[0] + '_output.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    fpsout = fpsin
    img = cv2.imread("zzimg0.jpg")
    height, width, layers = img.shape
    size = (width, height)
    out = cv2.VideoWriter(outfile, fourcc, fpsout, size, 0)
    for i in range(count):
        img = cv2.imread("zzimg%d.jpg" % i, 0)
        out.write(img)
    print("Video Converted to Grayscale, Please check the folder for the output file: ", outfile)
    out.release()
    capture.release()
    cv2.destroyAllWindows()
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


if __name__ == '__main__':
    app.debug = True
    app.run()