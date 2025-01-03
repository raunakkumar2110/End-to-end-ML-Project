from flask import Flask, render_template, request
import os
import numpy as np
import pandas as pd
from src.mlProject.pipeline.prediction import PredictionPipeline

app = Flask(__name__)  #initializing a flask app or object

@app.route('/',methods = ['GET'])
def homePage():
    return render_template("index.html")


@app.route('/train', methods = ['GET']) #route to train pipeline
def training():
    os.system("python main.py")
    return "Training Sucessful!"

@app.route('/predict', methods = ['POST','GET']) #route to show prediction in web UI
def index():
    if request.method == 'POST':
        try:
            # Print the length of the form data
            print("Length of Form Data:", len(request.form))
            
            # Print the entire form data to the console
            print("Form Data:", request.form)
            
            #reading inputs given y user
            GenHlth = int(request.form['GenHlth'])
            HighBP = int(request.form['HighBP'])
            BMI = float(request.form['BMI'])
            DiffWalk = int(request.form['DiffWalk'])
            HighChol = int(request.form['HighChol'])
            Age = int(request.form['Age'])
            HeartDiseaseorAttack = int(request.form['HeartDiseaseorAttack'])
            PhysHlth = int(request.form['PhysHlth'])
            Stroke = int(request.form['Stroke'])
            MentHlth = int(request.form['MentHlth'])
            CholCheck = int(request.form['CholCheck'])
            Smoker = int(request.form['Smoker'])
            NoDocbcCost = int(request.form['NoDocbcCost'])
            Sex = int(request.form['Sex'])
            AnyHealthcare = int(request.form['AnyHealthcare'])

            data = [GenHlth, HighBP, BMI, DiffWalk, HighChol, Age, HeartDiseaseorAttack, PhysHlth, Stroke, MentHlth, CholCheck, Smoker, NoDocbcCost, Sex, AnyHealthcare]
            data = np.array(data).reshape(1,15)

            obj = PredictionPipeline()
            predict = obj.predict(data)

            return render_template('results.html', prediction = str(predict))

        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
        
    else:
        return render_template('index.html')
        





if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 8080)