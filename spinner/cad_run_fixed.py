# %%
from build123d import *
from ocp_vscode import *

set_port(3939)

set_defaults(reset_camera=Camera.CENTER, helper_scale=5)
show_clear()

fillet_radius = 0.2 * MM
width_peg = 4.8 * MM
length_peg = 7.5 * MM
height_peg = 8 * MM

big_radius = 5.5 * MM
small_radius = 3.5 * MM

top_radius = small_radius
total_heigth = 44 * MM
distance_loft = 3 * MM
slot_width = 1.5 * MM
slot_length = total_heigth - distance_loft - height_peg
slot_offset = 1 * MM

with BuildPart() as peg:
    with BuildSketch() as rect_sk:
        RectangleRounded(width_peg, length_peg, fillet_radius)
    extrude(amount=height_peg)

    top_plane_peg = peg.faces().sort_by(sort_by=Axis.Z)[-1]

    with BuildSketch(top_plane_peg) as circle_big_sk:
        big_circle = Circle(big_radius)

    plane_small_circle = Plane(origin=(0, 0, height_peg + distance_loft))

    with BuildSketch(plane_small_circle) as circle_small_sk:
        Circle(small_radius)

    loft()

    ##########
    edge_of_big_circle = (
        peg.edges(Select.LAST).filter_by(GeomType.CIRCLE).sort_by(Axis.Z)[0]
    )
    fillet(edge_of_big_circle, fillet_radius)

    ##########
    plane_top_circle = Plane(origin=(0, 0, total_heigth))

    with BuildSketch(plane_top_circle, mode=Mode.PRIVATE) as circle_top_sk:
        Circle(top_radius)

    loft(sections=[circle_top_sk.sketch.face(), circle_small_sk.sketch.face()])

    ##########
    # line along the last loft
    vertical_edge_of_loft = peg.edges(Select.LAST).filter_by(Plane.YZ)[0]

    with BuildSketch(
        Plane(origin=vertical_edge_of_loft @ 0.5, z_dir=(1, 0, 0)),
    ) as slot_sk:
        with Locations((slot_offset, 0)):
            SlotOverall(slot_length, slot_width)
        with Locations((slot_length / 2, 0)):
            Rectangle(slot_width, slot_width)
    extrude(amount=-top_radius + 1 * MM, mode=Mode.SUBTRACT)

    with BuildSketch(
        Plane(origin=vertical_edge_of_loft @ 1, z_dir=(1, 0, 0)),
    ) as hole_sk:
        with Locations((slot_offset, 0)):
            Circle(slot_width / 2 - 0.2, align=(Align.MIN, Align.CENTER))
    extrude(amount=-top_radius - 1 * MM, mode=Mode.SUBTRACT)

# show_object(peg.part, clear=True)
# for i, line in enumerate(all_lines):
#     show_object(line, name="line" + str(i))

# for i, circle in enumerate(all_circles):
#     show_object(circle, name="circle" + str(i))
show_clear()

show_all()

export_step(peg.part, "/home/bebe/Code/cad_projects/spinner/peg.step")
