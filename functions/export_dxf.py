import ezdxf


def export_to_dxf(points, filepath):
    """
    points: list of (name, x, y)
    filepath: output dxf path
    """

    doc = ezdxf.new(dxfversion="R2010")
    msp = doc.modelspace()

    # --- Layers ---
    doc.layers.new(name="POINTS", dxfattribs={"color": 1})
    doc.layers.new(name="TEXT", dxfattribs={"color": 3})

    for name, x, y in points:
        # Điểm
        msp.add_point((x, y), dxfattribs={"layer": "POINTS"})

        # Text tên điểm
        txt = msp.add_text(
            str(name),
            dxfattribs={
                "height": 1.2,
                "layer": "TEXT"
            }
        )
        txt.dxf.insert = (x + 1, y + 1)

    doc.saveas(filepath)
