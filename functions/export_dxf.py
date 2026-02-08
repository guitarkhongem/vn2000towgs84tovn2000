import ezdxf


def export_to_dxf(points, filepath):
    """
    points: list of (name, x, y)  # x = Easting, y = Northing (VN2000)
    filepath: output dxf path
    """

    doc = ezdxf.new(dxfversion="R2010")
    msp = doc.modelspace()

    # --- Layers ---
    if "POINTS" not in doc.layers:
        doc.layers.new(name="POINTS", dxfattribs={"color": 1})
    if "TEXT" not in doc.layers:
        doc.layers.new(name="TEXT", dxfattribs={"color": 3})

    for name, x, y in points:
        # --- Vẽ điểm (ĐÚNG TRỤC) ---
        msp.add_point(
            (x, y),
            dxfattribs={"layer": "POINTS"}
        )

        # --- Ghi tên điểm (lệch nhẹ để dễ nhìn) ---
        txt = msp.add_text(
            str(name),
            dxfattribs={
                "height": 1.2,
                "layer": "TEXT"
            }
        )
        txt.dxf.insert = (x + 1.0, y + 1.0)

    doc.saveas(filepath)
