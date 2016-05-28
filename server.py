from flask import Flask, request, send_from_directory, jsonify
import numpy as np;

app = Flask(__name__, static_url_path='')

# dummy stuff
the_model = [1, 1, 0, 0, -1, -1, 0, 0, 1, 1];
the_seismic = the_model;

@app.route('/api/model/<levelid>')
def get_model(levelid):
  filename = 'Model' + str(levelid) + '.txt';
  return app.send_static_file('Data/' + filename);
 
@app.route('/api/seismic/<levelid>')
def get_seismic(levelid):
  return jsonify(model=the_model);

@app.route('/api/forward')
def get_forward_model():
  pass

@app.route('/')
def root():
    return app.send_static_file('index.html');

@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)
    
if __name__ == "__main__":
    app.run(debug=True)