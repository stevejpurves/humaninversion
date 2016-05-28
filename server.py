from flask import Flask, request, send_from_directory

app = Flask(__name__, static_url_path='')


@app.route('/api/model/:id')
def get_model():
  pass
 
@app.route('/api/seismic/:id')
def get_seismic():
  pass

@app.route('/api/forward/:id')
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
    app.run()