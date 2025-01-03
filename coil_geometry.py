import math
from ngsolve import *
from netgen.occ import *

def create_coil_geometry(nwindings=6, wireradius=0.001, coilradius=0.01):
    """
    Creates a 3D geometry of a coil with specified parameters.

    Parameters:
    nwindings (int): Number of windings in the coil. Default is 6.
    wireradius (float): Radius of the wire used to create the coil. Default is 0.001.
    coilradius (float): Radius of the coil. Default is 0.01.

    Returns:
    OCCGeometry: The 3D geometry of the coil and surrounding air.
    """
    coilheight = nwindings * (2 * wireradius) * 1.2
    airh = 10 * coilradius

    cyl = Cylinder((0, 0, -coilheight / 2), Z, r=coilradius, h=coilheight).faces[0]
    heli = Edge(Segment((0, 0), (nwindings * 2 * math.pi, coilheight)), cyl)

    ps = heli.start
    vs = heli.start_tangent
    pe = heli.end
    ve = heli.end_tangent

    spiral = Wire([heli])
    circ = Face(Wire([Circle(ps, Y, wireradius)]))

    coil = Pipe(spiral, circ)

    coil.faces.maxh = 0.2
    coil.faces.name = "coilbnd"
    coil.faces.Max(Z).name = "in"
    coil.faces.Min(Z).name = "out"
    coil.mat("coil")

    crosssection = coil.faces.Max(Z).mass

    box = Box((-airh / 2, -airh / 2, -airh / 2), (airh / 2, airh / 2, airh / 2))
    box.faces.name = "outer"
    air = box - coil
    air.mat("air")

    geo = OCCGeometry(Glue([coil, air]))

    return geo, crosssection


def create_homo_geometry(nwindings=6, wireradius=0.001, coilradius=0.01):
    """
    Create a homogeneous coil geometry.

    Parameters:
    nwindings (int): Number of windings in the coil. Default is 6.
    wireradius (float): Radius of the wire used in the coil. Default is 0.001.
    coilradius (float): Radius of the coil. Default is 0.01.

    Returns:
    OCCGeometry: The combined geometry of the coil and the surrounding air region.
    crosssection: float
    """
    coilheight = nwindings * (2 * wireradius) * 1.2
    airh = 10 * coilradius

    # Create the coil geometry using cylinders
    cyl1 = Cylinder((0, 0, -coilheight / 2), Z, r=coilradius + wireradius, h=coilheight)
    cyl2 = Cylinder((0, 0, -coilheight / 2), Z, r=coilradius - wireradius, h=coilheight)

    # Subtract the inner cylinder from the outer cylinder to form the coil
    coil = cyl1 - cyl2

    # Set mesh size for the coil
    coil.solids.maxh = wireradius
    coil.edges.maxh = wireradius
    coil.faces.maxh = wireradius
    coil.solids.name = 'coil'
    coil.name = 'coil'
        
    crosssection = coil.faces.Max(Z).mass

    # Create the surrounding air box
    box = Box((-airh / 2, -airh / 2, -airh / 2), (airh / 2, airh / 2, airh / 2))
    box.faces.name = "outer"

    # Subtract the coil from the air box to form the air region
    air = box - coil
    air.mat("air")

    # Combine the coil and air region into a single geometry
    geo = OCCGeometry(Glue([coil, air, cube]))

    return geo, crosssection


def create_homo_geometry_cube(nwindings=6, wireradius=0.001, coilradius=0.01, center_x=0, center_y=0, center_z=0):
    """
    Create a homogeneous geometry coil with a cube visualisation.
    Parameters:
    nwindings (int): Number of windings in the coil. Default is 6.
    wireradius (float): Radius of the wire used in the coil. Default is 0.001.
    coilradius (float): Radius of the coil. Default is 0.01.
    center_x (float): X-coordinate of the center of the cube. Default is 0.
    center_y (float): Y-coordinate of the center of the cube. Default is 0.
    center_z (float): Z-coordinate of the center of the cube. Default is 0.
    Returns:
    tuple: A tuple containing the geometry object and the cross-section mass of the coil.
    """
    coilheight = nwindings * (2 * wireradius) * 1.2
    airh = 10 * coilradius

    # Create the coil geometry using cylinders
    cyl1 = Cylinder((0, 0, -coilheight / 2), Z, r=coilradius + wireradius, h=coilheight)
    cyl2 = Cylinder((0, 0, -coilheight / 2), Z, r=coilradius - wireradius, h=coilheight)

    # Subtract the inner cylinder from the outer cylinder to form the coil
    coil = cyl1 - cyl2

    # Set mesh size for the coil
    coil.solids.maxh = wireradius
    coil.edges.maxh = wireradius
    coil.faces.maxh = wireradius
    coil.solids.name = 'coil'
    coil.name = 'coil'
    
    # Dimensions
    width, height, depth = 0.001, 0.001, 0.001

    # Calculate the corner points based on the center and dimensions
    corner1 = (center_x - width / 2, center_y - height / 2, center_z - depth / 2)
    corner2 = (center_x + width / 2, center_y + height / 2, center_z + depth / 2)

    # Create a box using the calculated corner points
    cube = Box(Pnt(*corner1), Pnt(*corner2))
    cube.mat("cube")
    cube.faces.name = "cubebnd"
    cube.solids.name = 'coil'
    cube.name = 'coil'
    
    crosssection = coil.faces.Max(Z).mass

    # Create the surrounding air box
    box = Box((-airh / 2, -airh / 2, -airh / 2), (airh / 2, airh / 2, airh / 2))
    box.faces.name = "outer"

    # Subtract the coil from the air box to form the air region
    air = box - coil
    air.mat("air")

    # Combine the coil and air region into a single geometry
    geo = OCCGeometry(Glue([coil, air, cube]))

    return geo, crosssection