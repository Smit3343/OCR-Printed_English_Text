from flask import Flask, make_response , render_template , request , flash , redirect, send_file, send_from_directory
from werkzeug.utils import secure_filename 
from processing import extractText
import os
from docx import Document

UPLOAD_FOLDER = 'D:/Semaster6/SDP/Project/static/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],os.path.join('img',filename)))
            txt = extractText(filename)
            # resp = make_response()
            # resp.set_cookie('Text', txt)
            return render_template('index.html', txt=txt , filename = filename)
    else:
        return render_template('index.html')


@app.route('/word', methods=['GET', 'POST'])
def word():
    if(request.method == 'POST'):
        document = Document()
        document.add_paragraph(request.form['txt'])
        document.save(UPLOAD_FOLDER + 'word/Download.docx')
        return send_from_directory(path = UPLOAD_FOLDER + 'word/Download.docx' ,  directory=UPLOAD_FOLDER + 'word', filename='Download.docx') 
    return redirect('/')


if __name__ == "__main__":
    app.run(debug = True)