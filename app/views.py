import random
import numpy as np
import pandas as pd
from flask import render_template, jsonify, redirect, flash, request
from flask_googlemaps import GoogleMaps, Map, icons
from .google_map import compute_path
from app import app

app.config['GOOGLEMAPS_KEY'] = "AIzaSyC027Msv7wEU6fsCTFBJoQy52GDraHGCqw"
GoogleMaps(app)

# load the data onto memory
full = pd.read_csv("app/static/data/light_full_classified.csv")
pts = np.asarray(list(zip(full["Lat"], full["Lon"])))

mymap = Map(
        identifier="plinemap",
        style = "height:90%;width:100%;",
        lat=37.871853,
        lng=-122.258423,
    )

@app.route('/')
@app.route("/pathing", methods=["GET"])
def hello():
    
    return render_template("index.html", plinemap=mymap)

@app.route("/pathing", methods=['POST'])
def pathing():
    try:
        if request.form["start"] == "":
            return render_template("index.html", plinemap=mymap)

        start = request.form["start"]
        dest = request.form["dest"]
        shortest_path, safest_path, crimes = compute_path(start, dest)

        crimes = list_to_tuple(crimes)
        shortest = latlon_dict_list(shortest_path)
        safest = latlon_dict_list(safest_path)

        pline_short = {
            'stroke_color': '#B62F00',
            'stroke_opacity': 0.7,
            'stroke_weight': 3,
            'path': shortest
        }

        pline_safe = {
            'stroke_color': '#09B600',
            'stroke_opacity': .9,
            'stroke_weight': 3,
            'path': safest
        }

        if "marker" in request.form:
            plinemap = Map(
                identifier="plinemap",
                varname="plinemap",
                lat=37.871853,
                lng=-122.258423,
                style = "height:90%;width:100%;",
                markers = {"//labs.google.com/ridefinder/images/mm_20_gray.png":crimes},
                polylines=[pline_safe, pline_short]
            )
        else:
            plinemap = Map(
                identifier="plinemap",
                varname="plinemap",
                lat=37.871853,
                lng=-122.258423,
                style = "height:90%;width:100%;",
                polylines=[pline_safe, pline_short]
            )

        return render_template("index.html", plinemap=plinemap)
    except:
        return render_template("index.html", plinemap=mymap)
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


def latlon_dict_list(lst):
    result = []
    for point in lst:
        point_dict = {"lat":point[0], "lng":point[1]}
        result.append(point_dict)
    return result

def list_to_tuple(lst):
    result = []
    for point in lst:
        result.append((point[1], point[0]))
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
