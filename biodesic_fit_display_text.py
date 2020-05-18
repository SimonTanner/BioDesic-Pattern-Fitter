import pygame, sys, collections
from pygame.locals import *

class DisplayData():

    def __init__(self, surface):
        self.box_grey = (150, 150, 150)
        self.text_colour = (0, 0, 0)
        self.box_edge_grey_offset = -50
        self.box_edge_grey = list(map(lambda a: a + self.box_edge_grey_offset, self.box_grey))
        self.surface = surface
        self.font = pygame.font.match_font('dejavusans')
        self.font_size = 13
        self.large_font_size = 18
        self.screen_height = self.surface.get_height()
        self.screen_width = self.surface.get_width()
        self.text_boxes = {}
        self._init_text_values()
        self.add_text_data()
        self.draw_text_boxes([0, 0])

    def _init_text_values(self):
        self.text_items = collections.OrderedDict({
            'measurement': {
                'text': ['measurement: ', 'mm'],
                'args': [0]
            },
            'new_measurement': {
                'text': ['new measurement: ', 'mm'],
                'args': [0]
            },
            'coordinates_1': {
                'text': ['point 1: '],
                'args': []
            },
            'coordinates_2': {
                'text': ['point 2: '],
                'args': []
            },
            'ang_x': {
                'text': ['x angle: ', ' deg'],
                'args': []
            },
            'ang_y': {
                'text': ['y angle: ', ' deg'],
                'args': []
            },
            'ang_z': {
                'text': ['z angle: ', ' deg'],
                'args': []
            }
        })

    def clear_values(self):
        self._init_text_values()

    def display(self):
        self.draw_text_boxes([0, 0])

    def update_value(self, name, value):
        if isinstance(value, (list, tuple)):
            value = list(map(lambda a: round(a, 0), value))
            value = str(value).strip('[]()')
        elif isinstance(value, float):
            value = int(value)

        self.text_items[name]['args'] = [value]
        self.add_text_data()
    
    def update_angle(self, angle):
        keys = ['ang_x', 'ang_y', 'ang_z']
        for idx in range(0, len(keys)):
            self.update_value(keys[idx], angle[idx])

    def _create_text(self, text, args):
        display_text = ""
        screen_offset = 20
        box_offset = 10

        for i in range(0, len(text)):
            display_text += text[i]
            if i < len(args):
                display_text += str(args[i])

        font_obj = pygame.font.Font(self.font, self.font_size)
        text_obj = font_obj.render(display_text, True, self.text_colour, self.box_grey)
        text_surf = text_obj.get_rect()
        bounding_box = text_surf.inflate(screen_offset, screen_offset)

        return {
            'text': {
                'object': text_obj,
                'surface': text_surf
            },
            'box': bounding_box,
            'offset': {
                'screen': screen_offset,
                'box' : box_offset
            },
            'width': bounding_box.width
        }

    def add_text_data(self):
        max_width = 0
        for name, item in self.text_items.iteritems():
            self.text_boxes[name] = self._create_text(item['text'], item['args'])
            if self.text_boxes[name]['width'] > max_width:
                max_width = self.text_boxes[name]['width']
        self.max_width = max_width

    def draw_text_boxes(self, position):
        for _, item in self.text_boxes.iteritems():
            text_surf = item['text']['surface']
            text_obj = item['text']['object']
            box = item['box']
            box.width = self.max_width
            screen_offset = item['offset']['screen']
            box_offset = item['offset']['box']
            offset = screen_offset - box_offset
            text_surf.topleft = ( (screen_offset + position[0]), (screen_offset + position[1]) )
            box.topleft = ( (offset + position[0]), (offset + position[1]) )
            self.draw_box(box)
            self.surface.blit(text_obj, text_surf)
            position[1] += box.height

    
    def draw_box(self, bounding_box):
        box_coords = self.get_rect_points(bounding_box)
        pygame.draw.rect(self.surface, self.box_grey, bounding_box)
        pygame.draw.lines(self.surface, self.box_edge_grey, False, box_coords)

    def text3(self, text, screen_coord, colour):
        text = str(text)

        fontobj = pygame.font.Font(self.font, self.font_size)
        textobj = fontobj.render(text, True, colour, self.box_grey)
        text_surf = textobj.get_rect()
        text_surf.topleft = ((20 + screen_coord[0]), (20 + screen_coord[1]))

        self.surface.blit(textobj, text_surf)


    def quit_text(self, text, screen_coord, colour):
        if type(text) != 'str':
            text = str(text)
        fontobj = pygame.font.Font(self.font, self.large_font_size)
        text_obj = fontobj.render(text, True, colour, self.box_grey)
        text_surf = text_obj.get_rect()
        text_surf.center = ( screen_coord[0], screen_coord[1] )

        self.surface.blit(text_obj, text_surf)
        # return text_obj, text_surf


    def quit_screen(self):
        text_pos = [int(self.screen_width / 2), int(self.screen_height / 2)]
        text_surf = self.quit_text('Would you like to save the new model?', text_pos, [255, 50, 50])
        # box = text_surf.get_rect()
        text_pos_2 = map(lambda a, b: a + b, text_pos, [0, 40])
        self.quit_text('Enter Y/N or C for cancel', text_pos_2, [255, 50, 50])

    def get_rect_points(self, rect):
        return [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft]

def simple_text(surface, text, coords, colour=[50, 50, 50]):
    text = str(text)
    font = pygame.font.match_font('dejavusans')
    fontobj = pygame.font.Font(font, 12)
    textobj = fontobj.render(text, True, colour)
    text_surf = textobj.get_rect()
    text_surf.center = ((coords[0]), (coords[1]))

    surface.blit(textobj, text_surf)

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


def get_rect_points(rect):
    return [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft]



