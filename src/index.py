
from flask import Flask, render_template, request, url_for, jsonify
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
import logging
import uuid
import sys
from .receipt_recognition import get_items


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:asdf1234@HACKGT8db/HACKGT8'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4)
    store_name = db.Column(db.String(100))
    date = db.Column(db.DateTime)
    price = db.Column(db.Float)
    count = db.Column(db.Integer)
    item_name = db.Column(db.String(100))
    catagory = db.Column(db.String(100))

    def __init__(self, user_id, item_name, price, catagory):
        self.user_id = user_id
        self.item_name = item_name
        self.price = price
        self.catagory = catagory


@app.route('/')
def index():
  # Create item for test usage
  # testItem = Item('16fd2706-8baf-433b-82eb-8c7fada847da', 'item_name', 10, 'catagory')
  # db.session.add(testItem)
  # db.session.commit()
  items = Item.query.all()
  app.logger.info('%s items: ', items)
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
    db.create_all()
    db.session.commit()
    app.run()


app.run(debug = True)
