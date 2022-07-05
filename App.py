import base64
import os
from flask import Flask,  request,render_template,jsonify,send_file
from sqlalchemy import false
from werkzeug.utils import secure_filename
from brisque import BRISQUE

from time import time

app = Flask(__name__)

if not os.path.exists("uploads"):
    os.makedirs("uploads")

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_init():
		return jsonify({'message' : ' script ran successfully '})





@app.route('/upload', methods=['GET','POST'])
def upload_submit():

	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file and allowed_file(file.filename):
		
		filename = secure_filename(str(time())+file.filename )
		file.save(os.path.join("uploads", filename))
		
		
		# quality detection 
		
		obj = BRISQUE("uploads/"+filename, url=False)
		quality  = obj.score()
		# percentage quality -->150 to 120  = 62 to 52 
		percentage = 100-((quality*100)/120)
		percentageInt = int(percentage)


		resp = jsonify({"quality": percentageInt})
		resp.status_code = 201
		# os.remove("uploads/"+filename)
		return resp
if __name__ == '__main__':
    app.run(debug=false)