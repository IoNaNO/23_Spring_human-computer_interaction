#!flask/bin/python
################################################################################################################################
#------------------------------------------------------------------------------------------------------------------------------                                                                                                                             
# This file implements the REST layer. It uses flask micro framework for server implementation. Calls from front end reaches 
# here as json and being branched out to each projects. Basic level of validation is also being done in this file. #                                                                                                                                  	       
#-------------------------------------------------------------------------------------------------------------------------------                                                                                                                              
################################################################################################################################
from flask import Flask, jsonify, abort, request, make_response, url_for,redirect, render_template, send_file
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import os
import shutil 
import numpy as np
from search import recommend
import tarfile
from datetime import datetime
from scipy import ndimage
from flask_cors import CORS
#from scipy.misc import imsave

UPLOAD_FOLDER = 'uploads'
FAVORITE_FOLDER='static/favorite'
TAGS_FOLDER='database/tags'
RESULT_FOLDER='static/result'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
from tensorflow.python.platform import gfile
app = Flask(__name__, static_url_path = "")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
auth = HTTPBasicAuth()
CORS(app, resources=r'/*')

#==============================================================================================================================
#                                                                                                                              
#    Loading the extracted feature vectors for image retrieval                                                                 
#                                                                          						        
#                                                                                                                              
#==============================================================================================================================
extracted_features=np.zeros((2955,2048),dtype=np.float32)
with open('saved_features_recom.txt') as f:
    		for i,line in enumerate(f):
        		extracted_features[i,:]=line.split()
print("loaded extracted_features") 

# Check image tag
def check_number_in_file(file_path, number):
    with open(file_path, "r") as f:
        for line in f:
            if line.strip() == number:
                return True
    return False

#==============================================================================================================================
#                                                                                                                              
#  This function is used to do the image search/image retrieval
#                                                                                                                              
#==============================================================================================================================
@app.route('/imgUpload', methods=['GET', 'POST'])
#def allowed_file(filename):
#    return '.' in filename and \
#           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_img():
    print("image upload")
    result = 'static/result'
    if not gfile.Exists(result):
          os.mkdir(result)
    shutil.rmtree(result)
 
    if request.method == 'POST' or request.method == 'GET':
        print(request.method)
        print(request.files)
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
            # return jsonify({'msg':"Wrong FormData"})
        file = request.files['file']
        print(file.filename)
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
           
            print('No selected file')
            return redirect(request.url)
            # return jsonify({'msg':"Wrong FormData"})
        if file:# and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            inputloc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            recommend(inputloc, extracted_features)
            os.remove(inputloc)
            image_path = ""
            result_images =[os.path.join(image_path, file) for file in os.listdir(result)
                              if not file.startswith('.')]
            # result_images=image_list
            # images = {
			# 'image0':image_list[0],
            # 'image1':image_list[1],	
			# 'image2':image_list[2],	
			# 'image3':image_list[3],	
			# 'image4':image_list[4],	
			# 'image5':image_list[5],	
			# 'image6':image_list[6],	
			# 'image7':image_list[7],	
			# 'image8':image_list[8]
		    #   }				
            return jsonify(result_images)

# Return the raw image
@app.route('/image',methods=['GET'])
def get_image():
    if request.method == 'GET':
        image_path = request.args['path']
        print(image_path)
        return send_file(image_path, mimetype='image/jpeg')
    return jsonify({})

# Add image to favorites
@app.route('/favorite',methods=['POST'])
def add_favorite():
    image_name=request.args['path']
    print(image_name)
    if image_name in os.listdir(FAVORITE_FOLDER):
        return jsonify({'code':400,'msg':"Image already in favorites"})
    image_path_n=FAVORITE_FOLDER+"/"+image_name
    image_path_o="static/result/"+image_name
    shutil.copy(image_path_o,image_path_n)
    return jsonify({'code':200,'msg':"Image added to favorites"})

# Get all favorite images
@app.route('/favorite',methods=['GET'])
def get_favorite():
    image_path = ''
    image_list =[os.path.join(image_path, file) for file in os.listdir(FAVORITE_FOLDER)
                              if not file.startswith('.')]
    return jsonify(image_list)

# Remove image from favorites
@app.route('/favorite',methods=['DELETE'])
def remove_favorite():
    image_name=request.args['path']
    print(image_name)
    if image_name not in os.listdir(FAVORITE_FOLDER):
        return jsonify({'code':400,'msg':"Image not in favorites"})
    image_path=FAVORITE_FOLDER+"/"+image_name
    os.remove(image_path)
    return jsonify({'code':200,'msg':"Image removed from favorites"})

# Request image tags
@app.route('/tag',methods=['GET'])
def get_tags():
    tags_list =[file.split('.')[0] for file in os.listdir(TAGS_FOLDER)
                              if not file.startswith('.') or file=='README.txt']
    return jsonify(tags_list)

# Select image by tag
@app.route('/tag',methods=['POST'])
def select_image_by_tag():
    tag=request.args['tag']
    print(tag)
    result_images=[file for file in os.listdir(RESULT_FOLDER)
                              if not file.startswith('.')]
    if tag=="all":
        return jsonify(result_images)
    tag_path=TAGS_FOLDER+"/"+tag+".txt"
    selected_images=[]
    for image_name in result_images:
        image_no=image_name.split('.')[0][2:]
        # print(image_no)
        if check_number_in_file(tag_path, image_no):
            selected_images.append(image_name)
    return jsonify(selected_images)
#==============================================================================================================================
#                                                                                                                              
#                                           Main function                                                        	            #						     									       
#  				                                                                                                
#==============================================================================================================================
@app.route("/")
def main():
    
    return render_template("main.html")   
if __name__ == '__main__':
    app.run(debug = True, host= '0.0.0.0')
