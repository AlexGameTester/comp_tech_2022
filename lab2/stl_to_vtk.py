# STL model is made by mishkin2 https://www.thingiverse.com/mishkin2/designs
# Posted on https://www.thingiverse.com/thing:5203067/files
# And licensed under CC BY-NC 4.0 https://creativecommons.org/licenses/by-nc/4.0/
import numpy as np
import vtk
import gmsh


def main():
    if not create_model():
        return


def create_model():
    gmsh.initialize()

    try:
        gmsh.merge('Honeycomb_organizer.stl')
    except:
        print('File not found')
        return False

    angle = 15
    force_parameterizable_patches = False
    include_boundary = False
    curve_angle = 180

    gmsh.model.mesh.classifySurfaces(angle * np.pi / 180., include_boundary,
                                     force_parameterizable_patches,
                                     curve_angle * np.pi / 180.)

    gmsh.model.mesh.createGeometry()
    s = gmsh.model.getEntities(2)
    loop = gmsh.model.geo.addSurfaceLoop([tag for (_, tag) in s])
    gmsh.model.geo.addVolume([loop])

    gmsh.model.geo.synchronize()

    f = gmsh.model.mesh.field.add("MathEval")
    gmsh.model.mesh.field.setString(f, "F", "4")
    gmsh.model.mesh.field.setAsBackgroundMesh(f)

    gmsh.model.mesh.generate(3)

    node_tags, coord, parametric_coord = gmsh.model.mesh.getNodes()
    element_types, element_tags, node_tags = gmsh.model.mesh.getElements()

    GMSH_TETR_CODE = 4
    tetrs_node_tags = None
    for i in range(len(element_types)):
        if element_types[i] == GMSH_TETR_CODE:
            tetrs_node_tags = node_tags[i]

    if tetrs_node_tags is None:
        print('No tetrahedrons found in model.')
        gmsh.finalize()
        return False


if __name__ == '__main__':
    main()
