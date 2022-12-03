from flask import Flask, request , jsonify, render_template
from flask_cors import CORS, cross_origin

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

CORS(app)
cors = CORS(app, resources={r"*": {"origins": "*"}})


data = pd.read_csv("./tayara_cars.csv")


features =["location","km","marque","price","carburant","boite","cylindre"]

for feature in features:
  data[feature] = data[feature].fillna('')

def combine_features(row):
  try:
    return row['location']+" "+str(row['km'])+" "+row['marque']+" "+str(row['price'])+" "+row['carburant']+" "+row['boite']+" "+row['cylindre']
  except:
     print("Error:  " + row) 
     
data["combine_features"] = data.apply(combine_features, axis=1)

CV = CountVectorizer()
count_matrix = CV.fit_transform(data["combine_features"])
cosine_sim = cosine_similarity(count_matrix)

def get_car_from_index(index):
  return data[data.index == index]["combine_features"].values[0]


def get_index_from_car(combine_features):
  return data[data.combine_features == combine_features ]["Unnamed: 0"].values[0]



@app.route('/', methods=['GET','POST'])
@cross_origin()
def index():
    request_type_str = request.method
    if request_type_str == 'GET' :
      return render_template('car.html',prediction={})

    if request_type_str == 'POST' :
      location = request.form['location']
      marque = request.form['marque']
      cylindre = request.form['cylindre']
      boite = request.form['boite']
      carburant = request.form['carburant']
      price = request.form['price']
      km = request.form['km']
      car_user_like = location+" "+ km +" " + marque +" "+ price +" "+ carburant +" "+ boite +" "+cylindre


      # car_user_like ="Tunis, Autres villes 29000.0 Volkswagen 45000.0 Essence Nouveau Manuelle"
      car_index = get_index_from_car(car_user_like)
      similar_cars = list(enumerate(cosine_sim[car_index]))
      sorted_similar_cars = sorted(similar_cars , key=lambda x:x[1], reverse=True)

      d={}
      i =0
      for car in sorted_similar_cars :
        x=get_car_from_index(car[0])

        l= x.split()
        car_d={}
        car_d["cylindre"]=l.pop()
        car_d["boite"]=l.pop()
        car_d["carburant"]=l.pop()
        car_d["price"]=l.pop()
        car_d["marque"]=l.pop()
        car_d["km"]=l.pop()

        ch = ""
        for loc in l:
          ch+= " " + loc
        car_d["location"]=ch

        d[i]= car_d
        i += 1
        if i> 9 :
          break
      
      return render_template('car.html',prediction=d)



if __name__ == "__main__":
    app.run(debug=True)