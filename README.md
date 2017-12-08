Stayfe
=======

Flask server for computing safest path between two points

Requirements
--------------

- python 3
- flask
- googlemaps
- polyline
- numpy
- pandas
- scikit-learn


Endpoints
-----------------------

Run the server:

```
python run.py
```

Get crime data between two points:
```
GET /crimes/:src&:dst
```

```
e.g. http://host:port/crimes?src=-122.445,37.74&dst=-122.42,37.715
```

Find the safest path between two points:
```
GET /path/:src&:dst
```

```
e.g. http://host:port/path?src="Hillegaas Avenue, Berkeley, CA"&dst="Soda Hall, Berkeley, CA"
```
