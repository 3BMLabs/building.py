import bpy

def GIS2BIM_BLENDER_CurvestoBlenderCurves(curves):
    blenderCurves = []
    for i in curves:
        verts = []
        for j in i:
            verts.append((j[0], j[1], 0))
        blenderCurves.append(verts)
    return blenderCurves

def GIS2BIM_BLENDER_CurvesToMesh(BlenderCurves,Prefix):
    a = 0
    for i in BlenderCurves:
        a = a + 1
        firstItem = i[0]
        i.append(firstItem) # closed polygon
        vlength = len(i)
        result = list(range(vlength))
        faces = [result]
        GIS2BIM_BLENDER_add_mesh(Prefix + str(a), i, faces)
    return faces

def GIS2BIM_BLENDER_PlaceText(textData,fontSize):
    for i, j, k in zip(textData[0], textData[1], textData[2]):
        loc_txt = bpy.data.curves.new(type="FONT",name="txt")
        loc_txt.body = k
        loc_obj = bpy.data.objects.new("GIS2BIM-text", loc_txt)
        loc_obj.location = (i[0][0], i[0][1], 0)
        bpy.context.scene.collection.objects.link(loc_obj)
    return loc_obj

def GIS2BIM_BLENDER_add_mesh(name, verts, faces, edges=None, col_name="Collection"):
    if edges is None:
        edges = []
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(mesh.name, mesh)
    col = bpy.data.collections.get(col_name)
    col.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    mesh.from_pydata(verts, edges, faces)

def GIS2BIM_BLENDER_draw_line(Coordinate1, Coordinate2, Name):
    #Name is string
    #Coordinate is list of 3 floats
    verts = [Coordinate1,Coordinate2,]
    vlength = len(verts)
    result = list(range(vlength))
    faces = [result]
    GIS2BIM_BLENDER_add_mesh(Name, verts, faces)
