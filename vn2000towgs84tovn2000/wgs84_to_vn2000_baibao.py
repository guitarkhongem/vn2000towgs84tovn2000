
import math

def wgs84_to_vn2000_baibao(lat_deg, lon_deg, h, lon0_deg):
    a = 6378137.0
    f = 1 / 298.257223563
    e2 = 0.00669437999013
    ep2 = e2 / (1 - e2)
    k0 = 0.9999
    y0 = 500000

    B = math.radians(lat_deg)
    L = math.radians(lon_deg)
    L0 = math.radians(lon0_deg)

    N = a / math.sqrt(1 - e2 * math.sin(B)**2)
    Xw = (N + h) * math.cos(B) * math.cos(L)
    Yw = (N + h) * math.cos(B) * math.sin(L)
    Zw = ((1 - e2) * N + h) * math.sin(B)

    dX = -191.90441429
    dY = -39.30318279
    dZ = -111.45032835
    rx = math.radians(-0.00928836 / 3600)
    ry = math.radians(0.01975479 / 3600)
    rz = math.radians(-0.00427372 / 3600)
    k = 1.000000252906278

    Xs = Xw - dX
    Ys = Yw - dY
    Zs = Zw - dZ

    Xv = (1 / k) * (Xs - rz * Ys + ry * Zs)
    Yv = (1 / k) * (rz * Xs + Ys - rx * Zs)
    Zv = (1 / k) * (-ry * Xs + rx * Ys + Zs)

    p = math.sqrt(Xv**2 + Yv**2)
    gamma = math.atan((Zv / p) * (1 - f + (a * e2) / math.sqrt(Xv**2 + Yv**2 + Zv**2)))
    B_vn = math.atan((Zv * (1 - f) + a * e2 * math.sin(gamma)**3) / ((1 - f) * (p - a * e2 * math.cos(gamma)**3)))
    L_vn = math.atan2(Yv, Xv)
    if L_vn < 0:
        L_vn += 2 * math.pi
    H_vn = math.cos(B_vn) * p + Zv * math.sin(B_vn) - a * math.sqrt(1 - e2 * math.sin(B_vn)**2)

    l = L_vn - L0
    eta = math.sqrt(ep2) * math.cos(B_vn)
    T = math.tan(B_vn)**2
    C = ep2 * math.cos(B_vn)**2
    N = a / math.sqrt(1 - e2 * math.sin(B_vn)**2)

    A1x = (math.cos(B_vn)**2 * (5 - T + 9 * eta**2 + 4 * eta**4)) / 12
    A2x = (math.cos(B_vn)**4 * (61 - 58 * T + T**2)) / 360
    A1y = (math.cos(B_vn)**2 * (1 - T + eta**2)) / 6
    A2y = (math.cos(B_vn)**4 * (5 - 18 * T + T**2 + 14 * eta**2 - 58 * T * eta**2)) / 120

    A1 = 1 + 3/4 * e2 + 45/64 * e2**2
    A2 = 3/8 * e2 + 15/32 * e2**2
    A3 = 15/256 * e2**2
    XB = a * (1 - e2) * (A1 * B_vn - A2 * math.sin(2 * B_vn) + A3 * math.sin(4 * B_vn))

    x = k0 * (XB + l**2 / 4 * N * math.sin(2 * B_vn) * (1 + A1x * l**2 + A2x * l**4))
    y = k0 * l * N * math.cos(B_vn) * (1 + A1y * l**2 + A2y * l**4) + y0

    return round(x, 4), round(y, 4), round(H_vn, 4)
