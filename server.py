from flask import Flask, request, send_from_directory, jsonify
import json
import numpy as np;

app = Flask(__name__, static_url_path='')


the_seismic = [1, 1, 0, 0, -1, -1, 0, 0, 1, 1];
# dummy stuff
def dummySeismicGenerator(r):
  return {'seismic': [1,2,3], 'min': -10, 'max': 10}

@app.route('/api/model/<levelid>')
def get_model(levelid):
  filename = 'model' + str(levelid) + '.txt';
  return app.send_static_file('data/' + filename)

@app.route('/api/forward', methods=['POST'])
def get_forward_model():
  r = request.json['usermodel']
  tr = dummySeismicGenerator(r)
  return jsonify(tr)

@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)

if __name__ == "__main__":
    app.run(debug=True)
