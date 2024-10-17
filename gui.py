import stddraw
import pygame
from compass import _os
from picture import Picture

global window_size
window_size = 800
global frame_show_ms 
frame_show_ms = 200
global map_size

RES_PATH = "./res/"
global font
font_path = f"{RES_PATH}PixelSquare10.ttf"

# Image assets
flower_image = Picture(f"{RES_PATH}Flower.png")
bee_image = Picture(f"{RES_PATH}Bee.png")
desert_bee_image = Picture(f"{RES_PATH}DesertBee.png")
scout_image = Picture(f"{RES_PATH}Scout.png")
forager_image = Picture(f"{RES_PATH}Forager.png")
wasp_image = Picture(f"{RES_PATH}Wasp.png")
hive_image = Picture(f"{RES_PATH}Hive.png")
desert_hive_image = Picture(f"{RES_PATH}DesertHive.png")
honey_hive_image = Picture(f"{RES_PATH}HoneyHive.png")
wasp_hive_image = Picture(f"{RES_PATH}WaspHive.png")

# Copies of original surfaces
flower_surf = flower_image._surface.copy()
bee_surf = bee_image._surface.copy()
desert_bee_surf = desert_bee_image._surface.copy()
scout_surf = scout_image._surface.copy()
forager_surf = forager_image._surface.copy()
wasp_surf = wasp_image._surface.copy()
hive_surf = hive_image._surface.copy()
desert_hive_surf = desert_hive_image._surface.copy()
honey_hive_surf = honey_hive_image._surface.copy()
wasp_hive_surf = wasp_hive_image._surface.copy()

def init_gui(_map_size):
    """
    initialize gui window attributes and show main menu
    """
    global window_size
    global map_size 
    map_size = _map_size
    
    stddraw.setCanvasSize(window_size, window_size)
    stddraw.setXscale(0, window_size)
    stddraw.setYscale(0, window_size)
    
    show_menu()
    
    # Scale for gameplay
    border = window_size/(map_size + 2)
    square_size = (window_size - border) / map_size
    scale_images(square_size)    

def _refresh_menu(window_size, font_size):
    global font
    
    stddraw.clear(stddraw.DARK_GREEN)
    stddraw.setPenColor(stddraw.WHITE)

    # Title
    font = pygame.font.Font(font_path, font_size)
    text = font.render("FORAGING SIMULATOR", 0, pygame.Color("white"))
    rect = text.get_rect(center=(window_size/2, font_size))
    stddraw._surface.blit(text, rect)
    
    # Objects
    names_y = window_size/6
    font = pygame.font.Font(font_path, font_size//2)
    text = font.render("Flower   Hive   DesertHive   HoneyHive   WaspHive", 0, pygame.Color("white"))
    stddraw._surface.blit(text, text.get_rect(center=(window_size/2, names_y)))
    size = flower_image.width()
    y = window_size - names_y - 0.75*size
    
    # Magic numbers but position is dependent on scale :o
    stddraw.picture(flower_image, 1.5 * size/2, y)
    stddraw.picture(hive_image, 4.6*size/2, y)
    stddraw.picture(desert_hive_image, 8.25*size/2, y)
    stddraw.picture(honey_hive_image, 13.1*size/2, y)
    stddraw.picture(wasp_hive_image, 17.75*size/2, y)
    
    text = font.render("Bee    DesertBee    Forager    Scout    Wasp", 0, pygame.Color("white"))
    stddraw._surface.blit(text, text.get_rect(center=(window_size/2, names_y + 2*size)))
    y = window_size - names_y - 2*size - 0.75*size   
    
    stddraw.picture(bee_image, 2 * size/2, y)
    stddraw.picture(desert_bee_image, 5.75*size/2, y)
    stddraw.picture(forager_image, 10.4*size/2, y)
    stddraw.picture(scout_image, 14.3*size/2, y)
    stddraw.picture(wasp_image, 17.6*size/2, y)    

    # info text
    stddraw.setFontSize(font_size//2)
    stddraw.text(window_size/5,  font_size/2, "Mouse click/Space to Pause")
    stddraw.text(5*window_size/6,  font_size/2, "+/- to resize window")

def show_menu():
    """
    show the main menu and return when start is pressed
    """
    global frame_show_ms
    global window_size
    global font
    speed_step = 50

    # refresh static menu
    font_size = window_size//16
    font = pygame.font.Font(font_path, font_size)
    scale_images(window_size/10) # Scale for menu
    _refresh_menu(window_size, font_size)
    
    white = pygame.Color("white")
    red = pygame.Color("red")
    blue = pygame.Color("blue")
    button_green = stddraw.color.Color(0, 20, 0)
    button_hovered_green = stddraw.color.Color(0, 60, 0)
    while True:
        mouse_pressed = stddraw.mousePressed()
        start = False
        mouse_pos = pygame.mouse.get_pos()
        start_button_color = button_green
        plus_button_color = button_green
        minus_button_color = button_green
        
        # ---key-input---
        if stddraw.hasNextKeyTyped():
            key_typed = stddraw.nextKeyTyped()
        else:
            key_typed = None      
        
        if _handle_resize(key_typed):
            font_size = window_size//16
            font = pygame.font.Font(font_path, font_size)
            scale_images(window_size/10)
            _refresh_menu(window_size, font_size)
        
        # Start button
        button_y = 8*window_size/12; button_height = window_size/6
        button_rect = pygame.Rect(window_size/2 - window_size/4, button_y + button_height/2, window_size/2, button_height)
        font = pygame.font.Font(font_path, int(font_size))
        button_text = font.render("START", 0, pygame.Color("white"))
        
        # ---Game-speed-setting---
        # color based on speed
        speed_text_red = frame_show_ms > 800
        if speed_text_red:
            speed_text_color = red
            alpha = max(120,min(frame_show_ms*255//5000, 255))
        else: 
            speed_text_color = blue
            alpha = max(120, (800-frame_show_ms)*255//400)
            
        font = pygame.font.Font(font_path, int(font_size*0.75))
        text_plus = font.render("+", 0, white)
        text_minus = font.render("-", 0, white)
        speed_text = font.render(f"Frame speed: ", 0, white)
        speed_value_text = font.render(f"{frame_show_ms}ms", 0, speed_text_color)
        speed_value_text.set_alpha(alpha)
        rect = speed_text.get_rect(center=(window_size*0.3, button_rect.top - 2*font_size))
        speed_value_rect = speed_value_text.get_rect(left=rect.right, centery=rect.centery)
        
        speed_text_area_rect = pygame.Rect(0, rect.top - font_size/4, 
                                        window_size, rect.height + font_size/2)
        speed_down_rect = pygame.rect.Rect(window_size*0.7 + font_size/2, rect.centery-font_size/2,
                                        font_size, font_size)
        speed_up_rect = pygame.rect.Rect(speed_down_rect.left + speed_down_rect.width + font_size*0.2,
                                        rect.centery-font_size/2, font_size, font_size)
        
        # ---button-input---
        if button_rect.collidepoint(mouse_pos):
            # Darken button 
            start_button_color = button_hovered_green
            if mouse_pressed:
                start = True
        if speed_up_rect.collidepoint(mouse_pos):
            plus_button_color = button_hovered_green
            if mouse_pressed:
                if frame_show_ms == 1:
                    frame_show_ms = speed_step
                else:
                    frame_show_ms = min(frame_show_ms+speed_step, 10000)
        if speed_down_rect.collidepoint(mouse_pos):
            minus_button_color = button_hovered_green
            if mouse_pressed:
                frame_show_ms -= speed_step
                if frame_show_ms <= 0:
                    frame_show_ms = 1 
        
        # Start Button Drawing
        stddraw.setPenColor(start_button_color)
        stddraw.filledRectangle(button_rect.left, window_size - button_rect.bottom, button_rect.width, button_rect.height)
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.rectangle(button_rect.left, window_size - button_rect.bottom, button_rect.width, button_rect.height)
        stddraw._surface.blit(button_text, button_text.get_rect(center=button_rect.center))

        # Speed setting drawing
        pygame.draw.rect(stddraw._surface, stddraw._pygameColor(stddraw.DARK_GREEN), speed_text_area_rect)
        rect = speed_text.get_rect(center=(window_size*0.3, button_rect.top - 2*font_size))
        stddraw._surface.blit(speed_text, rect)
        stddraw._surface.blit(speed_value_text, speed_value_rect)

        stddraw.setPenColor(minus_button_color)
        stddraw.filledSquare(speed_down_rect.centerx, window_size-speed_down_rect.centery,speed_down_rect.width//2)
        stddraw._surface.blit(text_minus, text_minus.get_rect(center=speed_down_rect.center))
        stddraw.setPenColor(plus_button_color)
        stddraw.filledSquare(speed_up_rect.centerx, window_size-speed_up_rect.centery, speed_up_rect.width//2)
        stddraw._surface.blit(text_plus, text_plus.get_rect(center=speed_up_rect.center))
        
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.square(speed_down_rect.centerx, window_size-speed_down_rect.centery,speed_down_rect.width//2)
        stddraw.square(speed_up_rect.centerx, window_size-speed_up_rect.centery,speed_up_rect.width//2)

        stddraw.show(1)
        if start or key_typed and key_typed == ' ':
            return

def scale_images(size):
    flower_image._surface = pygame.transform.scale(flower_surf, (size, size))
    bee_image._surface = pygame.transform.scale(bee_surf, (size, size))
    desert_bee_image._surface = pygame.transform.scale(desert_bee_surf, (size, size))
    scout_image._surface = pygame.transform.scale(scout_surf, (size, size))
    forager_image._surface = pygame.transform.scale(forager_surf, (size, size))
    wasp_image._surface = pygame.transform.scale(wasp_surf, (size, size))
    hive_image._surface = pygame.transform.scale(hive_surf, (size, size))
    desert_hive_image._surface = pygame.transform.scale(desert_hive_surf, (size, size))
    honey_hive_image._surface = pygame.transform.scale(honey_hive_surf, (size, size))
    wasp_hive_image._surface = pygame.transform.scale(wasp_hive_surf, (size, size))
    
def show_result(result: str, bees_killed, pollen_action, map_board, hidden_entities):
    global window_size
    global font
    global map_size

    font_size = window_size//20
    result_font_size = font_size
    render_frame(map_board, hidden_entities, False)
    if pollen_action == "sort":
        lines = result.count("\n")
        if lines * font_size > window_size:
            result_font_size = window_size//lines
    font = pygame.font.Font(font_path, font_size)
    
    # Darken screen
    surf = pygame.Surface((window_size, window_size))
    surf.fill(pygame.color.Color(0, 0, 0))
    surf.set_alpha(200)
    stddraw._surface.blit(surf, (0,0))
    
    # result text
    border = window_size/(map_size + 2)
    c = pygame.Color("white")
    start_y = (window_size/20)
    start_x = border + window_size/5
    
    tokens = result.split("\n")
    tokens[0] = tokens[0].upper()
    text = font.render(tokens[0], 0, c)
    rect = text.get_rect(center=(start_x, start_y))
    stddraw._surface.blit(text, rect)
    
    x = rect.left
    y = start_y + font_size*1.1
    font = pygame.font.Font(font_path, int(result_font_size*0.75))
    for i, line in enumerate(tokens[1:]):
        text = font.render(line, 0, c)
        rect = text.get_rect(left=x, centery= y  + i * result_font_size + 2)
        stddraw._surface.blit(text, rect)
    
    # Bee kills
    font = pygame.font.Font(font_path, font_size)
    
    text = font.render("KILLS:", 0, c)
    rect = text.get_rect(center=(window_size - start_x, start_y))
    stddraw._surface.blit(text, rect)
    
    text = font.render(f"{bees_killed}", 0, c)
    rect = text.get_rect(center=(window_size - start_x, start_y + font_size*1.25))
    stddraw._surface.blit(text, rect)
    
    stddraw.show()
 
def render_frame(map_board, hidden_entities, show=True):
    """
    render the given board as a frame and wait for time set by frame_show_ms
    """
    global frame_show_ms
    global window_size
    global map_size
    
    border = window_size/(map_size + 2) # Set border for numbering
    square_size = (window_size - border) / map_size # size of squares based on map size

    stddraw.clear(stddraw.DARK_GREEN)
    draw_grid(map_size, border, square_size)
    
    for row in range(map_size):
        for col in range(map_size):
            if map_board[row][col] is None:
                continue
            image = get_image(map_board[row][col])
            x = border + (col * square_size) + square_size/2
            y = border + (row * square_size) + square_size/2
            
            if not image is None:
                size = image.width()
                if not (row, col) in hidden_entities:
                    stddraw.picture(image, x, y)
                else:
                    for i, char in enumerate(hidden_entities[(row, col)]):
                        stddraw.picture(get_image(char), x + i*size/16, y)
            # character was 'm'
            else:
                image = get_image(hidden_entities[(row, col)][0])
                size = image.width()
                for i, char in enumerate(hidden_entities[(row, col)]):
                        image = get_image(char)
                        img_cpy = Picture(size, size)
                        img_cpy._surface = pygame.transform.rotate(image._surface, i * 90)
                        stddraw.picture(img_cpy, x, y)
                
    if show:
        stddraw.show(frame_show_ms)

def draw_grid(map_size, border, square_size):
    # Col numbering
    global window_size
    global font
    font = pygame.font.Font(font_path, int(border/2) + 2)
    white = pygame.Color("white")

    for col in range(map_size):
        y = window_size - border/2
        x = border + (col * square_size) + square_size/2
        text = font.render(f"{col}", 0, white)
        stddraw._surface.blit(text, text.get_rect(center=(x, y)))
    
    for row in range(map_size):
        # Row numbering
        stddraw.setPenColor(stddraw.WHITE)
        y = window_size - border - (row * square_size) - square_size/2
        x = border/2
        text = font.render(f"{row}", 0, white)
        stddraw._surface.blit(text, text.get_rect(center=(x, y)))
        for col in range(map_size):
            x = border + (col * square_size) + square_size/2
            y = border + (row * square_size) + square_size/2
            c = stddraw.GREEN if (row + col) % 2 == 0 else stddraw.DARK_GREEN

            stddraw.setPenColor(c)
            stddraw.filledSquare(x, y, square_size/2)
    
    stddraw.setPenColor(stddraw.BLACK)
    stddraw.setPenRadius(square_size//20)
    stddraw.line(border, border, border, window_size)
    stddraw.line(border, border, window_size, border)

def get_image(char):
    """
    returns image based on character representation
    """
    if char == 'b':
        return bee_image
    if char == 'd':
        return desert_bee_image
    if char == 'f':
        return forager_image
    if char == 's':
        return scout_image
    if char == 'w':
        return wasp_image
    if char == 'm':
        return None
    if char == 'F':
        return flower_image
    if char == 'B':
        return hive_image
    if char == 'D':
        return desert_hive_image
    if char == 'H':
        return honey_hive_image
    if char == 'W':
        return wasp_hive_image
    
def handle_input():
    # Pause
    if stddraw.hasNextKeyTyped():
        key_pressed = stddraw.nextKeyTyped()
    else:
        key_pressed = None
    if stddraw.mousePressed() or (key_pressed and key_pressed == ' '):
        stddraw.show(10)
        while not stddraw.mousePressed() and not(stddraw.hasNextKeyTyped() and stddraw.nextKeyTyped() == ' '):
            stddraw.show(10)
      
def _handle_resize(key_pressed):
    global window_size
    global map_size
    resize_step = 50

    # Window resize
    if key_pressed and key_pressed == '=':
        # set background to new instance of display
        window_size = min(window_size + resize_step, 1050)
        stddraw._background = pygame.display.set_mode((window_size,window_size))
        stddraw._surface = pygame.Surface((window_size, window_size))
        stddraw._canvasWidth, stddraw._canvasHeight = window_size, window_size

        # resize scale and images
        border = window_size/(map_size + 2)
        square_size = (window_size - border) / map_size
        stddraw.setXscale(0, window_size)
        stddraw.setYscale(0, window_size)
        scale_images(square_size)
        return True
    elif key_pressed and key_pressed == '-':
        # set background to new instance of display
        window_size = max(window_size - resize_step, 100)
        stddraw._background = pygame.display.set_mode((window_size,window_size))
        stddraw._surface = pygame.Surface((window_size, window_size))
        stddraw._canvasWidth, stddraw._canvasHeight = window_size, window_size
        
        # resize scale and images
        border = window_size/(map_size + 2)
        square_size = (window_size - border) / map_size
        stddraw.setXscale(0, window_size)
        stddraw.setYscale(0, window_size)
        scale_images(square_size)
        return True
    
    return False
          
def set_window_title(string):
    stddraw.pygame.display.set_caption(string)




