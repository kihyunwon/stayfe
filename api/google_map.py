import googlemaps
import polyline
from datetime import datetime

from safepath import get_waypoints

gmaps = googlemaps.Client(key='AIzaSyDCXWvoPjy1rtQVJ5AqQBC2y8tGQQwOnas')


def decode_polyline(dr):
    return polyline.decode(dr['overview_polyline']['points'])

def geocode(addr):
    res = gmaps.geocode(addr)[0]['geometry']['location']
    return (res['lat'], res['lng'])

# waypoints: a single location, or a list of locations
# optimize_waypoints: let google reorder waypoints
def googleDirection(src, dst):
    src_addr = src
    dst_addr = dst

    if isinstance(src_addr, str):
        src_addr = geocode(src_addr)
    if isinstance(dst_addr, str):
        dst_addr = geocode(dst_addr)

    ss = (src_addr[1], src_addr[0])
    dd = (dst_addr[1], dst_addr[0])
    ways = get_waypoints(ss, dd)
    
    out = []
    sort_keys = sorted(ways.keys())
    for k in sort_keys:
        out.append(tuple(reversed(ways[k])))
    out = out[1:-1]

    now = datetime.now()
    directions = gmaps.directions(src_addr,
                                  dst_addr,
                                  mode='walking',
                                  waypoints=out,
                                  departure_time=now)
    
    return directions

def compute_path(src, dst):
    directions = googleDirection(src, dst)
    dr = directions[0]
    return decode_polyline(dr)

if __name__ == '__main__':
    print(compute_path("Hillegaas Avenue, Berkeley, CA", "Soda Hall, Berkeley, CA"))
