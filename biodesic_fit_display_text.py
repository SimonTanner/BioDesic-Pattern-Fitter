import pygame
from pygame.locals import *

def measurement_text(measurement):
    display = pygame.display.get_surface()
    screen_height = display.get_height()
    screen_width = display.get_width()

    measurement = int(measurement)
    measurement = str(measurement)

    fontobj = pygame.font.Font('freesansbold.ttf', 14)
    textobj = fontobj.render('Measurement: ' + measurement + ' mm', True, [100, 100, 255], [0, 0, 0])
    textsurf = textobj.get_rect()
    textsurf.topleft = ( (20), (20) )

    fontobj1 = pygame.font.Font('freesansbold.ttf', 14)
    textobj1 = fontobj1.render('Change Measurement', True, [100, 100, 255], [50, 50, 50])
    textsurf1 = textobj1.get_rect()
    textsurf1.topright = ( (screen_width - 20), (20) )

    offset = [-5, -5, 5, 5]
    box = map(lambda a, b: a + b, offset, textsurf1)
    pygame.draw.rect(display, (255, 0, 255), box, 0)
    display.blit(textobj, textsurf)
    display.blit(textobj1, textsurf1)


def convert_ui_integer_input(input_list):
    """
    Converts the input from the UI into an integer
    """
    number = str(input_list).translate(None, ',')
    number = number.translate(None, ' ')
    number = number.translate(None, '[')
    number = number.translate(None, ']')
    number = int(number)

    return number


def measurement_text2(measurement, screen_coord):
    display = pygame.display.get_surface()

    measurement = str(measurement)

    fontobj = pygame.font.Font('freesansbold.ttf', 14)
    textobj = fontobj.render('New Measurement: ' + measurement + ' mm', True, [100, 100, 255], [0, 0, 0])
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


def text2(text, screen_coord, colour, display=None):
    if display is None:
        display = pygame.display.get_surface()
    text = str(text)
    colour = None
    fontobj = pygame.font.Font('freesansbold.ttf', 12)
    textobj = fontobj.render(text, True, [0, 0, 0])
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


def quit_screen(screen_height, screen_width):
    text_pos = [int(screen_width/2), int(screen_height/2)]
    text4('Would you like to save the new model?', text_pos, [255, 50, 50])
    text_pos_2 = map(lambda a, b: a + b, text_pos, [0, 40])
    text4('Enter Y/N or C for cancel', text_pos_2, [255, 50, 50])
