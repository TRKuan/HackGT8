from flask import Flask, render_template, request, url_for, jsonify
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
import logging
import uuid
import sys
from datetime import datetime
from .receipt_recognition import get_items
from .mapping import item_map

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
    def __str__(self):
      return '(' + self.user_name + ', ' + str(self.price) + ')'

db.create_all()
db.session.commit()

@app.route('/')
def index():
  # Create item for test usage
  # testItem = Item('16fd2706-8baf-433b-82eb-8c7fada847da', 'item_name', 10, 'catagory')
  # db.session.add(testItem)
  # db.session.commit()
  items = Item.query.all()
  app.logger.info('%s items: ', items)
  return render_template('index.html')

@app.route('/drop')
def drop_table():
  Item.__table__.drop()
@app.route('/user_id/upload_images', methods = ['POST'])
def process_images():
  files = request.files.getlist("file[]")
  app.logger.info(files)
  for file in files:
    #print (file,sys.stderr)
    fs = file.read()
    try_round = 0
    while try_round < 5:
      try_round+=1
      try:
        res = get_items(fs)
        break
      except Exception as ex:
        app.logger.info(ex)
    app.logger.info(res)
    for item in res:
      item_catagory = item['item_name'].lower()
      if item_catagory in item_map:
        item_catagory = item_map[item_catagory]
      new_item = Item('16fd2706-8baf-433b-82eb-8c7fada847da', item['item_name'].lower(), item['price'], item_catagory)
      new_item.date = item['date'] if 'date' in item else None
      new_item.count = int(item['count']) if 'count' in item and int(item['count']) > 0 else 1
      new_item.store_name = item['store_name'] if 'store_name' in item else None
      db.session.add(new_item)
      db.session.commit()
    items = Item.query.all()
    x = [(i.item_name, i.price, i.catagory) for i in items]
    app.logger.info('%s items, %s ', len(x), file)
    #
    #print (res,sys.stderr)
  return "OK"

@app.route('/user_id/search/<search_str>', methods = ['GET'])
def get_list(search_str):
  app.logger.info(search_str)
  items = Item.query.filter_by(catagory = search_str).all()
  app.logger.info(items)
  #sample_list = [('Publix','2020/11/13','chicken','12','1'),('SQ5','2020/11/11','chicken','15','2')]
  sample_list = [(i.store_name, i.date.strftime("%m-%d-%Y") if i.date else None, i.item_name, "%.2f" % i.price, i.count) for i in items]
  return jsonify({'data': sample_list})
  

#  return 
if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    app.run()


app.run(debug = True)
