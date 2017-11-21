import os, pygame, sys, math, random, itertools, copy

from pygame.locals import *

file_name = "test_data/Skinny-v5.txt"

file_path = os.path.join(os.getcwd(), file_name)

file_path_new = file_path[:-4] + '_new_V2.txt'

op_file = open(file_path, 'r')
op_file_new = open(file_path_new, 'w')

data_list = []

pygame.init()

FPS = 30
FPSClock = pygame.time.Clock()

Screen_width = 1200
Screen_height = 800

for line in op_file:
    data_list.append(line)

def convert_data(dat):

    while True:

        try:
            while True:

                try:

                    for o in range(0, len(dat)):
                        dat[o] = float(dat[o])

                        if dat[o]%1 == 0:
                            dat[o] = int(dat[o])

                except ValueError:

                    del(dat[o])

                except TypeError:

                    del(dat[o])

                except IndexError:

                    break

                else:
                    break


        except IndexError:

            break

        else:

            break



def format_list(data):

    for i in range(0, len(data)):
        data[i] = data[i].translate(None, '[')
        data[i] = data[i].translate(None, '\n')
        data[i] = data[i].split(']')

    for m in range(0, len(data)):
         for n in range(0, len(data[m])):
             data[m][n] = data[m][n].split(',')

    for m in range(0, len(data)):
        for n in range(0, len(data[m])):
            convert_data(data[m][n])

    for m in range(0, len(data)):
        for n in range(0, len(data[m])):
            if len(data[m][n]) == 0:
                del(data[m][n])

    check_data(data)


def check_data(data):

    #data = copy.deepcopy(data1)

    error_val = 0.001
    errors = []
    face_delete = []

    for i in range(0, len(data[1])):
        for k in range(i, len(data[1])):

            if i != k:

                diff = map(lambda a, b: abs(a - b), data[1][i], data[1][k])

                if diff[0] < error_val and diff[1] < error_val and diff[2] < error_val:

                    errors.append([i+1, k+1])

    for i in range(0, len(errors)):

        for k in range(0, len(data[2])):

            while True:

                try:
                    n = data[2][k].index(errors[i][1])

                    data[2][k][n] = errors[i][0]

                except ValueError:

                    break

                else:

                    break

    for i in range(0, len(errors)):

        index = len(errors) - i -1

        delete = errors[index][1] - 1

        del(data[1][delete])



    for i in range(0, len(data[2])):

        for k in range(i, len(data[2])):

            face_errors = []

            for m in range(0, len(data[2][i])):

                while i != k and True:

                    try:
                        n = data[2][k].index(data[2][i][m])

                        if len(face_errors) > 0:

                            face_errors.index(n)

                        face_errors.append(n)

                    except ValueError:

                        break

                    else:

                        break

            if len(face_errors) == 3:

                face_delete.append([i, k, face_errors])

        for l in range(0, len(data[2][i])-1):

            for p in range(1, len(data[2][i])):

                if l != p:

                    if data[2][i][l] == data[2][i][p]:

                        face_delete.append([i])


    for i in range(0, len(face_delete)):

        index = len(face_delete) - 1 - i

        delete = face_delete[index][-1]

        del(data[2][delete])

    data[0][0][0] = len(data[1])
    data[0][0][1] = len(data[2])

    #return data, errors, face_delete







def calc_planes(data):

    planes = []

    for i in range(0, len(data[2])):

        point_1 = data[2][i][0] - 1

        point_2 = data[2][i][1] - 1

        point_3 = data[2][i][2] - 1

        vert_1 = data[1][point_1]

        vert_2 = data[1][point_2]

        vert_3 = data[1][point_3]

        vec_1, vec_2 =  [], []

        vec_1 = map(lambda a, b: a - b, vert_2, vert_1)
        vec_2 = map(lambda a, b: a - b, vert_3, vert_1)

        x = vec_1[1] * vec_2[2] - vec_1[2] * vec_2[1]
        y = vec_1[2] * vec_2[0] - vec_1[0] * vec_2[2]
        z = vec_1[0] * vec_2[1] - vec_1[1] * vec_2[0]

        d = ((vert_1[0] * x) + (vert_1[1] * y) + (vert_1[2] * z))
        plane_eqn = [x, y, z, d]

        planes.append([i + 1, plane_eqn])

    return(planes)


def calc_normals(vec_1, vec_2):

    i = vec_1[1] * vec_2[2] - vec_1[2] * vec_2[1]
    j = vec_1[2] * vec_2[0] - vec_1[0] * vec_2[2]
    k = vec_1[0] * vec_2[1] - vec_1[1] * vec_2[0]

    length = (math.sqrt( (i ** 2) + (j ** 2) + (k ** 2)))

    i = i/length
    j = j/length
    k = k/length

    normal = [i, j, k]

    return(normal)



def calc_line_eqn(vec_1, vert_1):

    # Function to calculate the equation of a line

    while True:

        try:

            m = vec_1[1] / vec_1[0]

        except ZeroDivisionError:

            # if dy/dx = inf then m is set to False

            m = None

            break

        else:

            break

    while True:

        try:

            n = vec_1[2] / vec_1[0]

        except ZeroDivisionError:

            n = None

            break

        else:

            break

    while True:

        try:

            o = vec_1[1] / vec_1[2]

        except ZeroDivisionError:

            o = None

            break

        else:

            break

    x = vert_1[0]
    y = vert_1[1]
    z = vert_1[2]

    #print m, n , o

    if m != None:

        c = y - m * x

    else:

        c = x

    if n != None:

        b = z - n * x

    else:

        b = x

    if o != None:

        a = y - o * z

    else:

        a = z

    #a = (y - n * x) / (z - m * x)

    eqn_xy = [m, c]
    eqn_xz = [n, b]
    eqn_zy = [o, a]


    return([eqn_xy, eqn_xz, eqn_zy])




def calc_line_eqn_2(point_1, point_2):

    dx, dy, dz = map(lambda a, b: a - b, point_2, point_1)

    # Function to calculate the equation of a line

    while True:

        try:

            m = dy / dx

        except ZeroDivisionError:

            # if dy/dx = inf then m is set to False then m_1 is set to 0 = dx/dy

            m = None

            break

        else:

            break

    while True:

        try:

            n = dz / dx

        except ZeroDivisionError:

            n = None

            break

        else:

            break

    while True:

        try:

            o = dy / dz

        except ZeroDivisionError:

            o = None

            break

        else:

            break

    x, y, z = point_1

    if m != None:

        c = y - m * x

    else:

        c = x

    if n != None:

        b = z - n * x

    else:

        b = x

    if o != None:

        a = y - o * z

    else:

        a = z

    #a = (y - n * x) / (z - m * x)

    eqn_xy = [m, c]
    eqn_xz = [n, b]
    eqn_zy = [o, a]


    return([eqn_xy, eqn_xz, eqn_zy])






def equations(data):

    lines_eqn = []

    for i in range(0, len(data[2])):

        vert_1 = (data[2][i][0] - 1)
        vert_2 = (data[2][i][1] - 1)
        vert_3 = (data[2][i][2] - 1)

        vec_1, vec_2, vec_3 =  [], [], []

        for n in range(0, len(data[1][vert_1])):

            vec_1.append(data[1][vert_2][n] - data[1][vert_1][n])
            vec_2.append(data[1][vert_3][n] - data[1][vert_2][n])
            vec_3.append(data[1][vert_1][n] - data[1][vert_3][n])

        eqn_1 = calc_line_eqn(vec_1, data[1][vert_1])
        eqn_2 = calc_line_eqn(vec_2, data[1][vert_2])
        eqn_3 = calc_line_eqn(vec_3, data[1][vert_3])

        normal = calc_normals(vec_1, vec_2)

        lines_eqn.append([i+1, [(vert_1 + 1), vec_1, eqn_1], [(vert_2 + 1), vec_2, eqn_2], [(vert_3 + 1), vec_3, eqn_3], normal])


    return(lines_eqn)



def vert_connects(data):

    connections = []

    for n in range(1, data[0][0][0] + 1):

        connections.append([n])

        connects = []

        for j in range(0, data[0][0][1]):


            while True:

                try:

                    count = data[2][j].index(n)

                    for k in range(0, len(data[2][j])):

                        if k != count:

                            while True:

                                try:
                                    connects.index(data[2][j][k])

                                except ValueError:

                                    connects.append(data[2][j][k])

                                else:

                                    break

                except ValueError:

                    break

                else:

                    break

        if len(connects) > 0:

            connections[n-1].append(connects)

        #connections[n-1] = list(itertools.chain(connections[n-1]))


    return(connections)




def face_connects(data):

    connections = []

    for n in range(1, data[0][0][0] + 1):

        connections.append([n])

        connects = []

        for j in range(0, data[0][0][1]):


            while True:

                try:

                    count = data[2][j].index(n)


                    while True:

                        try:
                            connects.index(j + 1)

                        except ValueError:

                            connects.append(j + 1)

                            break

                        else:

                            break

                except ValueError:

                    break

                else:

                    break

        if len(connects) > 0:

            connections[n-1].append(connects)


    return(connections)



def avg_normal(vert, data, equations):

    av_norm = [0.0, 0.0, 0.0]

    connections = face_connects(data)

    for i in range(0, len(connections[vert - 1][1])):

        face = connections[vert - 1][1][i] - 1

        av_norm = map(lambda a, b: a + b, equations[face][4], av_norm)

    av_norm_len = math.sqrt(sum(map(lambda x: x ** 2, av_norm)))

    for n in range(0, 3):

        av_norm[n] /= av_norm_len

    return(av_norm)




def plane_cutter(coord_1, coord_2, coord_3):


    vec_1, vec_2 =  [], []

    vec_1 = map(lambda a, b: a - b, coord_2, coord_1)
    vec_2 = map(lambda a, b: a - b, coord_3, coord_1)

    x = vec_1[1] * vec_2[2] - vec_1[2] * vec_2[1]
    y = vec_1[2] * vec_2[0] - vec_1[0] * vec_2[2]
    z = vec_1[0] * vec_2[1] - vec_1[1] * vec_2[0]

    d = ((coord_1[0] * x) + (coord_1[1] * y) + (coord_1[2] * z))
    plane_eqn = [x, y, z, d]

    return [coord_1, coord_2, coord_3, plane_eqn]




def vector_in_plane(plane, vector):

    #projects a vector onto a given plane

    normal = plane[:3]

    normal_mod_sqrd = sum(map(lambda a: a**2, normal))

    vector_mod_sqrd = sum(map(lambda a: a**2, vector))

    normal = map(lambda a: a / normal_mod_sqrd, normal)

    normal_vector_prod = sum(map(lambda a, b: a * b, normal, vector))

    coeff = normal_vector_prod / vector_mod_sqrd

    vec_in_plane = map(lambda a, b: a - b, vector, map(lambda c: coeff * c, normal))


    return vec_in_plane



def inv_eqn(equation):

    if equation[0] != 0.0 and equation[0] != None:

        grad = 1 / equation[0]

        const = - equation[1] * grad

    else:

        grad = None

        const = equation[1]

    return [grad, const]




def plane_intersect(plane, eqns):

    #Calculates the point of intersection between a plane and a line and returns the coords of this point
    Error_val = 0.01

    # dy/dx = eqns[0][0]
    # dz/dx = eqns[1][0]
    # dy/dz = eqns[2][0]

    c = eqns[0][1]
    b = eqns[1][1]
    a = eqns[2][1]

    px = plane[0]
    py = plane[1]
    pz = plane[2]
    D = plane[3]

    point = [None, None, None]
    point_check = []
    #eqns_2 = eqns[:]

    # 1st test to see if any lines equations are of form y = constant

    for i in range(0, len(eqns)):

        if eqns[i][0] == None:

            if i != 1:

                point[i] = eqns[i][1]

        elif eqns[i][0] == 0.0:

            if i == 0:

                point[1] = eqns[i][1]

            elif i == 1:

                point[2] = eqns[i][1]

            elif i == 2:

                point[1] = eqns[i][1]

    #print 'initial coords = ', point


    # 2nd test to see if the plane is of the form y = constant (i.e. if plane is perpendicular to an axis)

    for i in range(0, len(plane) - 2):

        #print 'blah ' + ' ' + str(i) + ' ' + str(plane[i])

        for k in range(1, len(plane) - 1):

            #print 'blah ' + ' ' + str(k) + ' ' + str(plane[k])

            if plane[i] == 0.0 and plane[k] == 0.0 and i != k:

                index = 3 - i - k

                p = plane[3] / plane[index]

                #print 'blah 2'

                if point[index] == None:

                    point[index] = p

                elif point[index] != None:

                    #print 'checking now'

                    if abs(point[index] - p) > Error_val:

                        point[index] = False


    #print 'initial coords 2 = ', point


    # Check how many coords calculated so far
    while True:

        try:

            ind = point.index(False)

            if type(point[ind]) == bool:

                unfound = True

        except ValueError:

            unfound = False

            break

        else:

            break

    #print unfound

    if unfound == False:

        for i in range(0, len(point)):

            if point[i] != None:

                point_check.append(i)


        # Calculate the rest of the coordinates

        if len(point_check) == 0:

            for i in range(0, len(point) - 1):

                for k in range(1, len(point)):

                    if i != k:

                        index = 3 - i - k

                        eqn_0 = eqns[0]
                        eqn_1 = eqns[1]

                        if index == 1:

                            eqn_0 = inv_eqn(eqns[0])
                            eqn_1 = inv_eqn(eqns[2])

                        elif index == 2:

                            eqn_0 = inv_eqn(eqns[1])
                            eqn_1 = eqns[2]

                        point[index] = plane[3] - plane[i] * eqn_0[1] - plane[k] * eqn_1[1]

                        point[index] /= (plane[index] + plane[i] * eqn_0[0] + plane[k] * eqn_1[0])



        elif len(point_check) == 1:

            index = point_check[0]

            if index == 0:

                i, k = 1, 2

                eqn_0 = eqns[2]
                eqn_1 = inv_eqn(eqns[2])

            elif index == 1:

                i, k = 0, 2

                eqn_0 = inv_eqn(eqns[1])
                eqn_1 = eqns[1]

            elif index == 2:

                i, k = 0, 1

                eqn_0 = inv_eqn(eqns[0])
                eqn_1 = eqns[0]


            if plane[i] != 0.0 or plane[k] != 0.0:

                point[i] = plane[3] - plane[index] * point[index] - plane[k] * eqn_1[1]

                point[i] /= (plane[i] + plane[k] * eqn_1[0])

                point[k] = plane[3] - plane[index] * point[index] - plane[i] * eqn_0[1]

                point[k] /= (plane[k] + plane[i] * eqn_0[0])

            else:

                if index == 0:

                    i, k = 1, 2

                    eqn_0 = eqns[0]
                    eqn_1 = eqns[1]

                elif index == 1:

                    i, k = 0, 2

                    eqn_0 = inv_eqn(eqns[0])
                    eqn_1 = inv_eqn(eqns[2])

                elif index == 2:

                    i, k = 0, 1

                    eqn_0 = inv_eqn(eqns[1])
                    eqn_1 = eqns[2]

                point[i] = eqn_0[0] * point[index] + eqn_0[1]
                point[k] = eqn_1[0] * point[index] + eqn_1[1]



        elif len(point_check) == 2:

            index = 3 - sum(point_check)

            i, k = point_check

            if index == 0:

                eqn_0 = inv_eqn(eqns[0])
                eqn_1 = inv_eqn(eqns[1])


            elif index == 1:

                eqn_0 = eqns[0]
                eqn_1 = eqns[2]


            elif index == 2:

                eqn_0 = eqns[1]
                eqn_1 = inv_eqn(eqns[2])

            if eqn_0[0] != None:

                point[index] = point[i] * eqn_0[0] + eqn_0[1]

                #print 'i', i, eqn_0

            elif eqn_1[0] != None:

                point[index] = point[k] * eqn_1[0] + eqn_1[1]

                #print 'k', k, eqn_1

        while True:

            try:

                D = sum(map(lambda a, b: a * b, point, plane[:-1]))

                if abs(D - plane[3]) > Error_val:

                    point = None

            except TypeError:

                point = None

                break

            else:

                break

    else:

        point = None



    #print 'plane = ', plane
    #print 'equations = ', eqns
    #print 'final coords = ', point

    #print ' '

    return point




def point_distance(vert_1, vert_2):

    distance = 0

    for n in range(0, len(vert_1)):

        distance += ( vert_1[n] - vert_2[n] ) **2

    distance = math.sqrt(distance)

    return(distance)



def face_find(data, vert_1_no, vert_2_no, i):

    joined = []
    joined_faces = []

    for n in range(0, len(data[2])):

        if i != n:

            while True:

                try:

                    data[2][n].index(vert_1_no + 1)
                    joined.append(n+1)


                except ValueError:

                    break

                except IndexError:

                    break

                else:

                    break


    for m in range(0, len(joined)):

        while True:

                try:

                    data[2][joined[m] - 1].index(vert_2_no + 1)
                    joined_faces.append(joined[m])



                except ValueError:

                    break

                except IndexError:

                    break

                else:

                    break

    return(joined_faces)




def find_vert(eqns, vert_no):

    for y in range(0, len(eqns)):

        while True:

            try:

                x = eqns[y].index(vert_no)
                location = y

            except AttributeError:

                break

            except ValueError:

                break

            else:

                break

    return location




def two_plane_intersection(plane_1, plane_2):

    #function to calculate the line of intersection between two planes in the form mx + ny +oz + D = 0

    x1, y1, z1, D1 = map(lambda a: float(a),[plane_1[0], plane_1[1], plane_1[2], plane_1[3]])
    x2, y2, z2, D2 = map(lambda a: float(a),[plane_2[0], plane_2[1], plane_2[2], plane_2[3]])

    # find 1st intersection point
    #let y = 0

    p1, p2 = [], []

    px1 = (z2 * D1 - z1 * D2) / (x2 * z1 - x1 * z2)

    py1 = float(0)

    pz1 = (x1 * D2 - x2 * D1) / (x2 * z1 - x1 * z2)

    p1 = [px1, py1, pz1]

    # find 2nd intersection point
    # let z = 0

    px2 = (y2 * D1 - y1 * D2) / (x2 * y1 - x1 * y2)

    py2 = (x1 * D2 - x2 * D1) / (x2 * y1 - x1 * y2)

    pz2 = float(0)

    # Need to add condition x = 0 incase line does not pass through xy or xz plane

    # Need to add while condition incase division by zero


    m = (py1 - py2) / (px1 - px2)
    c = py1 - m * px1

    n = (pz1 - pz2) / (px1 - px2)
    b = pz1 - n * px1

    o = (py1 - py2) / (pz1 - pz2)
    a = py1 - o * pz1

    eqn_xy = [m, c]
    eqn_xz = [n, b]
    eqn_zy = [o, a]

    return([eqn_xy, eqn_xz, eqn_zy])




def attached_faces(equations, data):

    #function creates a list of all faces attached directly to a particular plane

    faces = []
    planes = calc_planes(data)

    for i in range(0, len(data[2])):

        vert_1_no = data[2][i][0] - 1
        vert_2_no = data[2][i][1] - 1
        vert_3_no = data[2][i][2] - 1


        vert_1 = data[1][vert_1_no]
        vert_2 = data[1][vert_2_no]
        vert_3 = data[1][vert_3_no]

        centre_point = map(lambda a, b, c: (a + b + c) / 3, vert_1, vert_2, vert_3)

        point_1 = map(lambda a, b: (a + b) / 2, vert_1, vert_2)
        point_2 = map(lambda a, b: (a + b) / 2, vert_2, vert_3)
        point_3 = map(lambda a, b, c: (a + b) / 2 + c , point_1, point_2, equations[i][4])

        plane_1 = plane_cutter(point_1, point_2, point_3)

        joined_faces  = []

        face_1 = face_find(data, vert_1_no, vert_2_no, i)
        face_2 = face_find(data, vert_2_no, vert_3_no, i)

        if len(face_1) > 0 :

            joined_faces.append([face_1[0]])

            joined_faces[0].append([point_1, vert_1_no + 1, vert_2_no + 1, True])

            if len(face_2) > 0:

                joined_faces.append([face_2[0]])

                joined_faces[1].append([point_2, vert_2_no + 1, vert_3_no + 1, True])

            else:
                joined_faces.append([i + 1])

                joined_faces[1].append([point_2, vert_2_no + 1, vert_3_no + 1, False])


            joined_faces.append(plane_1[3])


        else:

            if len(face_1) < 1:

                joined_faces.append([i + 1])

                joined_faces[0].append([point_1, vert_1_no + 1, vert_2_no + 1, False])

                if len(face_2) > 0:

                    joined_faces.append([face_2[0]])

                    joined_faces[1].append([point_2, vert_2_no + 1, vert_3_no + 1, True])


                joined_faces.append(plane_1[3])



        '''for n in joined_faces:

            index_1 = find_vert(equations[n-1], vert_1_no)
            point_4 = plane_intersect(plane_1, equations[n - 1][index_1])'''

        faces.append(joined_faces)


    return(faces)



def index_verts(equations, face, vert):


    for n in range(1, len(equations[face])-1):

        while True:

            try:
                equations[face][n].index(vert)
                place = n
            except ValueError:

                break

            except UnboundLocalError:

                break

            else:

                break

    return(place)



def line_intersection(line_1, line_2):

    #function to calculate the point of intersect between two given lines and return the coords

    m1, c1 = line_1[0]
    m2, c2 = line_2[0]
    n1, b1 = line_1[1]
    n2, b2 = line_2[1]
    o1, a1 = line_1[2]
    o2, a2 = line_2[2]

    if m1 and m2 != None:

        x = (c2 - c1) / (m1 - m2)

        y = m1 * x + c1

    else:

        if m1 == None and m2 != None:

            x = c1
            y = m2 * x + c2

        elif m2 == None and m1 != None:

            x = c2
            y = m1 * x + c1



    if o1!= None and o2 != None:

        z = (a2 - a1) / (o1 - o2)

    elif o1!= None or o2 != None and m1 == None or m2 == None:

        if o1 == None:

            z = a1

            y = o2 * z + a2

        elif o2 == None:

            z = a2

            y = o1 * z + a1



    return [x, y, z]



def check_equation(point, eqn):

    #test function to see if the line equation is correct using a set of coordinates

    error_val = 0.005

    m1, c1 = eqn[0]

    n1, b1 = eqn[1]

    o1, a1 = eqn[2]

    x, y, z = point

    check_xy = m1 * x + c1 - y

    if error_val > check_xy or check_xy > -error_val:

        test1 = True

    else:

        test1 = False

    check_xz = n1 * x + b1 - z

    if error_val > check_xz or check_xz > -error_val:

        test2 = True

    else:

        test2 = False

    check_zy = o1 * z + a1 - y

    if error_val >  check_zy or check_zy > -error_val:

        test3 = True

    else:

        test3 = False


    if test1 and test2 and test3 == True:

        is_on_line = True

    else:

        is_on_line = False

    return is_on_line





def vector_ang(vec_1, vec_2):

    #function to calculate the angle between two vectors
    #While loop added due to value error generated in two vectors were the same but float nums

    while True:

        try:

            dot_prod = sum(map(lambda a, b: a * b, vec_1, vec_2))
            mod_vec_1 = math.sqrt(sum(map(lambda c: c**2, vec_1)))
            mod_vec_2 = math.sqrt(sum(map(lambda c: c**2, vec_2)))
            cos_ang_1 = dot_prod / (mod_vec_1 * mod_vec_2)
            ang_1 = math.degrees(math.acos(cos_ang_1))

        except ValueError:

            ang_1 = 0.0

            break

        else:

            break

    return(ang_1)


def angle_check(normal_angle, vector_angle, normal):

    sum_angles = normal_angle + vector_angle

    if abs(180 - sum_angles) > abs(vector_angle - normal_angle):

        normal_angle = 180 - normal_angle

        normal = map(lambda a: -a, normal)

    return normal_angle, normal



def correct_normals(data):

    eqns = equations(data)

    eqns_2 = copy.deepcopy(eqns)

    plane_eqns = calc_planes(data)

    connected = attached_faces(eqns, data)

    vectors = []

    points = []

    angles = []

    for i in range(0, len(connected)):

        #plane_1 is the plane that the normal to face i lies in and runs through p1_2 & p1_3
        plane_1 = connected[i][-1:][0]

        if connected[i][0][1][3] == True and connected[i][1][1][3] == True:

            face_2 = connected[i][0][0]-1
            verts_2 = connected[i][0][1][1:]
            plane_2 = plane_eqns[face_2][1]

            line_eqn_1_1 = two_plane_intersection(plane_1, plane_2)

            place_1 = [data[2][face_2].index(verts_2[0]), data[2][face_2].index(verts_2[1])]

            face_3 = connected[i][1][0] - 1
            verts_3 = connected[i][1][1][1:]
            plane_3 = plane_eqns[face_3][1]

            line_eqn_2_1 = two_plane_intersection(plane_1, plane_3)

            place_2 = [data[2][face_3].index(verts_3[0]), data[2][face_3].index(verts_3[1])]


        elif connected[i][0][1][3] == False and connected[i][1][1][3] == True:

            face_2 = connected[i][1][0]-1
            verts_2 = connected[i][1][1][1:]
            plane_2 = plane_eqns[face_2][1]

            line_eqn_1_1 = two_plane_intersection(plane_1, plane_2)

            place_1 = [data[2][face_2].index(verts_2[0]), data[2][face_2].index(verts_2[1])]


        elif connected[i][0][1][3] == True and connected[i][1][1][3] == False:

            face_2 = connected[i][0][0]-1
            verts_2 = connected[i][0][1][1:]
            plane_2 = plane_eqns[face_2][1]

            line_eqn_1_1 = two_plane_intersection(plane_1, plane_2)

            place_1 = [data[2][face_2].index(verts_2[0]), data[2][face_2].index(verts_2[1])]



                # print place_1

        if connected[i][0][1][3] == True and connected[i][1][1][3] == True:

            p1_2 = connected[i][0][1][0]

            p1_3 = connected[i][1][1][0]

            # If condition below chooses the 2 possible line equation depending on the index of the vertices


            if 0 in place_1:

                if 1 in place_1:

                    # print '0'

                    line_eqn_1_2_1 = eqns[face_2][2][2]
                    line_eqn_1_2_2 = eqns[face_2][3][2]


                elif 2 in place_1:

                    # print '1'

                    line_eqn_1_2_1 = eqns[face_2][1][2]
                    line_eqn_1_2_2 = eqns[face_2][2][2]


            else:

                # print '2'

                line_eqn_1_2_1 = eqns[face_2][1][2]
                line_eqn_1_2_2 = eqns[face_2][3][2]

            # print line_eqn_1_2

            if 0 in place_2:

                if 1 in place_2:

                    # print '0'

                    line_eqn_2_2_1 = eqns[face_3][2][2]
                    line_eqn_2_2_2 = eqns[face_3][3][2]


                elif 2 in place_2:

                    # print '1'

                    line_eqn_2_2_1 = eqns[face_3][1][2]
                    line_eqn_2_2_2 = eqns[face_3][2][2]


            else:

                # print '2'

                line_eqn_2_2_1 = eqns[face_3][1][2]
                line_eqn_2_2_2 = eqns[face_3][3][2]


        elif connected[i][0][1][3] == False and connected[i][1][1][3] == True:

            p1_2 = connected[i][1][1][0]

            p1_3 = connected[i][0][1][0]

            if 0 in place_1:

                if 1 in place_1:

                    # print '0'

                    line_eqn_1_2_1 = eqns[face_2][2][2]
                    line_eqn_1_2_2 = eqns[face_2][3][2]


                elif 2 in place_1:

                    # print '1'

                    line_eqn_1_2_1 = eqns[face_2][1][2]
                    line_eqn_1_2_2 = eqns[face_2][2][2]


            else:

                    # print '2'

                    line_eqn_1_2_1 = eqns[face_2][1][2]
                    line_eqn_1_2_2 = eqns[face_2][3][2]


        elif connected[i][0][1][3] == True and connected[i][1][1][3] == False:

            p1_2 = connected[i][0][1][0]

            p1_3 = connected[i][1][1][0]

            if 0 in place_1:

                if 1 in place_1:

                    # print '0'

                    line_eqn_1_2_1 = eqns[face_2][2][2]
                    line_eqn_1_2_2 = eqns[face_2][3][2]


                elif 2 in place_1:

                    # print '1'

                    line_eqn_1_2_1 = eqns[face_2][1][2]
                    line_eqn_1_2_2 = eqns[face_2][2][2]


            else:

                # print '2'

                line_eqn_1_2_1 = eqns[face_2][1][2]
                line_eqn_1_2_2 = eqns[face_2][3][2]


        #

        if connected[i][0][1][3] == True and connected[i][1][1][3] == True:

            p2_1 = line_intersection(line_eqn_1_1, line_eqn_1_2_1)

            p2_2 = line_intersection(line_eqn_1_1, line_eqn_1_2_2)

            if check_equation(p2_1, line_eqn_1_1) == True:

                p2 = p2_1

                line_eqn_1_2 = line_eqn_1_2_1

            elif check_equation(p2_2, line_eqn_1_1) == True:

                p2 = p2_2

                line_eqn_1_2 = line_eqn_1_2_2


            p3_1 = line_intersection(line_eqn_2_1, line_eqn_2_2_1)

            p3_2 = line_intersection(line_eqn_2_1, line_eqn_2_2_2)

            if check_equation(p3_1, line_eqn_2_1) == True:

                p3 = p3_1

                line_eqn_2_2 = line_eqn_2_2_1

            elif check_equation(p3_2, line_eqn_2_1) == True:

                p3 = p3_2

                line_eqn_2_2 = line_eqn_2_2_2


        else:

            p2_1 = line_intersection(line_eqn_1_1, line_eqn_1_2_1)

            p2_2 = line_intersection(line_eqn_1_1, line_eqn_1_2_2)

            if check_equation(p2_1, line_eqn_1_1) == True:

                p2 = p2_1

                line_eqn_1_2 = line_eqn_1_2_1

            elif check_equation(p2_2, line_eqn_1_1) == True:

                p2 = p2_2

                line_eqn_1_2 = line_eqn_1_2_2




        # print p2_1, p2_2, face_2, p1_2

        face_2_no = face_2 + 1
        face_3_no = face_3 + 1




        if connected[i][0][1][3] == True:

            vec_1_2 = map(lambda a, b: a - b, p1_3, p1_2)

            vec_2 = map(lambda a, b: a - b, p2, p1_2)

            normal_1 = eqns[i][4]

            normal_2 = vector_in_plane(plane_1, eqns[face_2][4])

            angle_1 = vector_ang(normal_1, normal_2)

            angle_1_1 = vector_ang(vec_1_2, vec_2)

            angle_1_2 = vector_ang(vec_2, normal_2)

            angle_1_3 = vector_ang(vec_1_2, normal_1)

            angle_1, eqns_2[face_2][4] = angle_check(angle_1, angle_1_1, normal_2)

            vectors_1 = [face_2_no, vec_1_2, vec_2]


            if connected[i][1][1][3] == True:

                vec_1_3 = map(lambda a, b: a - b, p1_2, p1_3)

                vec_3 = map(lambda a, b: a - b, p3, p1_3)

                vectors_2 = [face_3_no, vec_1_3, vec_3]

                normal_3 = vector_in_plane(plane_1, eqns[face_3][4])

                angle_2 = vector_ang(normal_1, normal_3)

                angle_2_1 = vector_ang(vec_1_3, vec_3)

                angle_2_2 = vector_ang(vec_3, normal_3)

                angle_2_3 = vector_ang(vec_1_3, normal_1)

                angle_2, eqns_2[face_3][4] = angle_check(angle_2, angle_2_1, normal_3)


                vectors.append([vectors_1, vectors_2])

                points.append([[face_2_no, p1_2, p2, line_eqn_1_1, line_eqn_1_2], [face_3_no, p1_3, p3, line_eqn_2_1, line_eqn_2_2]])

                angles.append([[face_2_no, angle_1, angle_1_1, angle_1_2, angle_1_3], [face_3_no, angle_2, angle_2_1, angle_2_2, angle_2_3]])

            elif connected[i][1][1][3] == False:

                vectors.append([vectors_1])

                points.append([[face_2_no, p1_2, p2, p1_3, line_eqn_1_1, line_eqn_1_2]])

                angles.append([[face_2_no, angle_1, angle_1_1, angle_1_2, angle_1_3]])



        elif connected[i][0][1][3] == False:

            vec_1_2 = map(lambda a, b: a - b, p1_3, p1_2)

            vec_2 = map(lambda a, b: a - b, p2, p1_2)

            normal_1 = eqns[i][4]

            normal_2 = vector_in_plane(plane_1, eqns[face_2][4])

            angle_1 = vector_ang(normal_1, normal_2)

            angle_1_1 = vector_ang(vec_1_2, vec_2)

            angle_1_2 = vector_ang(vec_2, normal_2)

            angle_1_3 = vector_ang(vec_1_2, normal_1)

            angle_1, eqns_2[face_2][4] = angle_check(angle_1, angle_1_1, normal_2)



            vectors_1 = [face_2_no, vec_1_2, vec_2]

            vectors.append([vectors_1])

            points.append([[face_2_no, p1_2, p2, p1_3, line_eqn_1_1, line_eqn_1_2]])

            angles.append([[face_2_no, angle_1, angle_1_1, angle_1_2, angle_1_3]])



    return(vectors, points, angles, eqns_2)






def intersect(coord_1, coord_2, data, aligned_plane):

    global int_faces

    int_faces = []

    eqns = equations(data)

    if len(aligned_plane) == 0:

        coord_3 = map(lambda a, b: a + b, coord_1, [0.0, 10.0, 0.0])
        plane = plane_cutter(coord_1, coord_2, coord_3)[3]

    else:

        plane = aligned_plane

    #vec_1_2 = map(lambda a, b: a - b, coord_2, coord_1)

    intersecting = []

    #print plane, coord_1, coord_2

    for i in range(0, len(eqns)):

        int_points = []

        for n in range(1, len(eqns[i]) - 1):

            point_1 = plane_intersect( plane, eqns[i][n][2] )

            face = eqns[i][0]

            if point_1 != None:

                vert_no = eqns[i][n][0]

                vert_1 = data[1][vert_no - 1]

                intersecting = []

                if n < 3:
                    next_vert = eqns[i][n + 1][0] - 1

                    vert_2 = data[1][next_vert]

                else:

                    next_vert = eqns[i][n - 2][0] - 1

                    vert_2 = data[1][next_vert]


                #print point_1, face, vert_no, next_vert


                vec_c1_p1 = map(lambda a, b: a - b, point_1, coord_1)

                vec_c1_c2 = map(lambda a, b: a - b, coord_2, coord_1)

                vec_c1_c2_p1 = map(lambda a, b: a - b, vec_c1_c2, vec_c1_p1)





                for m in range(0, len(vert_1)):

                    if vec_c1_c2[m] >= vec_c1_p1[m] >= 0.0 or vec_c1_c2[m] <= vec_c1_p1[m] <= 0.0:

                        if vert_1[m] <= point_1[m] <= vert_2[m] or vert_1[m] >= point_1[m] >=  vert_2[m]:

                            intersecting.append(True)


                        else:

                            intersecting.append(False)

                    else:

                        intersecting.append(False)

                #print intersecting, vert_no, next_vert + 1, point_1


                if intersecting[0] == True and intersecting[2] == True:

                    int_points.append([vert_no, next_vert + 1, point_1])

                #print vert_no, point_1

        if len(int_points) > 1:

            int_faces.append([i + 1, int_points])

    #print int_faces

    return int_faces, plane#, intersecting



def align_plane(int_faces, plane, data, coord1, coord2):

    global verts_above, verts_below, centre_above, centre_below, normal_to_plane, centre_p, norm_vec_aligned

    verts_above = []

    verts_below = []

    c1, c2 = coord1, coord2

    normal_to_plane = plane[0:3]

    mod_norm = math.sqrt(sum(map(lambda a: a**2, normal_to_plane)))

    normal_to_plane = map(lambda a: a / mod_norm, normal_to_plane)

    for i in range(0, len(int_faces)):

        for n in range(0, len(int_faces[i][1])):

            for k in range(0, len(int_faces[i][1][n]) - 1):

                vert_no = int_faces[i][1][n][k] - 1

                vert = data[1][vert_no]

                cut_p = int_faces[i][1][n][-1]

                vec = map(lambda a, b: a - b, vert, cut_p)

                dot_prod = sum(map(lambda a, b: a * b, normal_to_plane, vec))

                if dot_prod > 0:

                    verts_above.append(vert)

                elif dot_prod < 0:

                    verts_below.append(vert)


    centre_above = calc_centre(verts_above)

    centre_below = calc_centre(verts_below)

    line_eqn = calc_line_eqn_2(centre_above, centre_below)

    centre_p = plane_intersect(plane, line_eqn)

    norm_vec_aligned = map(lambda a, b: a - b, centre_above, centre_p)

    plane = plane_from_vector(norm_vec_aligned, centre_p)

    line_eqn_c1 = calc_line_eqn(norm_vec_aligned, c1)
    line_eqn_c2 = calc_line_eqn(norm_vec_aligned, c2)

    c1 = plane_intersect(plane, line_eqn_c1)
    c2 = plane_intersect(plane, line_eqn_c2)

    return plane, c1, c2






def calc_measurement(int_faces):

    # int_faces is a list of faces generated by the intersect function

    measurement = 0

    while True:

        try:

            for i in range(0, len(int_faces)):

                point_1 = int_faces[i][1][0][2]

                point_2 = int_faces[i][1][1][2]

                measurement += point_distance(point_1, point_2)

        except IndexError:

            break

        else:

            break

    return(measurement)





def vector_length(vector):

    vec_length = math.sqrt(sum(map(lambda x: x**2, vector)))

    return(vec_length)


def sum_vectors(vec_1, vec_2):

    vec_sum = map(lambda a, b: a + b, vec_1, vec_2)

    return(vec_sum)



def final_norm(line_length, vert_to_cut_point, offset):

    #Function to calculate the amount to move the vertex at each end of the line

    tan_ang_1 = offset / line_length

    c1 = vert_to_cut_point

    c = line_length

    #Scalar movement amount perpendicular to the connecting the 2 vertices

    perp_norm_scal_1 = offset +  c1 * (1 - 2 * c1 / c)**2 * tan_ang_1

    perp_norm_scal_2 = offset - (c - c1) * (perp_norm_scal_1 - offset) /c1


    return perp_norm_scal_1, perp_norm_scal_2




def normal_move_calc(total_length, move_dist, l_1):

    #function to calculate the distance to move the vertex perpendicular to the line between it and a connected point

    total_length, move_dist, l_1 = map(float, (total_length, move_dist, l_1))

    tan_ang_1 = move_dist / total_length

    vert_1_dist = move_dist + l_1 * (1 - (2 * (l_1 / total_length))) * tan_ang_1

    vert_2_dist = move_dist - (total_length - l_1) * ((vert_1_dist - move_dist) / l_1)

    vert_1_dist = vert_1_dist ** 2 / move_dist
    vert_2_dist = vert_2_dist ** 2 / move_dist

    return [vert_1_dist, vert_2_dist]



def plane_from_vector(vector, vert_1):

    #Calculates the plane equation perpendicular to a vector passing through a vertex

    x, y, z = vector

    d = ((vert_1[0] * x) + (vert_1[1] * y) + (vert_1[2] * z))

    plane_eqn = [x, y, z, d]

    return plane_eqn




def move_vertices(int_faces, plane_eqn, measurement_2, data):


    face_eqns = equations(data)

    #int_faces, plane_eqn = intersect(coord_1, coord_2, data)

    plane_eqn = plane_eqn[-1]

    measurement_1 = calc_measurement(int_faces)

    ratio = measurement_2 / measurement_1

    delta_l = measurement_2 - measurement_1

    delta_h, delta_tan_ang, sum_ang = 0.0, 0.0, 0.0

    offset_calc = {'faces':{}}

    angles, lines, normals, move_scale, offset, moved = {}, {}, {}, {}, {}, {}

    move_vecs = {'vectors' : {}, 'numbers' : {}}

    test_dist = delta_l / len(int_faces)

    for i in range(0, len(int_faces)):

        vert_1_no = int_faces[i][1][0][0]

        vert_2_no = int_faces[i][1][0][1]

        vert_3_no = int_faces[i][1][1][0]

        vert_4_no = int_faces[i][1][1][1]

        move_vecs['vectors'][str(vert_1_no)] = [0.0, 0.0, 0.0]
        move_vecs['vectors'][str(vert_2_no)] = [0.0, 0.0, 0.0]
        move_vecs['vectors'][str(vert_3_no)] = [0.0, 0.0, 0.0]
        move_vecs['vectors'][str(vert_4_no)] = [0.0, 0.0, 0.0]

        move_vecs['numbers'][str(vert_1_no)] = 0
        move_vecs['numbers'][str(vert_2_no)] = 0
        move_vecs['numbers'][str(vert_3_no)] = 0
        move_vecs['numbers'][str(vert_4_no)] = 0

    for i in range(0, len(int_faces)):

        #offset_calc = {}

        face = int_faces[i][0]

        face_norm = face_eqns[face - 1][4]

        vert_1_no = int_faces[i][1][0][0]

        vert_2_no = int_faces[i][1][0][1]

        vert_3_no = int_faces[i][1][1][0]

        vert_4_no = int_faces[i][1][1][1]



        vert_1 = data[1][vert_1_no - 1]

        vert_2 = data[1][vert_2_no - 1]

        vert_3 = data[1][vert_3_no - 1]

        vert_4 = data[1][vert_4_no - 1]


        vector_1_2 = map(lambda a, b: a - b, vert_2, vert_1)

        vector_3_4 = map(lambda a, b: a - b, vert_4, vert_3)


        point_1 = int_faces[i][1][0][2]

        point_2 = int_faces[i][1][1][2]

        #vector connecting the two points cutting through the face

        l_1 = map(lambda a, b: a - b, point_2, point_1)

        l_2 = map(lambda a, b: a - b, point_1, point_2)

        length_1 = vector_length(l_1)


        d_p1_v1 = point_distance(vert_1, point_1)

        d_p2_v3 = point_distance(vert_3, point_2)

        d_1_2 = point_distance(vert_1, vert_2)

        d_3_4 = point_distance(vert_3, vert_4)


        av_norm_1 = avg_normal((vert_1_no), data, face_eqns)

        av_norm_2 = avg_normal((vert_2_no), data, face_eqns)

        av_norm_3 = avg_normal((vert_3_no), data, face_eqns)

        av_norm_4 = avg_normal((vert_4_no), data, face_eqns)


        #calculate the planes perpendicular to the lines connecting vertices:

        plane_1 = plane_from_vector(vector_1_2, vert_1)
        plane_2 = plane_from_vector(vector_1_2, vert_2)
        plane_3 = plane_from_vector(vector_3_4, vert_3)
        plane_4 = plane_from_vector(vector_3_4, vert_4)

        # project each normal onto its corresponding perpendiculr plane

        av_norm_to_plane_1 = vector_in_plane(plane_1, av_norm_1)
        av_norm_to_plane_2 = vector_in_plane(plane_2, av_norm_2)
        av_norm_to_plane_3 = vector_in_plane(plane_3, av_norm_3)
        av_norm_to_plane_4 = vector_in_plane(plane_4, av_norm_4)

        ang_1_V = math.radians(vector_ang(av_norm_to_plane_1, av_norm_1))
        ang_2_V = math.radians(vector_ang(av_norm_to_plane_2, av_norm_2))
        ang_3_V = math.radians(vector_ang(av_norm_to_plane_3, av_norm_3))
        ang_4_V = math.radians(vector_ang(av_norm_to_plane_4, av_norm_4))


        ang_1_2 = math.radians(vector_ang(av_norm_to_plane_1, av_norm_to_plane_2))
        ang_3_4 = math.radians(vector_ang(av_norm_to_plane_3, av_norm_to_plane_4))

        norm_ang_1_2 = math.radians(vector_ang(av_norm_to_plane_1, face_norm))
        norm_ang_3_4 = math.radians(vector_ang(av_norm_to_plane_3, face_norm))

        cut_ang_1_2 = (d_p1_v1 / d_1_2) * ang_1_2
        cut_ang_3_4 = (d_p2_v3 / d_3_4) * ang_3_4


        m1, m2 = normal_move_calc(d_1_2, test_dist, d_p1_v1)
        m3, m4 = normal_move_calc(d_3_4, test_dist, d_p2_v3)

        m1 = (m1 / math.cos(cut_ang_1_2)) * math.cos(ang_1_V)
        m2 = (m2 / math.cos(ang_1_2 - cut_ang_1_2)) * math.cos(ang_2_V)
        m3 = (m3 / math.cos(cut_ang_3_4)) * math.cos(ang_3_V)
        m4 = (m4 / math.cos(ang_3_4 - cut_ang_3_4)) * math.cos(ang_4_V)


        m1_vec = map(lambda a: a * m1, av_norm_1)
        m2_vec = map(lambda a: a * m2, av_norm_2)
        m3_vec = map(lambda a: a * m3, av_norm_3)
        m4_vec = map(lambda a: a * m4, av_norm_4)


        move_vecs['vectors'][str(vert_1_no)] = map(lambda a, b: a + b, move_vecs['vectors'][str(vert_1_no)], m1_vec)
        move_vecs['vectors'][str(vert_2_no)] = map(lambda a, b: a + b, move_vecs['vectors'][str(vert_2_no)], m2_vec)
        move_vecs['vectors'][str(vert_3_no)] = map(lambda a, b: a + b, move_vecs['vectors'][str(vert_3_no)], m3_vec)
        move_vecs['vectors'][str(vert_4_no)] = map(lambda a, b: a + b, move_vecs['vectors'][str(vert_4_no)], m4_vec)

        move_vecs['numbers'][str(vert_1_no)] += 1
        move_vecs['numbers'][str(vert_2_no)] += 1
        move_vecs['numbers'][str(vert_3_no)] += 1
        move_vecs['numbers'][str(vert_4_no)] += 1

        angles['face ' + str(face)] = {}
        angles['face ' + str(face)]['vert ' + str(vert_1_no)] = {'av norm': av_norm_1, 'av norm in plane': av_norm_to_plane_1}
        angles['face ' + str(face)]['vert ' + str(vert_2_no)] = {'av norm': av_norm_2, 'av norm in plane': av_norm_to_plane_2}
        angles['face ' + str(face)]['vert ' + str(vert_3_no)] = {'av norm': av_norm_3, 'av norm in plane': av_norm_to_plane_3}
        angles['face ' + str(face)]['vert ' + str(vert_4_no)] = {'av norm': av_norm_4, 'av norm in plane': av_norm_to_plane_4}




    for i, v in move_vecs['vectors'].items():

        vert_no = int(i)
        denominator = move_vecs['numbers'][str(vert_no)]
        move_vec = map(lambda a: a / denominator, move_vecs['vectors'][str(vert_no)])

        data[1][vert_no - 1] = sum_vectors(data[1][vert_no - 1], move_vec)


    return data




def rotate_data(coord, angle):

    angle = math.radians(angle)

    x1, y1, z1 = coord

    x2 = x1 * math.cos(angle) + y1 * math.sin(angle)

    y2 = x1 * math.sin(angle) - y1 * math.cos(angle)

    z2 = z1

    return [x2, y2, z2]



def delta_z(data): #Calculates the distance between heighest & lowest vertex

    delta_z_list = []

    for i in range(len(data[1])):
        delta_z_list.append(data[1][i][2])

    min_point = delta_z_list.index(min(delta_z_list))

    max_point = delta_z_list.index(max(delta_z_list))

    #return(min(delta_z_list), max(delta_z_list), min_point, max_point)

    del_z = max(delta_z_list) - min(delta_z_list)
    del_z_min = min(delta_z_list)

    return(del_z, del_z_min)

def delta_x(data): #Calculates the distance between heighest & lowest vertex

    delta_x_list = []

    for i in range(len(data[1])):
        delta_x_list.append(data[1][i][0])

    min_point = delta_x_list.index(min(delta_x_list))

    max_point = delta_x_list.index(max(delta_x_list))

    #return(min(delta_z_list), max(delta_z_list), min_point, max_point)

    del_x = max(delta_x_list) - min(delta_x_list)
    del_x_min = min(delta_x_list)

    return(del_x, del_x_min)


def calc_centre(data_verts):

    #calculates the centre point of all datapoints

    centre = [0.0, 0.0, 0.0]

    for i in range(0, len(data_verts)):

        centre = map(lambda a, b: a + b, centre, data_verts[i])

    centre = map(lambda a: a / len(data_verts), centre)

    return centre



def calc_face_centre(face, data):

    centre = [0.0, 0.0, 0.0]

    data_verts = data[2][face]

    for i in range(0, len(data_verts)):

        vert_no = data[2][face][i]
        vert = data[1][vert_no - 1]
        centre = map(lambda a, b: a + b, centre, vert)

    centre = map(lambda a: a / len(data_verts), centre)

    return centre




def screen_point_convertor(point, scale, min_z):

    point = map(float, point)

    point[0] = int(point[0] * scale + Screen_width / 2)

    point[2] = int( Screen_height / 2 - (point[2] - min_z) * scale  )

    del(point[1])

    return point


def data_point_screen_convertor(point, scale, min_z):

    point = map(float, point)

    point[0] = (point[0] - Screen_width / 2) / scale

    point.append(min_z + (Screen_height / 2 - point[1]) / scale)

    point[1] = 0.0

    return point


def sort_polygons(polygons):

    return polygons[2][1]






def draw_polygons(data, display, angle, centre_point, scale, min_z, show_face_no, show_av_norms, show_edges): #Draws the polygons of each face as different colours

    polygon_list = []

    #height = pygame.display.get_height()



    centre_point = rotate_data(centre_point, angle)

    #eqns_2 = correct_normals(data)[-1:][0]

    eqns_2 = equations(data)

    av_normals = []

    for i in range(0, len(data[1])):

        av_normal = avg_normal((i + 1), data, eqns_2)

        av_normals.append(av_normal)



    for i in range(0, len(data[2])):

        polygon = []

        face_no = i

        for n in range(0, len(data[2][i])):

            vert_no = data[2][i][n]

            points = rotate_data(data[1][(vert_no - 1)], angle)

            points = screen_point_convertor(points, scale, min_z)

            normals = eqns_2[i][4]

            normals = rotate_data(normals, angle)

            if normals[1] > 0.0:

                polygon.append(points)

        if len(polygon) > 2:

            polygon_center = calc_face_centre(face_no, data)
            polygon_center = rotate_data(polygon_center, angle)

            polygon_list.append([i, polygon, polygon_center])



        #colour = 100

    polygon_list = sorted(polygon_list, key = sort_polygons)

    for i in range(0, len(polygon_list)):

        polygon = polygon_list[i][1]

        face_no = polygon_list[i][0]

        if len(polygon) > 0:

            colour = int(255 * i / len(data[2]))

            pygame.draw.polygon(display, (255, 0 + colour, 255 - colour), polygon, 0)

            if show_face_no == True:

                polygon_center = calc_face_centre(face_no, data)
                polygon_center = rotate_data(polygon_center, angle)
                polygon_center = screen_point_convertor(polygon_center, scale, min_z)
                text2((face_no+1), polygon_center, (255, colour, 255 - colour))

            if show_edges == True:

                for k in range(0, len(polygon)):

                    if k == len(polygon) - 1:

                        pygame.draw.line(display, (0, 255, 0), polygon[k], polygon[0], 1)

                    else:

                        pygame.draw.line(display, (0, 255, 0), polygon[k], polygon[k+1], 1)




        if show_av_norms == True:

            for i in range(0, len(av_normals)):

                av_norm_rotated = rotate_data(av_normals[i], angle)

                if av_norm_rotated[1] >= 0:

                    p1 = data[1][i]
                    normal = map(lambda a: a * 30 / scale , av_normals[i])
                    p2 = map(lambda a, b: a + b, p1, normal)

                    p1 = rotate_data(p1, angle)
                    p1 = screen_point_convertor(p1, scale, min_z)

                    p2 = rotate_data(p2, angle)
                    p2 = screen_point_convertor(p2, scale, min_z)

                    pygame.draw.line(display, [0, 0, 255], p1, p2, 1)

    return scale, min_z, polygon_list


def draw_edges(data, display, angle, centre_point, show_av_norms, scale, min_z): #Draws the polygons of each face as different colours

    polygon_list = []

    centre_point = rotate_data(centre_point, angle)

    eqns_2 = equations(data)

    av_normals = []

    for i in range(0, len(data[1])):

        av_normal = avg_normal((i + 1), data, eqns_2)

        av_normals.append(av_normal)



    for i in range(0, len(data[2])):

        polygon = []

        for n in range(0, len(data[2][i])):

            vert_no = data[2][i][n]

            points = rotate_data(data[1][(vert_no - 1)], angle)

            points = screen_point_convertor(points, scale, min_z)

            normals = eqns_2[i][4]

            normals = rotate_data(normals, angle)

            if normals[1] > 0:

                polygon.append(points)

        colour = int(255 * i / len(data[2]))

        #colour = 100

        if len(polygon) > 0:

            for k in range(0, len(polygon)):

                if k == len(polygon) - 1:

                    pygame.draw.line(display, (255, 0 , 0), polygon[k], polygon[0], 1)

                else:

                    pygame.draw.line(display, (255, 0 , 0), polygon[k], polygon[k+1], 1)


        polygon_list.append(polygon)

        for i in range(0, len(av_normals)):

            av_norm_rotated = rotate_data(av_normals[i], angle)

            if show_av_norms == True and av_norm_rotated[1] > 0:

                p1 = data[1][i]
                normal = map(lambda a: a * 30 / scale , av_normals[i])
                p2 = map(lambda a, b: a + b, p1, normal)

                p1 = rotate_data(p1, angle)
                p1 = screen_point_convertor(p1, scale, min_z)

                p2 = rotate_data(p2, angle)
                p2 = screen_point_convertor(p2, scale, min_z)

                pygame.draw.line(display, [255, 0, 0], p1, p2, 2)




def cut_lines(points):

    if len(points) % 2 == 0:

        for i in range(0, len(points), 2):

            pygame.draw.line(DISPLAYSURF, (255, 50, 50), points[i], points[i + 1])

    else:

        for i in range(0, len(points) - 1, 2):

            pygame.draw.line(DISPLAYSURF, (255, 50, 50), points[i], points[i + 1])



def measurement_text(measurement):

    display = pygame.display.get_surface()

    measurement = int(measurement)

    measurement = str(measurement)

    fontobj = pygame.font.Font('freesansbold.ttf', 14)
    textobj = fontobj.render('Measurement = ' + measurement + ' mm', True, [100, 100, 255], [0, 0, 0])
    textsurf = textobj.get_rect()
    textsurf.topleft = ( (20), (20) )

    fontobj1 = pygame.font.Font('freesansbold.ttf', 14)
    textobj1 = fontobj1.render('Change Measurement', True, [100, 100, 255], [50, 50, 50])
    textsurf1 = textobj1.get_rect()
    textsurf1.topright = ( (Screen_width - 20), (20) )

    offset = [-5, -5, 5, 5]
    box = map(lambda a, b: a + b, offset, textsurf1)


    display.blit(textobj, textsurf)
    #pygame.draw.polygon(display, (255, 0, 255), box, 0)
    display.blit(textobj1, textsurf1)


def convert_list(list_1):

    #converts the input from the UI into an integer

    number = str(list_1).translate(None, ',')
    number = number.translate(None, ' ')
    number = number.translate(None, '[')
    number = number.translate(None, ']')

    number = int(number)

    return number


def measurement_text2(measurement, screen_coord):

    display = pygame.display.get_surface()

    measurement = str(measurement)

    fontobj = pygame.font.Font('freesansbold.ttf', 14)
    textobj = fontobj.render('New Measurement = ' + measurement + ' mm', True, [100, 100, 255], [0, 0, 0])
    textsurf = textobj.get_rect()
    textsurf.topleft = ( (20 + screen_coord[0]), (20 + screen_coord[1]) )

    display.blit(textobj, textsurf)


def text1(text, screen_coord):

    display = pygame.display.get_surface()

    text = str(map(int, text))



    fontobj = pygame.font.Font('freesansbold.ttf', 12)
    textobj = fontobj.render(text + ' mm', True, [100, 100, 255], [0, 0, 0])
    textsurf = textobj.get_rect()
    textsurf.topleft = ( (20 + screen_coord[0]), (20 + screen_coord[1]) )

    display.blit(textobj, textsurf)


def text2(text, screen_coord, colour):

    display = pygame.display.get_surface()

    text = str(text)

    fontobj = pygame.font.Font('freesansbold.ttf', 12)
    textobj = fontobj.render(text, True, [0, 0, 0], colour)
    textsurf = textobj.get_rect()
    textsurf.center = ( (screen_coord[0]), (screen_coord[1]) )

    display.blit(textobj, textsurf)


def text3(text, screen_coord, colour):

    display = pygame.display.get_surface()

    text = str(text)

    fontobj = pygame.font.Font('freesansbold.ttf', 12)
    textobj = fontobj.render(text, True, colour, [0, 0, 0])
    textsurf = textobj.get_rect()
    textsurf.topleft = ( (20 + screen_coord[0]), (20 + screen_coord[1]) )

    display.blit(textobj, textsurf)


def text4(text, screen_coord, colour):

    display = pygame.display.get_surface()

    if type(text) != 'str':

        text = str(text)


    fontobj = pygame.font.Font('freesansbold.ttf', 24)
    textobj = fontobj.render(text, True, colour, [0, 0, 0])
    textsurf = textobj.get_rect()
    textsurf.center = ( screen_coord[0], screen_coord[1] )

    display.blit(textobj, textsurf)



def quit_screen():

        text_pos = [int(Screen_width/2), int(Screen_height/2)]
        text4('Would you like to save the new model?', text_pos, [255, 50, 50])
        text_pos_2 = map(lambda a, b: a + b, text_pos, [0, 40])
        text4('Enter Y/N or C for cancel', text_pos_2, [255, 50, 50])



def quit_game(data, save):

    if save == True:

        op_file_new.write(str(data))
        op_file_new.close()

    pygame.quit()
    sys.exit()




def create_screen(centre_point):

    global data_list#, polygon_list, int_faces_1, points, coords, cut_plane, cut_plane_2

    data_list_2 = copy.deepcopy(data_list)


    DISPLAYSURF = pygame.display.set_mode((Screen_width, Screen_height), 0, 32)
    pygame.display.set_caption('BioDesic Pattern Fitter Version 2')
    pygame.key.set_repeat(50, 30)

    angle = 0
    points = []
    SHIFT = False
    CONTROL = False

    coords = []
    measurement_2 = 0.0
    measurement_list = [0]

    quit_scr = False
    quitting = False

    faces_vis = False
    norm_vis = False
    show_edges = False
    show_unedited = False
    align_to_plane = False
    plane_aligned = False
    int_faces_1 = []
    test_data = {}
    cut_plane_2 = []

    height = float(Screen_height * .95)

    width = float(Screen_width * .95)

    scale_z = height / delta_z(data_list_2)[0]

    scale_x = width / delta_x(data_list_2)[0]

    if scale_z < scale_x:

        scale = scale_z

    else:

        scale = scale_x

    min_z = delta_z(data_list_2)[1] + delta_z(data_list_2)[0] / 2

    while True:

        DISPLAYSURF.fill((0, 0, 0))

        scale, min_z, polygon_list = draw_polygons(data_list_2, DISPLAYSURF, angle, centre_point, scale, min_z, faces_vis, norm_vis, show_edges)

        clicked = False

        check_measurement = False

        if show_unedited == True:

            draw_edges(data_list, DISPLAYSURF, angle, centre_point, norm_vis, scale, min_z)

        if quit_scr == True:

            quit_screen()

        measurement_2 = convert_list(measurement_list)

        measurement_text2(measurement_2, [0, 20])

        if len(coords) > 0:

            text1(coords[-1], [0, 60])
            text1(coords[-2], [0, 40])

        for event in pygame.event.get():
            if event.type == QUIT:

                quit_scr = True


            elif event.type == KEYDOWN:

                if event.key == K_ESCAPE:

                    quit_scr = True

                elif event.key == K_y and quit_scr == True:

                    quit_game(data_list_2, True)

                elif event.key == K_n and quit_scr == True:

                    quit_game(data_list_2, False)

                elif event.key == K_c and quit_scr == True:

                    quit_scr = False

                elif event.key == K_LEFT:

                    angle += 1

                elif event.key == K_RIGHT:

                    angle -= 1

                elif event.key == K_f:

                    angle = 0

                elif event.key == K_b:

                    angle = 180

                elif event.key == K_r:

                    angle = 90

                elif event.key == K_l:

                    angle = -90

                elif event.key == K_e:

                    if CONTROL == False:

                        if show_edges == False:

                            show_edges = True

                        elif show_edges == True:

                            show_edges = False

                    else:

                        if show_unedited == False:

                            show_unedited = True

                        elif show_unedited == True:

                            show_unedited = False


                elif event.key == K_v:

                    if faces_vis == False:

                        faces_vis = True

                    elif faces_vis == True:

                        faces_vis = False

                elif event.key == K_n:

                    if norm_vis == False:

                        norm_vis = True

                    elif norm_vis == True:

                        norm_vis = False

                elif event.key == K_DELETE:

                    data_list_2 = copy.deepcopy(data_list)

                    #int_faces_1 = []

                elif event.key == K_c:

                    points = []

                    coords = []

                    cut_plane = []

                    cut_plane_2 = []

                    #int_faces_1 = []

                elif event.key == K_a:

                    if len(cut_plane) > 0 and align_to_plane == False:

                        align_to_plane = True

                    else:

                        align_to_plane = False

                        clicked = True

                elif event.key == K_LSHIFT or event.key == K_RSHIFT:

                    SHIFT = True

                elif event.key == K_LCTRL or event.key == K_RCTRL:

                    CONTROL = True

                elif event.key >= K_0 and event.key <= K_9:

                    measurement_list.append(event.key-48)

                elif event.key == K_RETURN  and len(measurement_list) > 1 and len(points) > 0 and measurement > 0.0:

                    coord1 = copy.deepcopy(coords[-2])
                    coord2 = copy.deepcopy(coords[-1])

                    if align_to_plane == True & len(cut_plane_2) > 0:

                        plane = cut_plane_2

                    else:

                        plane = cut_plane

                    data_list_2 = move_vertices(int_faces_1, plane, measurement_2, data_list_2)

                    check_measurement = True

                    #measurement_list = [0]


                elif event.key == K_BACKSPACE and  len(measurement_list) > 1:

                    del(measurement_list[-1])





            elif event.type == KEYUP:

                if event.key == K_LSHIFT or event.key == K_RSHIFT:

                    SHIFT = False

                elif event.key == K_LCTRL or event.key == K_RCTRL:

                    CONTROL = False


            elif event.type == MOUSEBUTTONDOWN:

                if pygame.mouse.get_pressed()[0]:

                    point = list(pygame.mouse.get_pos())

                    clicked = True

                    if SHIFT == True and len(points) > 0:

                        last_point = points[-1]

                        if abs(last_point[0][0] - point[0]) > abs(last_point[0][1] - point[1]) :

                            point[1] = last_point[0][1]

                        else:

                            point[0] = last_point[0][0]

                        if len(points[-1]) == 1 :

                            points[-1].append(point)

                        else:

                            points.append([point])

                    elif len(points) == 0:

                        points.append([point])

                    elif len(points) > 0:

                        if len(points[-1]) == 1:

                            points[-1].append(point)

                        else:

                            points.append([point])


        for i in range(0, len(points)):

            for n in range(0, len(points[i])):

                pygame.draw.circle(DISPLAYSURF, (255, 50, 50), points[i][n], 5, 2)


        if len(points) > 0:

            if len(points[-1]) % 2 == 0:

                for i in range(0, len(points)):

                    pygame.draw.line(DISPLAYSURF, (255, 50, 50), points[i][0], points[i][1])

                    if clicked == True:

                        coords.append(data_point_screen_convertor(points[-1][0], scale, min_z))

                        coords.append(data_point_screen_convertor(points[-1][1], scale, min_z))

                    #if check_measurement == True:

                if len(cut_plane_2) == 0 or clicked == True or align_to_plane == False:

                    if plane_aligned == True:

                        del(coords[-2:])

                    try:

                        int_faces_1, cut_plane = intersect(coords[-2], coords[-1], data_list_2, [])

                    except IndexError:

                        break

                    plane_aligned == False

                if align_to_plane == True and len(cut_plane_2) == 0:

                    #print 'yah 1'

                    cut_plane_2, coord1, coord2 = align_plane(int_faces_1, cut_plane, data_list_2, coords[-2], coords[-1])

                    #coords.append(coord1)
                    #coords.append(coord2)

                    p1 = screen_point_convertor(coord1, scale, min_z)
                    p2 = screen_point_convertor(coord2, scale, min_z)

                    points.append([p1, p2])

                    int_faces_1 = intersect(coord1, coord2, data_list_2, cut_plane_2)[0]

                    plane_aligned = True

                measurement = calc_measurement(int_faces_1)

                measurement_text(measurement)



            else:

                for i in range(0, len(points) - 1):

                    pygame.draw.line(DISPLAYSURF, (255, 50, 50), points[i][0], points[i][1])

        if check_measurement == True:

                if len(cut_plane_2) == 0:

                    int_faces_1, cut_plane = intersect(coords[-2], coords[-1], data_list_2, [])

                if align_to_plane == True:


                    cut_plane_2, coord1, coord2 = align_plane(int_faces_1, cut_plane, data_list_2, coords[-2], coords[-1])

                    p1 = screen_point_convertor(coord1, scale, min_z)
                    p2 = screen_point_convertor(coord2, scale, min_z)

                    points.append([p1, p2])

                    int_faces_1 = intersect(coord1, coord2, data_list_2, cut_plane_2)[0]


                measurement = calc_measurement(int_faces_1)

                measurement_text(measurement)


        if len(test_data) > 0:
            text3('offset = ' + str(test_data['delta_h']),[0, 80], [255, 255, 255])
            text3('total angle = ' + str(test_data['total angle']), [0, 100], [255, 255, 255])

        if len(int_faces_1) > 0:

            for i in int_faces_1:

                cutp1 = i[1][0][2]
                cutp2 = i[1][1][2]
                cutp1 = rotate_data(cutp1, angle)
                cutp1 = screen_point_convertor(cutp1, scale, min_z)
                cutp2 = rotate_data(cutp2, angle)
                cutp2 = screen_point_convertor(cutp2, scale, min_z)

                pygame.draw.circle(DISPLAYSURF, (50, 255, 50), cutp1, 5, 2)
                pygame.draw.circle(DISPLAYSURF, (50, 255, 50), cutp2, 5, 2)

                pygame.draw.line(DISPLAYSURF, (255, 50, 50), cutp1, cutp2)


        #align_to_plane = False




        pygame.display.update()
        FPSClock.tick(FPS)

    return test_data, points



def init_data():

    global eqns, face_eqns, attached_f, int_faces, plane_eqn, c1, c2, c3

    eqns = equations(data_list)

    face_eqns = calc_planes(data_list)

    attached_f = face_connects(data_list)

    c1, c2 = [200.0, 0.0, 1200.0], [-200.0, 0.0, 1200.0]

    c3 = map(lambda a, b: a + b, c1, [0.0, 100.0, 0.0])

    #int_faces, plane_eqn = intersect(c1, c2, data_list)







def Main():

    global mn

    format_list(data_list)

    #datalist = check_data(data_list)[0]

    centre_point = calc_centre(data_list[1])

    mn = create_screen(centre_point)


Main()
