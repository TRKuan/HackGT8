from flask import Flask, render_template
app = Flask(__name__)

from .receipt_recognition import get_items

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/user_id/image', methods = ['POST'])
def process_image():
  pass

@app.route('/user_id/search/<search_str>', methods = ['GET'])
def get_list(search_str):
  pass

#  return 
if __name__ == '__main__':
    app.run()
