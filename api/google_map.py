import polyline
import googlemaps
from datetime import datetime

from safepath import get_waypoints

gmaps = googlemaps.Client(key='your client key')


def decode_polyline(dr):
    steps = dr['legs'][0]['steps']
    for i in range(len(steps)):
        steps[i]['polyline'] = polyline.decode(steps[i]['polyline']['points'])

def geocode(addr):
    res = gmaps.geocode(addr)[0]['geometry']['location']
    return (res['lat'], res['lng'])

# waypoints: a single location, or a list of locations
# optimize_waypoints: let google reorder waypoints
def googleDirection(src, dst, optimize_waypoints=True):
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
                                  departure_time=now,
                                  waypoints=out,
                                  optimize_waypoints=optimize_waypoints)
    
    return directions
    
def select_coords(dr):
    coords = []
    indices = []
    steps = dr['legs'][0]['steps']
    
    idx = 0
    for i in range(len(steps)):
        coords += steps[i]['polyline']
        idx += len(steps[i]['polyline'])
        indices.append(idx)
    
    # store original index
    return coords, indices

def compute_path(src, dst, waypoints=True):
    directions = googleDirection(src, dst, waypoints)
    dr = directions[0]
    decode_polyline(dr)
    coords, indices = select_coords(dr)
    return coords

if __name__ == '__main__':
    directions = googleDirection("Hillegaas Avenue, Berkeley, CA", "Soda Hall, Berkeley, CA")
    dr = directions[0]
    decode_polyline(dr)
    coords, indices = select_coords(dr)
