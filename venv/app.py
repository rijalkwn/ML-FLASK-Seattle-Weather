import numpy as np
import os
import flask
import pickle
from flask import Flask, request, render_template, redirect, url_for

#create instance of Flask
app = Flask(__name__, template_folder='templates')

picFolder = os.path.join('static','img')
print(picFolder)
app.config['UPLOAD_FOLDER'] = picFolder

@app.route('/')
@app.route('/index')
def index():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'images.png')
    return flask.render_template('index.html', user_image = pic1)


#function to predict the output
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 2)
    loaded_model = pickle.load(
        open("./model/model.pkl", "rb"))
    result = loaded_model.predict(to_predict)
    return result[0]

#function to get the input from the user
@app.route('/result', methods = ['POST'])
def result():
    if request.method == 'POST':
        precipation = request.form['precipitation']
        temp_max = request.form['temp_max']
        to_predict_list = list(map(float, [precipation, temp_max]))
        result = ValuePredictor(to_predict_list)
        if int(result) == 0:
            prediction = 'low precipitation and low temperature'
        elif int(result) == 1:
            prediction = 'low precipitation and high temperature'
        elif int(result) == 2:
            prediction = 'high precipitation and normal temperature'
        return render_template("result.html", prediction = prediction)

if __name__ == "__main__":
    app.run(debug=True)