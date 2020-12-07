#!flask/bin/python
from flask import Flask, jsonify, abort, request, render_template, url_for, redirect
import pandas as pd
import sqlalchemy as sqla
import animal_data as ad
import url_data as ud
import image_recognizer as ir
import plotter as pl
import uuid
import settings


app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_home():
    return render_template('home.html') 

@app.route('/postanimal', methods=['POST'])
def post_animal():
    f = request.files["animal"]
    string = f.filename
    extension = string.split(".")
    filename = uuid.uuid4().hex[:10]
    f.save(settings.FILEPATH + "static/user_files/" + filename + "." + extension[1])
    scanresults = ir.scanpicture(settings.FILEPATH + "static/user_files/" + filename + "." + extension[1])
    
    #scanresults[1] is a DATAFRAME with results from scan
    pl.plot(scanresults[1], filename)

    #scanresults[0] is the name of the most likely animal
    url = ud.create_url(scanresults[0] , filename + "." + extension[1], filename + ".png")
    return redirect("/result/" + url)


@app.route('/result/<string:res>', methods=['GET'])
def get_result(res):
    resultrow = ud.get_url(res)
    funfact = ad.get_animal(resultrow[2])
    return  render_template("result.html", url="http://127.0.0.1:5000/result/" + res, animal=resultrow[2], funfact=funfact, picurl=url_for("static", filename='user_files/' + resultrow[3]), ploturl=url_for("static", filename='plot_files/' + resultrow[4]));


@app.route('/about', methods=['GET'])
def get_about():
    ad.populate_db()
    return  render_template("home.html");

@app.route('/plot', methods=['GET'])
def get_plot():
    ad.plot()
    return  render_template("home.html");

if __name__ == '__main__':
    app.run(debug=True)