from flask import Flask, request , jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "hello yahya!"

@app.route('/api/testobj', methods=['GET' , 'POST'])
def testobj():
    request_type_str = request.method
    if request_type_str == 'GET' :
        return jsonify(data = "http://127.0.0.1:5000/static/obj/f9af1d798bdec6ae00547baf9a8c72722f254cd15eeba67eb1480e8a05ff2e71.obj"), 200
    if request_type_str == 'POST' :

        objFile = request.files['objfile']
        obj_path = "./static/obj/" + objFile.filename
        objFile.save(obj_path)


        return jsonify(data =obj_path), 201

@app.route('/api/3d_mobel' , methods=['GET' , 'POST'])
def man():
  request_type_str = request.method
  if request_type_str == 'GET' :
    return jsonify(data ="ttttttttt"), 200
    #return render_template('index.html' , imagePath="static/imageModel.svg")
  else :
    inputData = request.get_json()

    return jsonify( data = inputData['name']) , 200



if __name__ == "__main__":
    app.run(debug=True)