import os, pygame, sys, math, random, itertools, copy
from pygame.locals import *
import json

from biodesic_functions import *
from freecad_formatter import freecad_format
from input_file_formatter import InputFormatter
from output_file_formatter import OutputFormatter

file_name = "test_data/Skinny-v5.txt"

file_name = "test_data/Skinny-v5.obj"

file_path = os.path.join(os.getcwd(), file_name)

pygame.init()

FPS = 10
FPSClock = pygame.time.Clock()

Screen_width = 1200
Screen_height = 800


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


def display_model(data, display, angle, centre_point, scale, min_z, show_face_no, show_av_norms,
                  show_edges, avg_normals=None):
    """
    Draws the polygons of each face as different colours
    """

    polygon_list = []
    #height = pygame.display.get_height()
    centre_point = rotate_data(centre_point, angle)
    #eqns_2 = correct_normals(data)[-1:][0]
    eqns_2 = equations(data)    

    for i in range(0, len(data[2])):
        polygon = []
        face_no = i

        for n in range(0, len(data[2][i])):
            vert_no = data[2][i][n]
            points = rotate_data(data[1][(vert_no - 1)], angle)
            points = screen_point_convertor(points, scale, min_z)
            normal = eqns_2[i][4]
            normal = rotate_data(normal, angle)

            if normal[1] > 0.0:
                polygon.append(points)

        if len(polygon) > 2:
            polygon_center = calc_face_centre(face_no, data)
            polygon_center = rotate_data(polygon_center, angle)
            polygon_list.append([i, polygon, polygon_center, normal])

    polygon_list = sorted(polygon_list, key=sort_polygons)

    for i in range(0, len(polygon_list)):
        polygon = polygon_list[i][1]
        face_no = polygon_list[i][0]
        normal = polygon_list[i][3]
        # if face_no == 105:
        #     print angle
        #     print normal

        if len(polygon) > 0:
            dot_prod = abs(sum(map(lambda a, b: a * b, normal, [0.0, 1.0, 0.0])))
            dot_prod = dot_prod ** 2
            # print dot_prod
            colour = int(255 * i / len(data[2]))
            colour_1 = int(200 * dot_prod)
            colour_2 = int(255 * dot_prod)
            pygame.draw.polygon(display, (255 , colour_2, 255 - colour_1), polygon, 0)

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
            avg_normals = draw_avg_normals(data, eqns_2, scale, angle, min_z, display, avg_normals)
    return scale, min_z, polygon_list, avg_normals

def draw_avg_normals(data, eqns, scale, angle, min_z, display, avg_normals=None):
    if avg_normals == None:
        print "MEH"
        avg_normals = calculate_all_avg_normals(data, eqns)
    for i in range(0, len(avg_normals)):
        av_norm_rotated = rotate_data(avg_normals[i], angle)
        if av_norm_rotated[1] >= 0:
            p1 = data[1][i]
            normal = map(lambda a: a * 30 / scale , avg_normals[i])
            p2 = map(lambda a, b: a + b, p1, normal)

            p1 = rotate_data(p1, angle)
            p1 = screen_point_convertor(p1, scale, min_z)

            p2 = rotate_data(p2, angle)
            p2 = screen_point_convertor(p2, scale, min_z)

            pygame.draw.line(display, [255, 255, 255], p1, p2, 1)
    return avg_normals


def draw_edges(data, display, angle, centre_point, show_av_norms, scale, min_z):
    #Draws the polygons of each face as different colours

    polygon_list = []
    centre_point = rotate_data(centre_point, angle)
    eqns_2 = equations(data)
    # av_normals = []
    colour_black_grey = (50, 50, 50)

    # for i in range(0, len(data[1])):
    #     av_normal = avg_normal((i + 1), data, eqns_2)
    #     av_normals.append(av_normal)

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

        if len(polygon) > 0:
            for k in range(0, len(polygon)):
                if k == len(polygon) - 1:
                    pygame.draw.line(display, colour_black_grey, polygon[k], polygon[0], 1)

                else:
                    pygame.draw.line(display, colour_black_grey, polygon[k], polygon[k+1], 1)


        polygon_list.append(polygon)

        # for i in range(0, len(av_normals)):
        #     av_norm_rotated = rotate_data(av_normals[i], angle)
        #     if show_av_norms == True and av_norm_rotated[1] > 0:
        #         p1 = data[1][i]
        #         normal = map(lambda a: a * 30 / scale , av_normals[i])
        #         p2 = map(lambda a, b: a + b, p1, normal)

        #         p1 = rotate_data(p1, angle)
        #         p1 = screen_point_convertor(p1, scale, min_z)

        #         p2 = rotate_data(p2, angle)
        #         p2 = screen_point_convertor(p2, scale, min_z)

        #         pygame.draw.line(display, [255, 0, 0], p1, p2, 2)


def cut_lines(points):
    point_count = len(points)
    if len(points) % 2 != 0:
        point_count -= 1

    for i in range(0, point_count, 2):
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
    # pygame.draw.polygon(display, (255, 0, 255), box, 0)
    display.blit(textobj1, textsurf1)


def convert_list(list_1):
    # Converts the input from the UI into an integer
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
        output_formatter = OutputFormatter(file_path, "obj")
        output_formatter.save_new_file_name(data)
    pygame.quit()
    sys.exit()


def create_screen(data_list):
    centre_point = calc_centre(data_list[1])
    data_list_2 = copy.deepcopy(data_list)


    DISPLAYSURF = pygame.display.set_mode((Screen_width, Screen_height), 0, 32)
    pygame.display.set_caption('BioDesic Pattern Fitter Version 2')
    pygame.key.set_repeat(50, 30)

    angle = 0
    delta_ang_pheta = 2
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
    connected_faces = face_connects(data_list)
    avg_normals = None

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
        try:
            DISPLAYSURF.fill((0, 0, 0))

            scale, min_z, polygon_list, avg_normals = display_model(
                data_list_2,
                DISPLAYSURF,
                angle,
                centre_point,
                scale,
                min_z,
                faces_vis,
                norm_vis,
                show_edges,
                avg_normals
            )

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
                # print event
                if event.type == QUIT:
                    quit_scr = True

                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        quit_scr = True

                    elif event.key == K_y and quit_scr == True:
                        quit_game(data_list_2, True)

                    elif event.key == K_n and quit_scr == True:
                        quit_game(data_list_2, False)

                    elif event.key == K_c and quit_scr == True and not CONTROL:
                        quit_scr = False

                    elif event.key == K_c and CONTROL == True:
                        quit_scr = True

                    elif event.key == K_LEFT:
                        angle += delta_ang_pheta

                    elif event.key == K_RIGHT:
                        angle -= delta_ang_pheta

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

                    elif event.key == K_c:
                        points = []
                        coords = []
                        cut_plane = []
                        cut_plane_2 = []
                        int_faces = []

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

                        data_list_2, avg_normals = move_vertices(int_faces_1, plane, measurement_2, data_list_2, connected_faces)
                        check_measurement = True

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

                    if len(cut_plane_2) == 0 or clicked == True or align_to_plane == False:
                        # if plane_aligned == True:
                        #     print coords
                            # del(coords[-2:])
                        try:
                            int_faces_1, cut_plane = get_intersect_face_plane(coords[-2], coords[-1], data_list_2, [])

                        except IndexError as error:
                            print(error)
                            break

                        plane_aligned == False

                    if align_to_plane == True and len(cut_plane_2) == 0:
                        cut_plane_2, coord1, coord2 = align_plane(int_faces_1, cut_plane, data_list_2, coords[-2], coords[-1])

                        p1 = screen_point_convertor(coord1, scale, min_z)
                        p2 = screen_point_convertor(coord2, scale, min_z)
                        points.append([p1, p2])
                        int_faces_1 = get_intersect_face_plane(coord1, coord2, data_list_2, cut_plane_2)[0]
                        plane_aligned = True

                    elif align_to_plane == True and len(cut_plane_2) > 0:
                        int_faces_1 = get_intersect_face_plane(coords[-2], coords[-1], data_list_2, cut_plane_2)[0]
                        plane_aligned = True

                    measurement = calc_measurement(int_faces_1)
                    measurement_text(measurement)

                else:
                    for i in range(0, len(points) - 1):
                        pygame.draw.line(DISPLAYSURF, (255, 50, 50), points[i][0], points[i][1])

            if check_measurement == True:
                if len(cut_plane_2) == 0:
                    int_faces_1, cut_plane = get_intersect_face_plane(coords[-2], coords[-1], data_list_2, [])

                if align_to_plane == True:
                    cut_plane_2, coord1, coord2 = align_plane(int_faces_1, cut_plane, data_list_2, coords[-2], coords[-1])
                    p1 = screen_point_convertor(coord1, scale, min_z)
                    p2 = screen_point_convertor(coord2, scale, min_z)
                    points.append([p1, p2])
                    int_faces_1 = get_intersect_face_plane(coord1, coord2, data_list_2, cut_plane_2)[0]

                measurement = calc_measurement(int_faces_1)
                measurement_text(measurement)

            if len(test_data) > 0:
                text3('offset = ' + str(test_data['delta_h']),[0, 80], [255, 255, 255])
                text3('total angle = ' + str(test_data['total angle']), [0, 100], [255, 255, 255])

            if len(int_faces_1) > 0 and len(points) > 0:
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

            pygame.display.update()
            FPSClock.tick(FPS)
        
        except Exception as error:
            print error
            print "Oh no!"



def main():
    formatter = InputFormatter(file_name)
    data_list = formatter.data
    with open("data.txt", "w+") as file:
        json.dump(data_list, file, indent=4)
        file.close()
    with open("eqns.txt", "w+") as file:
        json.dump(equations(data_list), file, indent=4)
        file.close()
    create_screen(data_list)

if __name__ == '__main__':
    main()
