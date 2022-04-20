import math


def distance(c1, c2):
    lat1, lon1 = c1
    lat2, lon2 = c2

    to_rad = math.pi / 180

    R = 6371
    phi1 = lat1 * to_rad
    phi2 = lat2 * to_rad
    d_phi = (lat2 - lat1) * to_rad
    d_lambda = (lon2 - lon1) * to_rad

    a = (math.sin(d_phi / 2) ** 2) + math.cos(phi1) * math.cos(phi2) * (math.sin(d_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

