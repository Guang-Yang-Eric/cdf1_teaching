"""
Geometry basics -- reusable Rhino.Geometry functions for Grasshopper.

Adding a new function with Copilot
-----------------------------------
1. Open this file and select this chat model, then ask Copilot something like:
   "Add a function here, all in Rhino geometry, that builds a <your shape/idea>.
   Follow the same style as create_cone / create_fractal_tree (defaults for
   optional inputs, a docstring listing params, return a Rhino.Geometry object)."
2. Once the function is added, ask Copilot:
   "Give me the Python code to use this function in a Grasshopper GHPython 3
   component, importing it from computational_design_and_fabrication."
3. Copy the snippet Copilot gives you into a GHPython component, wire up the
   inputs as sliders/panels, and set the output variable (e.g. `a`).
"""

import math
import Rhino.Geometry as rg
import random

def create_cube(base_point=None, length=1.0, width=1.0, height=1.0):
    """
    Build a cube as a Brep.

    base_point : Rhino.Geometry.Point3d -- corner of the cube
    length     : float -- length of the cube
    width      : float -- width of the cube
    height     : float -- height of the cube

    Returns a Rhino.Geometry.Brep.
    """
    if base_point is None:
        base_point = rg.Point3d(0, 0, 0)

    if length is None or width is None or height is None:
        raise ValueError("Length, width, and height must be provided.")

    if length <= 0 or width <= 0 or height <= 0:
        raise ValueError("Length, width, and height must be positive values.")

    plane = rg.Plane(base_point, rg.Vector3d.ZAxis)
    box = rg.Box(plane, rg.Interval(0, length), rg.Interval(0, width), rg.Interval(0, height))
    return box.ToBrep()

def create_cone(base_point=None, height=10.0, radius=5.0, cap_bottom=True):
    """
    Build a cone as a Brep.

    base_point : Rhino.Geometry.Point3d -- center of the cone's base circle
    height     : float -- cone height along the base plane's normal (Z by default)
    radius     : float -- base circle radius
    cap_bottom : bool  -- whether to cap the base circle (closed vs open cone)

    Returns a Rhino.Geometry.Brep.
    """
    if base_point is None:
        base_point = rg.Point3d(0, 0, 0)

    plane = rg.Plane(base_point, rg.Vector3d.ZAxis)
    cone = rg.Cone(plane, height, radius)
    return cone.ToBrep(cap_bottom)

def create_cylinder(base_point=None, height=10.0, radius=5.0, cap_bottom=True, cap_top=True):
    """
    Build a cylinder as a Brep.

    base_point : Rhino.Geometry.Point3d -- center of the cylinder's base circle
    height     : float -- cylinder height along the base plane's normal (Z by default)
    radius     : float -- base circle radius
    cap_bottom : bool  -- whether to cap the bottom circle (closed vs open cylinder)
    cap_top    : bool  -- whether to cap the top circle (closed vs open cylinder)

    Returns a Rhino.Geometry.Brep.
    """
    if base_point is None:
        base_point = rg.Point3d(0, 0, 0)

    plane = rg.Plane(base_point, rg.Vector3d.ZAxis)
    circle = rg.Circle(plane, radius)
    cylinder = rg.Cylinder(circle, height)
    return cylinder.ToBrep(cap_bottom, cap_top)

def create_sphere(center_point=None, radius=5.0):
    """
    Build a sphere as a Brep.

    center_point : Rhino.Geometry.Point3d -- center of the sphere
    radius     : float -- radius of the sphere

    Returns a Rhino.Geometry.Brep.
    """
    pass  # TODO: Implement this function to create a sphere using Rhino.Geometry

    if center_point is None:
        center_point = rg.Point3d(0, 0, 0)

    return rg.Sphere(center_point, radius)

def  create_torus(center_point=None, major_radius=5.0, minor_radius=2.0):
    """
    Build a torus as a Brep.

    center_point : Rhino.Geometry.Point3d -- center of the torus
    major_radius : float -- distance from the center of the torus to the center of the tube
    minor_radius : float -- radius of the tube

    Returns a Rhino.Geometry.Brep.
    """
    if center_point is None:
        center_point = rg.Point3d(0, 0, 0)

    if major_radius <= 0 or minor_radius <= 0:
        raise ValueError("Major and minor radii must be positive values.")

    if minor_radius >= major_radius:
        raise ValueError("Minor radius must be smaller than major radius.")

    plane = rg.Plane(center_point, rg.Vector3d.ZAxis)
    torus = rg.Torus(plane, major_radius, minor_radius)
    return torus.ToBrep()

def boolean_difference(brep_a, brep_b):
    """
    Perform a boolean difference operation between two Breps.

    brep_a : Rhino.Geometry.Brep -- the first Brep
    brep_b : Rhino.Geometry.Brep -- the second Brep to subtract from the first

    Returns a list of Rhino.Geometry.Brep resulting from the difference.
    """
    if brep_a is None or brep_b is None:
        raise ValueError("Both brep_a and brep_b must be provided.")

    result = rg.Brep.CreateBooleanDifference(brep_a, brep_b, 0.001)
    return result

def boolean_union(brep_a, brep_b):
    """
    Perform a boolean union operation between two Breps.

    brep_a : Rhino.Geometry.Brep -- the first Brep
    brep_b : Rhino.Geometry.Brep -- the second Brep to union with the first

    Returns a list of Rhino.Geometry.Brep resulting from the union.
    """
    if brep_a is None or brep_b is None:
        raise ValueError("Both brep_a and brep_b must be provided.")

    result = rg.Brep.CreateBooleanUnion([brep_a, brep_b], 0.001)
    return result

def boolean_intersection(brep_a, brep_b):
    """
    Perform a boolean intersection operation between two Breps.

    brep_a : Rhino.Geometry.Brep -- the first Brep
    brep_b : Rhino.Geometry.Brep -- the second Brep to intersect with the first

    Returns a list of Rhino.Geometry.Brep resulting from the intersection.
    """
    if brep_a is None or brep_b is None:
        raise ValueError("Both brep_a and brep_b must be provided.")

    result = rg.Brep.CreateBooleanIntersection(brep_a, brep_b, 0.001)
    return result

def copy_brep_along_z(brep, distance, copy_count):
    """
    Create copies of a Brep, each offset in the +Z direction.

    brep : Rhino.Geometry.Brep -- the Brep to copy
    distance : float -- the Z spacing between consecutive copies
    copy_count : int -- the number of copies to create

    Returns a list of Rhino.Geometry.Brep copies; copy i is moved by distance * (i + 1).
    """
    if brep is None:
        raise ValueError("brep must be provided.")
    if copy_count < 0:
        raise ValueError("copy_count must not be negative.")

    copies = []
    for i in range(1, int(copy_count) + 1):
        copy = brep.DuplicateBrep()
        copy.Transform(rg.Transform.Translation(rg.Vector3d(0, 0, distance * i)))
        copies.append(copy)
    return copies

def copy_brep_along_x(brep, distance, copy_count):
    """
    Create copies of a Brep, each offset in the +X direction.

    brep : Rhino.Geometry.Brep -- the Brep to copy
    distance : float -- the X spacing between consecutive copies
    copy_count : int -- the number of copies to create

    Returns a list of Rhino.Geometry.Brep copies; copy i is moved by distance * (i + 1).
    """
    if brep is None:
        raise ValueError("brep must be provided.")
    if copy_count < 0:
        raise ValueError("copy_count must not be negative.")

    copies = []
    for i in range(1, int(copy_count) + 1):
        copy = brep.DuplicateBrep()
        copy.Transform(rg.Transform.Translation(rg.Vector3d(distance * i, 0, 0)))
        copies.append(copy)
    return copies

def rotate_brep(brep, angle_degrees, axis_point=None, axis_direction=None):
    """
    Rotate a Brep around a specified axis.

    brep : Rhino.Geometry.Brep -- the Brep to rotate
    angle_degrees : float -- rotation angle in degrees
    axis_point : Rhino.Geometry.Point3d -- a point on the rotation axis (default is origin)
    axis_direction : Rhino.Geometry.Vector3d -- direction of the rotation axis (default is Z-axis)

    Returns a new rotated Rhino.Geometry.Brep.
    """
    if brep is None:
        raise ValueError("brep must be provided.")

    if axis_point is None:
        axis_point = rg.Point3d(0, 0, 0)
    if axis_direction is None:
        axis_direction = rg.Vector3d.ZAxis

    rotation_transform = rg.Transform.Rotation(math.radians(angle_degrees), axis_direction, axis_point)
    rotated_brep = brep.DuplicateBrep()
    rotated_brep.Transform(rotation_transform)
    return rotated_brep

def _path_points(width, max_length, steps, angle_step, max_turn, seed):
    values = (width, max_length, steps, angle_step, max_turn, seed)
    if any(v is None for v in values):
        raise ValueError("Connect all six inputs to sliders.")
    if not all(math.isfinite(float(v)) for v in values):
        raise ValueError("Inputs must be finite numbers.")
    if width <= 0 or max_length <= 0:
        raise ValueError("width and max_length must be positive.")
    if int(steps) != steps or not 1 <= steps <= 200:
        raise ValueError("steps must be an integer from 1 to 200.")
    if angle_step <= 0 or not 0 <= max_turn <= 180:
        raise ValueError("Need angle_step > 0 and 0 <= max_turn <= 180.")
    if int(seed) != seed:
        raise ValueError("seed must be an integer.")

    # Separate random streams keep lengths unchanged when angles change.
    lengths_rng = random.Random(int(seed))
    turns_rng = random.Random(int(seed) + 100003)
    turn_count = int(math.floor(max_turn / angle_step + 1e-10))
    points = [(0.0, 0.0)]
    heading = 0.0
    for i in range(int(steps)):
        if i > 0:
            turn = turns_rng.randint(-turn_count, turn_count) * angle_step
            heading += math.radians(turn)
        length = lengths_rng.uniform(0.5 * max_length, max_length)
        x, y = points[-1]
        points.append((x + length * math.cos(heading),
                       y + length * math.sin(heading)))
    return points


def create_random_path(width=4.0, max_length=15.0, steps=10,
                       angle_step=90.0, max_turn=90.0, seed=1):
    """Return road_parts (Brep list), centerline, info.

    Starts at world origin, first segment points along +X.
    max_length is the maximum length PER SEGMENT, not a site boundary.
    Pieces overlap at circular joints; they are not Boolean-unioned.
    Crossings and revisits are allowed. All parts use a fixed height of 0.2.
    """

    coords = _path_points(width, max_length, steps, angle_step, max_turn, seed)
    points = [rg.Point3d(x, y, 0) for x, y in coords]
    road_parts = []
    half = width / 2.0
    thickness = 0.2
    total_length = 0.0

    # Each rectangle starts exactly where the preceding one ends.
    for i in range(len(points) - 1):
        start, end = points[i], points[i + 1]
        direction = end - start
        length = direction.Length
        direction.Unitize()
        side = rg.Vector3d(-direction.Y, direction.X, 0)
        plane = rg.Plane(start, direction, side)
        box = rg.Box(plane, rg.Interval(0, length),
                     rg.Interval(-half, half), rg.Interval(0, thickness))
        brep = box.ToBrep()
        if brep is None or not brep.IsValid:
            raise ValueError("Failed to create a road rectangle.")
        road_parts.append(brep)
        total_length += length

    # Round joints overlap adjacent rectangles and fill turning gaps.
    for point in points:
        circle = rg.Circle(rg.Plane(point, rg.Vector3d.ZAxis), half)
        joint = rg.Cylinder(circle, thickness).ToBrep(True, True)
        if joint is None or not joint.IsValid:
            raise ValueError("Failed to create a round joint.")
        road_parts.append(joint)

    centerline = rg.PolylineCurve(points)
    info = "Segments: {} | Parts: {} | Total centerline length: {:.2f}".format(
        int(steps), len(road_parts), total_length)
    return road_parts, centerline, info

def create_brep_cloud(
    brep_a, brep_b, brep_c,
    length, width, count,
    spacing_x, spacing_y,
    seed=1
):
    rng = random.Random(int(seed))

    models = [brep_a, brep_b, brep_c]
    points = []
    copies_a = []
    copies_b = []
    copies_c = []

    anchors = []

    for model in models:
        box = model.GetBoundingBox(True)

        anchor = rg.Point3d(
            (box.Min.X + box.Max.X) / 2,
            (box.Min.Y + box.Max.Y) / 2,
            box.Min.Z
        )

        anchors.append(anchor)

    for attempt in range(int(count) * 300):

        if len(points) >= int(count):
            break

        point = rg.Point3d(
            rng.uniform(0, length),
            rng.uniform(0, width),
            0
        )

        too_close = False

        for old_point in points:
            if (
                abs(point.X - old_point.X) < spacing_x
                and abs(point.Y - old_point.Y) < spacing_y
            ):
                too_close = True
                break

        if too_close:
            continue

        index = rng.randrange(3)

        copy = models[index].DuplicateBrep()
        move = rg.Transform.Translation(
            point - anchors[index]
        )
        copy.Transform(move)

        points.append(point)
        if index == 0:
            copies_a.append(copy)
        elif index == 1:
            copies_b.append(copy)
        else:
            copies_c.append(copy)

    return copies_a, copies_b, copies_c, points