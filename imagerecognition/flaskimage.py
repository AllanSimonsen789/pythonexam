#!flask/bin/python
from flask import Flask, jsonify, abort, request, render_template, url_for, redirect
import pandas as pd
import sqlalchemy as sqla
import animal_data as ad
import url_data as ud
import image_recognizer as ir
import startup as su
import plotter as pl
import uuid
import settings


app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_home():
    return render_template('home.html') 

@app.route('/postanimal', methods=['POST'])
def post_animal():
    #save user picture to static folder
    f = request.files["animal"]
    string = f.filename
    extension = string.split(".")
    filename = uuid.uuid4().hex[:10]
    filepath = settings.FILEPATH + "static/user_files/" + filename + "." + extension[1]
    f.save(filepath)

    ##
    scanresultsvgg = ir.scanpicture(filepath, "vgg")
    #scanresults[1] is a DATAFRAME with results from scan
    pl.plot(scanresultsvgg[1], filename+"vgg")

    ##
    scanresultsmanual = ir.scanpicture(filepath, "manual")
    #scanresults[1] is a DATAFRAME with results from scan
    pl.plot(scanresultsmanual[1], filename+"manual")


    #scanresults[0] is the name of the most likely animal
    url = ud.create_url(filename + "." + extension[1], scanresultsvgg[0], filename + "vgg.png", scanresultsmanual[0], filename + "manual.png")
    return redirect("/result/" + url)


@app.route('/result/<string:res>', methods=['GET'])
def get_result(res):
    resultrow = ud.get_url_data(res)
    picurl = url_for("static", filename='user_files/' + resultrow[2])

    animalvgg = resultrow[5]
    funfactvgg = ad.get_Animal_funfact(resultrow[5])
    plotvgg = url_for("static", filename='plot_files/' + resultrow[6])

    animalmanual = resultrow[3]
    funfactmanual = ad.get_Animal_funfact(resultrow[3])
    plotmanual = url_for("static", filename='plot_files/' + resultrow[4])
    
    return  render_template("result.html", url=settings.URL + res, picurl = picurl, animalvgg = animalvgg, funfactvgg = funfactvgg, plotvgg = plotvgg, animalmanual = animalmanual, funfactmanual = funfactmanual,  plotmanual = plotmanual);


@app.route('/populate', methods=['GET'])
def populate_database():
    su.populate_db()
    return  render_template("home.html");

if __name__ == '__main__':
    app.run(debug=True)