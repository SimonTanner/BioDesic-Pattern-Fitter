
def freecad_format(data_list):
    mesh_name = "Mesh.add("
    converted = []
    for poly in data_list[2]:
        # print poly
        polygon = []
        for vert in poly:
            # print vert
            # print data_list[1][vert - 1]
            polygon.append(data_list[1][vert - 1])
        # print polygon
        converted += polygon

    # converted = map(lambda x: mesh_name + str(x) + ")", converted)

    return converted
