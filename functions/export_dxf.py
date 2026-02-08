import ezdxf

def export_to_dxf(points, filename):
    """
    points = [
        ("pt1", X, Y),
        ("pt2", X, Y),
        ...
    ]
    """
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()

    # Layer
    doc.layers.new(name="POINTS", dxfattribs={"color": 1})
    doc.layers.new(name="TEXT", dxfattribs={"color": 2})
    doc.layers.new(name="POLY", dxfattribs={"color": 3})

    # Vẽ point + text
    for name, x, y in points:
        msp.add_point((y, x), dxfattribs={"layer": "POINTS"})
        msp.add_text(
            name,
            dxfattribs={"height": 1.5, "layer": "TEXT"}
        ).set_pos((y + 1, x + 1))

    # Vẽ polyline nếu >2 điểm
    if len(points) >= 2:
        poly_points = [(y, x) for _, x, y in points]
        msp.add_lwpolyline(poly_points, close=True, dxfattribs={"layer": "POLY"})

    doc.saveas(filename)
