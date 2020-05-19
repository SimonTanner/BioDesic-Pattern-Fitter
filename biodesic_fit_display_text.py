import pygame, sys, collections
from pygame.locals import *

class DisplayData():

    def __init__(self, surface, position=[0, 0, 0]):
        self.box_grey = (150, 150, 150)
        self.text_colour = (0, 0, 0)
        self.box_edge_grey_offset = -50
        self.box_edge_grey = list(map(lambda a: a + self.box_edge_grey_offset, self.box_grey))
        self.surface = surface
        self.position = position
        self.font = pygame.font.match_font('dejavusans')
        self.font_size = 13
        self.large_font_size = 18
        self.screen_height = self.surface.get_height()
        self.screen_width = self.surface.get_width()
        self.display_quit = False
        self.text_boxes = {}
        self.overlay_surface = self.new_surface(150)
        self.quit_surface = self.new_surface(255)
        self._init_text_values()
        self.add_text_data()
        self.draw_text_boxes()
        

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
        self.draw_text_boxes()

    def update_value(self, name, value):
        if isinstance(value, (list, tuple)):
            value = list(map(lambda a: round(a, 0), value))
            value = str(value).strip('[]()')
        elif isinstance(value, float):
            value = int(value)

        self.text_items[name]['args'] = [value]
        self.add_text_data()

    def show_quit(self, show):
        self.display_quit = show

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

    def _update_screen(self):
        self.screen_height = self.surface.get_height()
        self.screen_width = self.surface.get_width()

    def draw_text_boxes(self):
        # TODO make this moveable
        self._update_screen()
        position = self.position[:]
        # max_x, max_y = self.surface.get_size()
        # position[0] = position[0] if position[0] + self.max_width < max_x else position[0] - self.max_width
        # position[1] = position[1] if position[1] + self.max_width < max_y else position[1] - self.max_height
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
        
        if self.display_quit == True:
            self.quit_screen()
        # self.max_height = position[1]

    
    def draw_box(self, bounding_box, surface=None, fill_colour=None):
        box_coords = self.get_rect_points(bounding_box)
        if fill_colour is None:
            fill_colour = self.box_grey
        if surface is None:
            surface = self.surface
        pygame.draw.rect(surface, fill_colour, bounding_box)
        pygame.draw.lines(surface, self.box_edge_grey, True, box_coords)

    def new_surface(self, alpha=100):
        child_surface = pygame.Surface((self.screen_width, self.screen_height))
        child_surface.set_alpha(alpha)                # alpha level
        child_surface.fill((255, 255, 255))

        return child_surface

    def _quit_text(self, text, screen_coord, text_colour, fill_colour=None):
        if type(text) != 'str':
            text = str(text)
        if fill_colour is None:
            fill_colour = self.box_grey
        fontobj = pygame.font.Font(self.font, self.large_font_size)
        text_obj = fontobj.render(text, True, text_colour, fill_colour)
        text_surf = text_obj.get_rect()
        text_surf.center = ( screen_coord[0], screen_coord[1] )

        return text_obj, text_surf

    def quit_screen(self):
        # TODO - Refactor
        text_pos = [int(self.screen_width / 2), int(self.screen_height / 2)]
        text_obj_1, text_surf_1 = self._quit_text('Would you like to save the new model?', text_pos, self.text_colour)
        text_pos_2 = map(lambda a, b: a + b, text_pos, [0, text_surf_1.height + 20])
        text_obj_2, text_surf_2 = self._quit_text('Enter Y/N or C for cancel', text_pos_2, self.text_colour)
        box_width = max([text_surf_1.width, text_surf_2.width])
        box_height = list(map(lambda a, b: a - b, text_surf_2.bottomright, text_surf_1.topleft))[1]
        box = pygame.Rect(text_surf_1.topleft, (box_width, box_height))
        box = box.inflate(30, 40)
    
        self.surface.blit(self.overlay_surface, (0, 0))
        self.draw_box(box, self.surface)
        self.surface.blit(text_obj_1, text_surf_1)
        self.surface.blit(text_obj_2, text_surf_2)
        
    
    def text3(self, text, screen_coord, colour):
        text = str(text)
        fontobj = pygame.font.Font(self.font, self.font_size)
        textobj = fontobj.render(text, True, colour, self.box_grey)
        text_surf = textobj.get_rect()
        text_surf.topleft = ((20 + screen_coord[0]), (20 + screen_coord[1]))

        self.surface.blit(textobj, text_surf)

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



