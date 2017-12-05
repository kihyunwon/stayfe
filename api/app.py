import random
import numpy as np
import pandas as pd
from flask import Flask
from flask import request, jsonify
from flask import render_template, redirect, flash
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

app = Flask(__name__)
app.config['GOOGLEMAPS_KEY'] = "AIzaSyC027Msv7wEU6fsCTFBJoQy52GDraHGCqw"

GoogleMaps(app)

from google_map import compute_path


# load the data onto memory
full = pd.read_csv("../data/light_full_classified.csv")
pts = np.asarray(list(zip(full["Lat"], full["Lon"])))


@app.route('/')
def hello():
    mymap = Map(
        identifier="main-map",
        lat=37.871853,
        lng=-122.258423,
    )
    return render_template("index.html", plinemap=mymap)

@app.route("/pathing", methods=['GET', 'POST'])
def pathing():
    start = request.form["start"]
    dest = request.form["dest"]
    path = compute_path(start, dest) #List of tuples of (longitudes, lats)

    print(path)
    points = []
    for point in path:
        point_dict = {"lat":point[0], "lng":point[1]}
        points.append(point_dict)

    polyline = {
        'stroke_color': '#0AB0DE',
        'stroke_opacity': 1.0,
        'stroke_weight': 3,
        'path': points
    }

    plinemap = Map(
        identifier="plinemap",
        varname="plinemap",
        lat=37.8702804,
        lng=-122.3212382,
        polylines=[polyline]
        )
    print(points)
    return render_template("index.html", plinemap=plinemap)

# e.g. host:port/crimes?src=-122.445,37.74&dst=-122.42,37.715
@app.route('/crimes', methods=['GET'])
def serve_crime():
    src = request.args.get('src') or '0,0'
    dst = request.args.get('dst') or '0,0'

    src = tuple(map(lambda x: float(x), src.split(',')))
    dst = tuple(map(lambda x: float(x), dst.split(',')))

    ll = np.asarray(src)  # lower-left
    ur = np.asarray(dst)  # upper-right

    inidx = np.all(np.logical_and(ll <= pts, pts <= ur), axis=1)
    inbox = pts[inidx]
    outbox = pts[np.logical_not(inidx)]

    return jsonify(list(map(tuple, inbox)))
    
# e.g. host:port/path?src="Hillegaas Avenue, Berkeley, CA"&dst="Soda Hall, Berkeley, CA"
@app.route('/path', methods=['GET'])
def serve_path():
    src = request.args.get('src') or ''
    dst = request.args.get('dst') or ''

    path = compute_path(src, dst)
    
    return jsonify(path) 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
