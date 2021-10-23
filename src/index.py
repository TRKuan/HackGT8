from flask import Flask, render_template, request, url_for, jsonify
import sys
app = Flask(__name__)

from .receipt_recognition import get_items

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/user_id/upload_images', methods = ['POST'])
def process_images():
  files = request.files.getlist("file[]")
  for file in files:
    #print (file,sys.stderr)
    fs = file.read()
    res = get_items(fs)
    #print (res,sys.stderr)
  return "OK"

@app.route('/user_id/search/<search_str>', methods = ['GET'])
def get_list(search_str):
  sample_list = [('Publix','2020/11/13','chicken','12'),('SQ5','2020/11/11','chicken','15')]
  return jsonify({'data': sample_list})

#  return 
if __name__ == '__main__':
    app.run()
