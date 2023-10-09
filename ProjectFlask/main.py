from flask import Flask,render_template, request,flash,redirect, send_file
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','webp'}

app = Flask(__name__)
app.secret_key = 'dd hh'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def  processImage(filename, operation,file):
    print(f"The operation is {operation} and filename is {filename}")
    img=cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imageProcessed=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            newfilename=f"static/{filename}"
            cv2.imwrite(newfilename,imageProcessed)
            return newfilename

        case "cwebp":
            newfilename=f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newfilename,img)
            return newfilename
        case "cjpg":
            newfilename=f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newfilename,img)
            return newfilename
        case "cpng":
            newfilename=f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newfilename,img)
            return newfilename
        case "cjpeg":
            newfilename=f"static/{filename.split('.')[0]}.jpeg"
            cv2.imwrite(newfilename,img)
            return newfilename
        case "cgif":
           # imageProcessed=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            newfilename=f"static/{filename.split('.')[0]}.gif"
            cv2.imwrite(newfilename,img)
            return newfilename  
      
pass


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route('/button_click', methods=['POST'])
def button_click():
    # Perform any necessary actions here
    return render_template('login.html')
@app.route('/submit_form', methods=['POST'])
def submit_form():
    # Perform any necessary actions here
    return render_template('signup.html')

@app.route("/edit",methods=['GET', 'POST'])
def edit():
   if request.method == 'POST':
        # check if the post request has the file part
        operation=request.form.get("operation")
        #image_file = request.files
        if 'file' not in request.files:
            flash('No file part')
            return "Error!"
        file=request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "Error! no selected file."
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new=processImage(filename,operation,file)
            flash( f"Your image has been processed and available <a href='/{new}' target='_blank' >here</a>")
            return render_template("index.html")

            

   return render_template("index.html")

app.run(debug=True,port=5001)

