import numpy as np
import flask
import pickle
from flask import Flask, request, render_template

#create instance of Flask
app = Flask(__name__, template_folder='templates')

@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')

#function to predict the output
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 8)
    loaded_model = pickle.load(open("model.pkl", "rb"))
    result = loaded_model.predict(to_predict)
    return result[0]

#function to get the input from the user
@app.route('/result', methods = ['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(int, to_predict_list))
        result = ValuePredictor(to_predict_list)
        if int(result) == 0:
            prediction = 'Cluster 0'
        elif int(result) == 1:
            prediction = 'Cluster 1'
        elif int(result) == 2:
            prediction = 'Cluster 2'
        elif int(result) == 3:
            prediction = 'Cluster 3'
        elif int(result) == 4:
            prediction = 'Cluster 4'
        return render_template("result.html", prediction = prediction)

if __name__ == "__main__":
    app.run(debug=False)