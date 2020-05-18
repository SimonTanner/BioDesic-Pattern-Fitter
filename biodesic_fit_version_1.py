import os, pygame, sys, math, random, itertools, copy
from pygame.locals import *
import json
import traceback
import time, datetime

from biodesic_functions import *
from biodesic_fit_display_text import *
from freecad_formatter import freecad_format
from input_file_formatter import InputFormatter
from output_file_formatter import OutputFormatter

# file_name = "test_data/Skinny-v5.txt"

file_name = "test_data/Skinny-v5.obj"

# file_name = "test_data/bio-hoody-02-v3 _Fitted.txt"

file_path = os.path.join(os.getcwd(), file_name)

pygame.init()

FPS = 30
FPSClock = pygame.time.Clock()

Screen_width = 1400
Screen_height = 900


def screen_point_convertor(point, scale, mid_z, screen_height, screen_width, rel_pos=(0, 0)):
    """
    Converts the data coordinates (x, y, z) to fit on screen (x, y)
    """
    point = map(float, point)
    point[0] = int(point[0] * scale + screen_width / 2) + rel_pos[0]
    point[2] = int( screen_height / 2 - (point[2] - mid_z) * scale ) + rel_pos[1]
    del(point[1])

    return point


def data_point_screen_convertor(point, scale, mid_z, centre_point, angle, screen_height, screen_width, rel_pos=(0, 0)):
    """
    Converts (x, y) screen coordinates back to real (x, y, z) coords
    """
    point = map(float, point)
    point[0] = (point[0] - screen_width / 2  + rel_pos[0]) / scale
    z_coord = mid_z + (screen_height / 2 + rel_pos[1] - point[1]) / scale
    point.append(z_coord)
    point[1] = 0.0

    point = rotate_data(point, angle, centre_point)

    return point


def sort_polygons(polygons):
    return polygons[2][1]

def calc_light_colour(vector, face_normal, data, colour, intensity=1):
    """
    Calculates the colour of a surface given a light direction vector & base colour
    """
    light_dir_scale = math.sqrt(sum(vector))
    light_dir_normal = list(map(lambda c: c / light_dir_scale, vector))
    dot_prod = abs(sum(map(lambda a, b: a * b, face_normal, light_dir_normal))) ** 2
    colour = list(map(lambda a: light_colour(dot_prod, a, intensity), colour))

    return colour

def light_colour(dot_prod, value, intensity):
    colour = int(dot_prod * value * intensity)
    if colour > 255:
        colour = 255
    return colour

def display_model(data, display, angle, centre_point, scale, mid_z, show_face_no, show_av_norms,
                  show_edges, screen_height, screen_width, avg_normals=None, rel_pos=(0, 0)):
    """
    Draws the polygons of each face as different colours
    """
    polygon_list = []
    centre_point = rotate_data(centre_point, angle, centre_point)
    eqns_2 = equations(data)
    light_dir = [0.5, 1.0, 0.0]
    edge_colour = (200, 0, 0)   # Red
    face_colour = (255, 40, 180)

    for i in range(0, len(data[2])):
        polygon = []
        face_no = i

        for n in range(0, len(data[2][i])):
            vert_no = data[2][i][n]
            
            points = rotate_data(data[1][(vert_no - 1)], angle, centre_point)
            points = screen_point_convertor(points, scale, centre_point[2], screen_height, screen_width, rel_pos)
            normal = eqns_2[i][4]
            normal = rotate_data(normal, angle)

            if normal[1] > 0.0:
                polygon.append(points)

        if len(polygon) > 2:
            polygon_center = calc_face_centre(face_no, data)
            polygon_center = rotate_data(polygon_center, angle, centre_point)
            polygon_list.append([i, polygon, polygon_center, normal])

    polygon_list = sorted(polygon_list, key=sort_polygons)
    # new_display = pygame.Surface((screen_height, screen_width))
    # new_display.set_alpha(10)                # alpha level
    # new_display.fill((0 ,0 ,0))
    for i in range(0, len(polygon_list)):
        polygon = polygon_list[i][1]
        face_no = polygon_list[i][0]
        normal = polygon_list[i][3]

        if len(polygon) > 0:
            colour = int(255 * i / len(data[2]))
            face_light_colour = calc_light_colour(light_dir, normal, data, face_colour, 5)
            pygame.draw.polygon(display, face_light_colour, polygon, 0)

            if show_face_no == True: 
                polygon_center = calc_face_centre(face_no, data)
                polygon_center = rotate_data(polygon_center, angle, centre_point)
                polygon_center = screen_point_convertor(polygon_center, scale, mid_z, screen_height, screen_width, rel_pos)
                simple_text(display, (face_no+1), polygon_center, (255, colour, 255 - colour))

            if show_edges == True:
                for k in range(0, len(polygon)):
                    if k == len(polygon) - 1:
                        pygame.draw.line(display, edge_colour, polygon[k], polygon[0], 1)
                    else:
                        pygame.draw.line(display, edge_colour, polygon[k], polygon[k+1], 1)

        if show_av_norms == True:
            avg_normals = draw_avg_normals(data, eqns_2, scale, angle, centre_point, mid_z, display, screen_height, screen_width, avg_normals, rel_pos)
        # if show_face_no is True:
        #     display.blit(new_display, (0, 0))
    return scale, mid_z, polygon_list, avg_normals

def draw_avg_normals(data, eqns, scale, angle, centre_point, mid_z, display, screen_height,
    screen_width, avg_normals=None, rel_pos=(0, 0)):
    """
    Displays the average normal of faces surrounding a vertex
    """
    normal_colour = (255, 255, 255)
    normal_disp_size = 30

    if avg_normals == None:
        avg_normals = calculate_all_avg_normals(data, eqns)
    for i in range(0, len(avg_normals)):
        av_norm_rotated = rotate_data(avg_normals[i], angle, centre_point)
        if av_norm_rotated[1] >= 0:
            p1 = data[1][i]
            normal = map(lambda a: a * normal_disp_size / scale , avg_normals[i])
            p2 = map(lambda a, b: a + b, p1, normal)

            p1 = rotate_data(p1, angle, centre_point)
            p1 = screen_point_convertor(p1, scale, mid_z, screen_height, screen_width, rel_pos)

            p2 = rotate_data(p2, angle, centre_point)
            p2 = screen_point_convertor(p2, scale, mid_z, screen_height, screen_width, rel_pos)

            pygame.draw.line(display, normal_colour, p1, p2, 1)

    return avg_normals


def draw_edges(data, display, angle, centre_point, show_av_norms, scale, mid_z,
screen_height, screen_width, rel_pos=(0, 0)):
    """
    Draws the polygons of each face as different colours
    """

    polygon_list = []
    eqns_2 = equations(data)
    colour_black_grey = (50, 50, 50)

    for i in range(0, len(data[2])):
        polygon = []
        for n in range(0, len(data[2][i])):

            vert_no = data[2][i][n]
            points = rotate_data(data[1][(vert_no - 1)], angle, centre_point)
            points = screen_point_convertor(points, scale, mid_z, screen_height, screen_width, rel_pos)
            normals = eqns_2[i][4]
            normals = rotate_data(normals, angle)

            if normals[1] > 0:
                polygon.append(points)

        if len(polygon) > 0:
            for k in range(0, len(polygon)):
                if k == len(polygon) - 1:
                    pygame.draw.line(display, colour_black_grey, polygon[k], polygon[0], 1)

                else:
                    pygame.draw.line(display, colour_black_grey, polygon[k], polygon[k+1], 1)

        polygon_list.append(polygon)


def draw_cut_lines(display, points):
    point_count = len(points)
    if len(points) % 2 != 0:
        point_count -= 1

    for i in range(0, point_count, 2):
        pygame.draw.line(display, (255, 50, 50), points[i], points[i + 1])



def quit_game(data, save):
    if save == True:
        output_formatter = OutputFormatter(file_path, "obj")
        output_formatter.save_new_file_name(data)
    pygame.quit()
    sys.exit()

def draw_axes(display, angle):
    """
    Draws the x, y, z axes on screen
    """
    colour = (0, 0, 0)
    size = 50
    offset = 50
    axes = ({'x': (-size, 0, 0)}, {'y': (0, size, 0)}, {'z': (0, 0, size)})
    screen_dims = display.get_size()
    screen_offset = (2 * offset, offset)
    screen_position = sum_vectors(screen_dims, screen_offset, True)
    # print(screen_position)
    for axis in axes:
        name = axis.keys()[0]
        coords = axis.values()[0]
        rotated_coords = rotate_data(coords, angle)
        del(rotated_coords[1])
        position = sum_vectors(screen_position, rotated_coords, True)
        # print(position)
        simple_text(display, name, position, colour)
        pygame.draw.line(display, colour, screen_position, position)
    # sys.exit()



def calculate_display_sizes(screen_height, screen_width, data):
    """
    Calculates the scale that the model should be displayed at
    """
    height = float(screen_height * .95)
    width = float(screen_width * .95)

    delta_mid_z = calc_delta_z(data)
    delta_mid_x = calc_delta_x(data)

    scale_z = height / delta_mid_z[0]
    scale_x = width / delta_mid_x[0]

    if scale_z < scale_x:
        scale = scale_z
    else:
        scale = scale_x

    mid_z = delta_mid_z[1]
    return scale, mid_z

def move_screen_points(screen_points, mouse_rel_motion):
    """
    Moves the list of click points when the user pans
    """
    moved_points = []
    for point_1_2 in screen_points:
        moved_point = []
        for point in point_1_2:
            moved_point.append(map(lambda a, b: a + b, point, mouse_rel_motion))
            # print("------------------point------------------")
            # print(mouse_rel_motion)
            # print(point)
            # print("------------------------------------------------------")
        moved_points.append(moved_point)
    return moved_points

def display_slice_outlines(display, int_faces, angle, centre_point, scale, mid_z,
    screen_height, screen_width, mouse_rel_pos):
    line_colour, circle_colour = (255, 50, 50), (50, 255, 50)
    for i in int_faces:
        cutp1 = i[1][0][2]
        cutp2 = i[1][1][2]
        cutp1 = rotate_data(cutp1, angle, centre_point)
        cutp1 = screen_point_convertor(cutp1, scale, mid_z, screen_height, screen_width, mouse_rel_pos)
        cutp2 = rotate_data(cutp2, angle, centre_point)
        cutp2 = screen_point_convertor(cutp2, scale, mid_z, screen_height, screen_width, mouse_rel_pos)

        pygame.draw.circle(display, circle_colour, cutp1, 5, 2)
        pygame.draw.circle(display, circle_colour, cutp2, 5, 2)
        pygame.draw.line(display, line_colour, cutp1, cutp2)


class SeperatedFaces:
    def __init__(self, data_list):
        self.objects = {}
        self.faces = []
        self.data_list = data_list

    def add_face(self, face_no):
        # Add a face to an object
        if face_no not in self.faces and not self.check_no_repeated_faces(face_no):
            self.faces.append(face_no)
        else:
            print("face no.: {} has already been added".format(face_no))

    def create_object(self):
        # Call once all faces that we wish to be seperate are selected
        object_key = len(self.objects) + 1
        self.objects[object_key] = self.faces
        self.clear_faces()

    def clear_faces(self):
        self.faces = []

    def check_no_repeated_faces(self, face_no):
        # Check the face where trying to add to a new object hasn't already been added
        for _obj_key, faces in self.objects.items():
            if face_no in faces:
                return True
            else:
                return False

    def get_objects(self):
        # Need to add check that total no of faces is equal to that of data_list
        return self.objects


def create_screen(data_list, screen_height, screen_width):
    # Calculate the centre point coordinate of the model
    centre_point = calc_centre(data_list[1])
    data_list_copy = copy.deepcopy(data_list)

    # Load icon
    logo_rel_path = 'logo/Bio-Logo-v1.jpg'
    logo_path = os.path.join(os.getcwd(), logo_rel_path)
    logo = pygame.image.load(logo_path)
    pygame.display.set_icon(logo)

    DISPLAYSURF = pygame.display.set_mode(
        (screen_width, screen_height),
        pygame.RESIZABLE|pygame.HWSURFACE|pygame.DOUBLEBUF,
        32
    )

    # Set name in title bar
    pygame.display.set_caption('BioDesic Pattern Fitter')
    background_colour = (50, 50 ,50)
    pygame.key.set_repeat(50, 10)

    # Instantiate text box class
    display_data = DisplayData(DISPLAYSURF)

    # Consts for rotational view angles
    view_angles = {
        'front': (0, 0, 180),
        'back': (0, 0, 0),
        'left': (0, 0, 90),
        'right': (0, 0, -90),
        'top': (-90, 0, 0),
        'bottom': (90, 0, 0)
    }
    angle = list(view_angles['front'])
    delta_ang_amount = 2 # Number of degrees to rotate by every frame
    # Dict for getting rotation coords by axis
    delta_ang_all = {
        'x': (delta_ang_amount, 0, 0),
        'y': (0, delta_ang_amount, 0),
        'z': (0, 0, delta_ang_amount)
    }

    def add_angles(angle, delta_ang, neg=False):
        const = 1
        if neg:
            const = -1
        angle = map(lambda a, b: a + const * b, angle, delta_ang)

        return angle

    SHIFT = False
    CONTROL = False

    points = [] # Screen coords of click points [x, y]
    coords = [] # Coordinates of click points in model space
    measurement = 0
    input_measurement = 0.0
    measurement_list = [0]

    quit_scr = False
    quitting = False

    faces_vis = False   # Display face nos
    norm_vis = False    # Display normals
    show_edges = False  # Display edges
    show_unedited = False   # Display unedited model edges
    align_to_plane = False  # Align slice plane to geometry
    plane_aligned = False
    int_faces_1 = []
    test_data = {}
    cut_plane_2 = []
    connected_faces = face_connects(data_list)
    avg_normals = None

    seperate_objects_mode = False
    seperated_faces = SeperatedFaces(data_list_copy)

    initial_scale, mid_z = calculate_display_sizes(screen_height, screen_width, data_list_copy)
    scale = initial_scale
    # z = []
    # for i in data_list_copy[1]:
    #     z.append(i[2])

    # print("Max z value = " + str(max(z)))
    # print("Min z value = " + str(min(z)))
    # print("Middle z value = " + str(mid_z))

    # Vars for handling mouse up & down events and moving objects on screen by dragging
    mouse_dwn_start = None
    max_mouse_dwn = 0.3
    mouse_dwn_delta = 0
    mouse_rel_pos = [0, 0]

    # Toggle boolean vars
    flip_bool = {True: False, False: True}

    cut_point_colour = (0, 100, 250)

    while True:
        try:
            DISPLAYSURF.fill(background_colour)

            draw_axes(DISPLAYSURF, angle)

            # Draw geometry of model
            scale, mid_z, _polygon_list, avg_normals = display_model(
                data_list_copy,
                DISPLAYSURF,
                angle,
                centre_point,
                scale,
                mid_z,
                faces_vis,
                norm_vis,
                show_edges,
                screen_height,
                screen_width,
                avg_normals,
                mouse_rel_pos
            )

            clicked = False

            # Draw unedited model edges
            if show_unedited == True:
                draw_edges(
                    data_list,
                    DISPLAYSURF,
                    angle,
                    centre_point,
                    norm_vis,
                    scale,
                    mid_z,
                    screen_height,
                    screen_width,
                    mouse_rel_pos
                )

            if quit_scr == True:
                display_data.quit_screen()

            if len(coords) > 0:
                display_data.update_value('coordinates_1', coords[-1])
                display_data.update_value('coordinates_2', coords[-2])

            for event in pygame.event.get():
                if event.type == VIDEORESIZE:
                    screen_height, screen_width = event.h, event.w
                    # to reset the scale when resizing add scale var below
                    _, mid_z = calculate_display_sizes(screen_height, screen_width, data_list_copy)
                    DISPLAYSURF = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE | pygame.DOUBLEBUF, 32)

                if event.type == QUIT:
                    quit_scr = True

                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        quit_scr = True

                    elif event.key == K_y and quit_scr == True:
                        quit_game(data_list_copy, True)

                    elif event.key == K_n and quit_scr == True:
                        quit_game(data_list_copy, False)

                    elif event.key == K_c:
                        if quit_scr and not CONTROL:
                            quit_scr = False
                        elif CONTROL:
                            quit_scr = True
                        else:
                            points = []
                            coords = []
                            cut_plane = []
                            cut_plane_2 = []
                            int_faces = []
                            display_data.clear_values()
                            measurement = 0

                    # Rotate view clockwise about z axis
                    elif event.key == K_LEFT:
                        angle = add_angles(angle, delta_ang_all['z'])

                    # Rotate view counter-clockwise about z axis
                    elif event.key == K_RIGHT:
                        angle = add_angles(angle, delta_ang_all['z'], True)

                    # Rotate view clockwise about x axis
                    elif event.key == K_UP:
                        angle = add_angles(angle, delta_ang_all['x'], True)
                    
                    # Rotate view counter-clockwise about x axis
                    elif event.key == K_DOWN:
                        angle = add_angles(angle, delta_ang_all['x'])

                    elif event.key == K_f:
                        angle = list(view_angles['front'])

                    elif event.key == K_b:
                        angle = list(view_angles['back'])

                    elif event.key == K_r:
                        if CONTROL:
                            mouse_rel_pos = [0, 0]
                            scale = initial_scale
                        else:
                            angle = list(view_angles['right'])
                        
                    elif event.key == K_l:
                        angle = list(view_angles['left'])

                    elif event.key == K_t:
                        angle = list(view_angles['top'])
                    
                    elif event.key == K_MINUS:
                        scale *= 0.9

                    elif event.key == K_EQUALS:
                        scale *= 1.1

                    elif event.key == K_e:
                        if CONTROL == False:
                            show_edges = flip_bool[show_edges]
                        else:
                            show_unedited = flip_bool[show_unedited]

                    elif event.key == K_s:
                        # Need to add logic for seperating faces to different objects
                        print("not currently implemented")
                        if seperate_objects_mode is True:
                            seperate_objects_mode = False
                        else:
                            seperate_objects_mode = True

                    elif event.key == K_v:
                        faces_vis = flip_bool[faces_vis]

                    elif event.key == K_n:
                        norm_vis = flip_bool[norm_vis]

                    elif event.key == K_DELETE:
                        data_list_copy = copy.deepcopy(data_list)

                    elif event.key == K_a:
                        if len(cut_plane) > 0 and align_to_plane == False:
                            # We can only align a plane if we have one already
                            align_to_plane = True
                        else:
                            align_to_plane = False
                            clicked = True
                            cut_plane_2 = []

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

                        # Move vertices to fit measurement entered
                        data_list_copy, avg_normals = offset_vertices(int_faces_1, plane, input_measurement, data_list_copy, connected_faces)
                        # check_measurement = True

                    elif event.key == K_BACKSPACE and len(measurement_list) > 1:
                        del(measurement_list[-1])

                elif event.type == KEYUP:
                    if event.key == K_LSHIFT or event.key == K_RSHIFT:
                        SHIFT = False

                    elif event.key == K_LCTRL or event.key == K_RCTRL:
                        CONTROL = False

                elif event.type == MOUSEMOTION:
                    get_rel = pygame.mouse.get_rel()
                    # If the left mouse is down and the mouse moves get the relative motion for panning the
                    # model
                    if mouse_dwn_start != None:
                        mouse_rel_pos = map(lambda x, y: x + y, get_rel, mouse_rel_pos)
                        

                elif event.type == MOUSEBUTTONDOWN:
                    # Start the timer to check how long the left mouse button is pressed
                    if pygame.mouse.get_pressed()[0]:
                        mouse_dwn_start = time.time()

                elif event.type == MOUSEBUTTONUP:
                    # Calculate how long the left button was pressed
                    if mouse_dwn_start != None:
                        mouse_dwn_delta = time.time() - mouse_dwn_start
                    # If time pressed less than max time assume it's a click
                    if mouse_dwn_start == None or mouse_dwn_delta < max_mouse_dwn:

                        point = list(pygame.mouse.get_pos())
                        clicked = True

                        if SHIFT == True and len(points) > 0:
                            last_point = points[-1]
                            if abs(last_point[0][0] - point[0]) > abs(last_point[0][1] - point[1]):
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
                    mouse_dwn_start = None
                    mouse_dwn_delta = 0


            for i in range(0, len(points)):
                # Draw points that have been clicked on screen
                for n in range(0, len(points[i])):
                    pygame.draw.circle(DISPLAYSURF, cut_point_colour, points[i][n], 5, 2)


            if len(points) > 0:
                print(points)
                print(mouse_rel_pos)
                print(coords)
                # points = move_screen_points(points, mouse_rel_pos)
                updated_points = []
                for coord in coords:
                    screen_coord = screen_point_convertor(
                        coord, scale, mid_z, screen_height, screen_width, rel_pos=(0, 0)
                    )
                    updated_points.append(screen_coord)

                # sys.exit()
                # points = updated_points
                
                if len(points[-1]) % 2 == 0:
                    for i in range(0, len(points)):
                        pygame.draw.line(DISPLAYSURF, cut_point_colour, points[i][0], points[i][1])
                        if clicked == True:
                            for i in range(0, len(points[-1])):
                                coords.append(
                                    data_point_screen_convertor(
                                        points[-1][i],
                                        scale,
                                        mid_z,
                                        centre_point,
                                        angle,
                                        screen_height,
                                        screen_width,
                                        mouse_rel_pos
                                    )
                                )

                    if (len(cut_plane_2) == 0 or clicked == True) and align_to_plane == False:
                        try:
                            # Calculate points of intersection between the cut plane and model
                            int_faces_1, cut_plane = get_intersect_face_plane(coords[-2], coords[-1], data_list_copy, [])

                        except IndexError as error:
                            print(error)
                            break

                        plane_aligned == False

                    if align_to_plane == True and len(cut_plane_2) == 0:
                        cut_plane_2, coord1, coord2 = align_plane(int_faces_1, cut_plane, data_list_copy, coords[-2], coords[-1])
                        # coords.extend([coord1, coord2])
                        print("align_to_plane: True, cut_plane: None")
                        print(cut_plane_2)

                        p1 = screen_point_convertor(coord1, scale, mid_z, screen_height, screen_width, mouse_rel_pos)
                        p2 = screen_point_convertor(coord2, scale, mid_z, screen_height, screen_width, mouse_rel_pos)
                        points.append([p1, p2])
                        int_faces_1 = get_intersect_face_plane(coord1, coord2, data_list_copy, cut_plane_2)[0]
                        print(len(int_faces_1))

                        plane_aligned = True

                    elif align_to_plane == True and len(cut_plane_2) > 0:
                        print("align_to_plane: True, cut_plane: True")
                        print(cut_plane_2)
                        int_faces_1 = get_intersect_face_plane(coords[-2], coords[-1], data_list_copy, cut_plane_2)[0]

                        plane_aligned = True
                        print(len(int_faces_1))

                    measurement = calc_measurement(int_faces_1)

                else:
                    for i in range(0, len(points) - 1):
                        pygame.draw.line(DISPLAYSURF, cut_point_colour, points[i][0], points[i][1])

                measurement = calc_measurement(int_faces_1)

            # if len(test_data) > 0:
            #     display_data.text3('offset: ' + str(test_data['delta_h']),[0, 80], [255, 255, 255])
            #     display_data.text3('total angle: ' + str(test_data['total angle']), [0, 100], [255, 255, 255])

            # If there is a cut through display intersection lines
            if len(int_faces_1) > 0 and len(points) > 0:
                display_slice_outlines(
                    DISPLAYSURF, int_faces_1, angle, centre_point, scale, mid_z,
                    screen_height, screen_width, mouse_rel_pos
                )

            input_measurement = convert_ui_integer_input(measurement_list)
            display_data.update_value('measurement', measurement)
            display_data.update_value('new_measurement', input_measurement)
            display_data.update_angle(angle)
            display_data.display()

            pygame.display.flip()
            FPSClock.tick(FPS)
        
        except Exception as error:
            print(error)
            print("Oh no!")
            print(traceback.format_exc())



def main(debug=False):
    formatter = InputFormatter(file_name)
    data_list = formatter.data

    if debug:
        # Output data for debugging
        with open("data.txt", "w+") as file:
            json.dump(data_list, file, indent=4)
            file.close()
        with open("eqns.txt", "w+") as file:
            json.dump(equations(data_list), file, indent=4)
            file.close()

    create_screen(data_list, Screen_height, Screen_width)

if __name__ == '__main__':
    args = sys.argv
    if len(args) > 1:
        debug = args[1].split("=")
    else:
        debug = False
    # print(debug)
    if debug == "True":
        debug = True

    main(debug)
