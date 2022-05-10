from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import os

#from __future__ import print_function
import fitz
from PIL import Image
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['IMAGE_UPLOADS'] = "C:/Users/gratt/PycharmProjects/FlaskVolt/templates"
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'secretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'


class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")

class NamerForm(FlaskForm):
    name = StringField("Whats your name")
    file = FileField("File")
    submit = SubmitField("Submit")

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/',methods=['POST', 'GET'])
def index():

    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/admin')
def fake_admin():
    return render_template('admin.html')

@app.route('/admin')
def fake_admin2():
    return render_template('admin.html')

@app.route('/sj',methods=['POST', 'GET'])
def sj():
    name = None
    form = NamerForm()
    file = UploadFileForm()
    if form.validate_on_submit():
        name = form.name.data
        filename = file.file
        form.name.data = ''

    return render_template('sj.html', form=form, name = name)

    #if request.method == "POST":
    #    print("request")
    #    if request.files:

    #        image = request.files['pdf']
    #        print(image)
    #        print("Creating a directory.")

    #        dir_name = "C:/Users/gratt/PycharmProjects/FlaskVolt/jpg-converted"
    #        os.chmod("C:/Users/gratt/PycharmProjects/FlaskVolt/", 0o777)
    #        image.save(dir_name)
    #        #image.save('C:/Users/gratt/PycharmProjects/FlaskVolt', image.filename)
    #        print("image saved")

    #        return redirect(request.url)


    pdf_to_jpg()
    #pdf_to_jpg()


def pdf_to_jpg():
    doc = fitz.open('C:/Users/gratt/Desktop/dhl.pdf')
    # doc = fitz.open('C:/Users/gratt/Desktop/leo.pdf')
    pages = doc.page_count

    if pages >= 3:
        print("Creating a directory.")
        dir_name = "jpg-converted"
        os.mkdir(f'C:/Users/gratt/Desktop/{dir_name}/')
    else:
        dir_name = ""

    for page in range(0, pages):
        page = doc.load_page(page)  # loads page number 'pno' of the document (0-based)
        print(page)
        pix = page.get_pixmap(dpi=300)
        pix.save(f"C:/Users/gratt/Desktop/{dir_name}/page-%i.png" % page.number)
        img = Image.open(f"C:/Users/gratt/Desktop/{dir_name}/page-%i.png" % page.number)
        img.save(f"C:/Users/gratt/Desktop/{dir_name}/page-%i.jpg" % page.number)
        os.remove(f"C:/Users/gratt/Desktop/{dir_name}/page-%i.png" % page.number)

    # TODO-- email all pages as attachment
    # TODO-- download as zip separate pages

if __name__ == "__main__":
    app.run(debug=True)