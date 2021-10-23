from flask import Flask, render_template, request
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
  pass

#  return 
if __name__ == '__main__':
    app.run()
