# -*-coding:utf-8-*-
# PYTRIS™ Copyright (c) 2017 Jason Kim All Rights Reserved.

from contextlib import nullcontext
import pygame
import operator
from mino import *
from random import *
from pygame.locals import *


# Define
block_size = 17 # Height, width of single block
width = 10 # Board에 가로로 들어갈 블럭의 개수
height = 20 # Board에 세로로 들어갈 블럭의 개수
framerate = 30 # Bigger -> Slower

board_width = 800  # 전체 창의 가로 길이
board_height = 450 # 전체 창의 세로 길이

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)
pygame.time.set_timer(pygame.USEREVENT, framerate * 10)
pygame.display.set_caption("PYTRIS™")

initialize = True # Start Screen 에서 set_initial_values()로 초기화할지 여부를 boolean으로 저장

class ui_variables:
    # Fonts
    font_path = "assets/fonts/OpenSans-Light.ttf"
    font_path_b = "assets/fonts/OpenSans-Bold.ttf"
    font_path_i = "assets/fonts/Inconsolata/Inconsolata.otf"


    h1 = pygame.font.Font(font_path, 50)
    h2 = pygame.font.Font(font_path, 30)
    h4 = pygame.font.Font(font_path, 20)
    h5 = pygame.font.Font(font_path, 13)
    h6 = pygame.font.Font(font_path, 10)

    h1_b = pygame.font.Font(font_path_b, 50)
    h2_b = pygame.font.Font(font_path_b, 30)

    h2_i = pygame.font.Font(font_path_i, 30)
    h5_i = pygame.font.Font(font_path_i, 13)

    # Sounds
    click_sound = pygame.mixer.Sound("assets/sounds/SFX_ButtonUp.wav")
    move_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceMoveLR.wav")
    drop_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceHardDrop.wav")
    single_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearSingle.wav")
    double_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearDouble.wav")
    triple_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearTriple.wav")
    tetris_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialTetris.wav")

    # Background colors
    black = (10, 10, 10) #rgb(10, 10, 10)
    black_pause = (0, 0, 0, 127)
    real_white = (255, 255, 255) #rgb(255, 255, 255)
    white = (211, 211, 211) #rgb(211, 211, 211) ##연회색
    grey_1 = (26, 26, 26) #rgb(26, 26, 26)
    grey_2 = (35, 35, 35) #rgb(35, 35, 35)
    grey_3 = (55, 55, 55) #rgb(55, 55, 55)

    

    # Tetrimino colors
    cyan = (69, 206, 204) #rgb(69, 206, 204) # I
    blue = (64, 111, 249) #rgb(64, 111, 249) # J
    orange = (253, 189, 53) #rgb(253, 189, 53) # L
    yellow = (246, 227, 90) #rgb(246, 227, 90) # O
    green = (98, 190, 68) #rgb(98, 190, 68) # S
    pink = (242, 64, 235) #rgb(242, 64, 235) # T
    red = (225, 13, 27) #rgb(225, 13, 27) # Z

    t_color = [grey_2, cyan, blue, orange, yellow, green, pink, red, grey_3]


#각 이미지 주소
background_image = 'assets/images/background_image.png' #메뉴화면(첫 화면) 배경
gamebackground_image_nyc = 'assets/images/background_nyc.png' #게임 배경화면 : 기본값 뉴욕
pause_board_image = 'assets/vector/pause_board.png'

select_mode_button_image = 'assets/vector/select_mode_button.png'
clicked_select_mode_button_image = 'assets/vector/clicked_select_mode_button.png'

setting_button_image = 'assets/vector/settings_button.png'
clicked_setting_button_image = 'assets/vector/clicked_settings_button.png'

score_board_button_image = 'assets/vector/score_board_button.png'
clicked_score_board_button_image = 'assets/vector/clicked_score_board_button.png'

quit_button_image = 'assets/vector/quit_button.png'
clicked_quit_button_image = 'assets/vector/clicked_quit_button.png'


single_button_image = 'assets/vector/easy_button.png'
clicked_single_button_image = 'assets/vector/clicked_easy_button.png'

hard_button_image = 'assets/vector/hard_button.png'
clicked_hard_button_image = 'assets/vector/clicked_hard_button.png'

pvp_button_image = 'assets/vector/multi_button.png'
clicked_pvp_button_image = 'assets/vector/clicked_multi_button.png'


hard_tutorial_button_image = 'assets/vector/hard_tutorial_button.png'
clicked_hard_tutorial_button_image = 'assets/vector/clicked_hard_tutorial_button.png'

multi_tutorial_button_image = 'assets/vector/multi_tutorial_button.png'
clicked_multi_tutorial_button_image = 'assets/vector/clicked_multi_tutorial_button.png'


'''







help_button_image = 'assets/vector/help_button.png'
clicked_help_button_image = 'assets/vector/clicked_help_button.png'



gravity_button_image = 'assets/vector/gravity_button.png'
clicked_gravity_button_image = 'assets/vector/clicked_gravity_button.png'





setting_vector = 'assets/vector/setting_vector.png'
clicked_setting_vector = 'assets/vector/clicked_setting_vector.png'


setting_board_image = 'assets/vector/setting_board.png'
gameover_board_image = 'assets/vector/gameover_board.png'
gameover_image = 'assets/vector/gameover.png'

smallsize_board = 'assets/vector/screensize1.png'
midiumsize_board = 'assets/vector/screensize2.png'
bigsize_board = 'assets/vector/screensize3.png'

mute_button_image = 'assets/vector/allmute_button.png'
default_button_image = 'assets/vector/default_button.png'

number_board = 'assets/vector/number_board.png'

resume_button_image = 'assets/vector/resume_button.png'
clicked_resume_button_image = 'assets/vector/clicked_resume_button.png'

restart_button_image = 'assets/vector/restart_button.png'
clicked_restart_button_image = 'assets/vector/clicked_restart_button.png'




back_button_image = 'assets/vector/back_button.png'
clicked_back_button_image = 'assets/vector/clicked_back_button.png'

volume_vector = 'assets/vector/volume_vector.png'
clicked_volume_vector = 'assets/vector/clicked_volume_vector.png'

keyboard_vector = 'assets/vector/keyboard_vector.png'
clicked_keyboard_vector = 'assets/vector/clicked_keyboard_vector.png'

screen_vector = 'assets/vector/screen_vector.png'
clicked_screen_vector = 'assets/vector/clicked_screen_vector.png'

menu_button_image = 'assets/vector/menu_button.png'
clicked_menu_button_image = 'assets/vector/clicked_menu_button.png'

ok_button_image = 'assets/vector/ok_button.png'
clicked_ok_button_image = 'assets/vector/clicked_ok_button.png'

plus_button_image = 'assets/vector/plus_button.png'
clicked_plus_button_image = 'assets/vector/clicked_plus_button.png'

minus_button_image = 'assets/vector/minus_button.png'
clicked_minus_button_image = 'assets/vector/clicked_minus_button.png'
#음소거 추가#
sound_off_button_image = 'assets/vector/sound_off_button.png'
sound_on_button_image = 'assets/vector/sound_on_button.png'

check_button_image = 'assets/vector/checkbox_button.png'
clicked_check_button_image = 'assets/vector/clicked_checkbox_button.png'

pvp_win_image = 'assets/vector/pvp_win.png'
pvp_lose_image = 'assets/vector/pvp_lose.png'
'''

class button(): #버튼객체
    def __init__(self, board_width, board_height, x_rate, y_rate, width_rate, height_rate, img=''): #버튼생성
        self.x = board_width * x_rate #버튼 x좌표 (버튼이미지의 정중앙)
        self.y = board_height * y_rate #버튼 y좌표 (버튼이미지의 정중앙)
        self.width = int(board_width * width_rate) #버튼 너비
        self.height = int(board_height * height_rate) #버튼 높이
        self.x_rate = x_rate #board_width * x_rate = x좌표
        self.y_rate = y_rate #board_height * y_rate = y좌표
        self.width_rate = width_rate #board_width * width_rate = 버튼 너비
        self.height_rate = height_rate #board_height * height_rate = 버튼 높이
        self.image = img #불러올 버튼 이미지

    def change(self, board_width, board_height): #버튼 위치, 크기 바꾸기
        self.x = board_width * self.x_rate #x좌표
        self.y = board_height * self.y_rate #y좌표
        self.width = int(board_width * self.width_rate) #너비
        self.height = int(board_height * self.height_rate) #높이

    def draw(self, win, outline=None): #버튼 보이게 만들기
        if outline:
            draw_image(screen, self.image, self.x, self.y, self.width, self.height)

    def isOver(self, pos): #마우스의 위치가 버튼이미지 위에 있는지 확인  (pos[0]은 마우스 x좌표, pos[1]은 마우스 y좌표)
        if pos[0] > self.x - (self.width / 2) and pos[0] < self.x + (self.width / 2):
            if pos[1] > self.y - (self.height / 2) and pos[1] < self.y + (self.height / 2):
                return True
        return False

    def isOver_2(self, pos): #start 화면에서 single,pvp,help,setting을 위해서 y좌표 좁게 인식하도록
        if pos[0] > self.x - (self.width / 2) and pos[0] < self.x + (self.width / 2):
            if pos[1] > self.y - (self.height / 4) and pos[1] < self.y + (self.height / 4):#243줄에서의 2을 4로 바꿔주면서 좁게 인식할수 있도록함. 더 좁게 인식하고 싶으면 숫자 늘려주기#
                return True
        return False

# 메뉴 버튼 테스트용

select_mode_button = button(board_width, board_height, 0.2, 0.2, 0.22, 0.2, select_mode_button_image)
setting_button = button(board_width, board_height, 0.2, 0.8, 0.22, 0.2, setting_button_image)
quit_button = button(board_width, board_height, 0.8, 0.8, 0.22, 0.2, quit_button_image)
score_board_button = button(board_width, board_height, 0.8, 0.2, 0.22, 0.2, score_board_button_image)

single_button = button(board_width,board_height, 0.3, 0.55, 0.22, 0.2, single_button_image)
hard_button = button(board_width, board_height, 0.5, 0.55, 0.22, 0.2, hard_button_image)
pvp_button = button(board_width, board_height, 0.7, 0.55, 0.22, 0.2, pvp_button_image)

pause_quit_button = button(board_width, board_height, 0.5, 0.83, 0.17, 0.2, quit_button_image)
pause_setting_button = button(board_width, board_height, 0.5, 0.63, 0.17, 0.2, setting_button_image)

'''    
    #버튼객체 생성 class Button에서 확인
#def __init__(self, board_width, board_height, x_rate, y_rate, width_rate, height_rate, img='')
#(현재 보드너비, 현재보드높이, 버튼의 x좌표 위치비율, 버튼의 y좌표 위치비율, 버튼의 너비 길이비율, 버튼의 높이 길이비율) - 전체화면 크기에 대한 비율

mute_button = button(board_width, board_height, 0.5, 0.27, 0.25, 0.45, mute_button_image)
default_button = button(board_width, board_height, 0.5, 0.27, 0.25, 0.45, default_button_image)


help_button = button(board_width, board_height, 0.12, 0.8, 0.235, 0.435, help_button_image)

gravity_button = button(board_width, board_height, 0.58, 0.55, 0.235, 0.435, gravity_button_image)
timeattack_button = button(board_width, board_height, 0.58, 0.8, 0.235, 0.435, timeattack_button_image)
setting_icon = button(board_width, board_height, 0.9, 0.85, 0.10, 0.15, setting_vector)
leaderboard_icon = button(board_width, board_height, 0.77, 0.85, 0.15, 0.2, leaderboard_vector)

resume_button = button(board_width, board_height, 0.5, 0.23, 0.15, 0.35, resume_button_image)
restart_button = button(board_width, board_height, 0.5, 0.43, 0.15, 0.35, restart_button_image)



back_button = button(board_width, board_height, 0.5, 0.85, 0.15, 0.35, back_button_image)
volume_icon = button(board_width, board_height, 0.4, 0.5, 0.12, 0.23, volume_vector)
screen_icon = button(board_width, board_height, 0.6, 0.5, 0.12, 0.23, screen_vector)
ok_button = button(board_width, board_height, 0.5, 0.83, 0.15, 0.35, ok_button_image)

volume = 1.0

menu_button = button(board_width, board_height, 0.5, 0.23, 0.15, 0.35, menu_button_image)
gameover_quit_button = button(board_width, board_height, 0.5, 0.43, 0.15, 0.35, quit_button_image)

effect_plus_button = button(board_width, board_height, 0.37, 0.73, 0.0625, 0.1111, plus_button_image)
effect_minus_button = button(board_width, board_height, 0.52, 0.73, 0.0625, 0.1111, minus_button_image)

sound_plus_button = button(board_width, board_height, 0.37, 0.53, 0.0625, 0.1111, plus_button_image)
sound_minus_button = button(board_width, board_height, 0.52, 0.53, 0.0625, 0.1111, minus_button_image)
level_plus_button = button(board_width, board_height, 0.63, 0.7719, 0.0625, 0.1111, plus_button_image)
level_minus_button = button(board_width, board_height, 0.56, 0.7719, 0.0625, 0.1111, minus_button_image)
combo_plus_button = button(board_width, board_height, 0.63, 0.9419, 0.0625, 0.1111, plus_button_image)
combo_minus_button =button(board_width, board_height, 0.56, 0.9419, 0.0625, 0.1111, minus_button_image)
speed_plus_button = button(board_width, board_height, 0.18, 0.12, 0.055, 0.09, plus_button_image)
speed_minus_button =button(board_width, board_height, 0.035, 0.12, 0.055, 0.09, minus_button_image)

#음소거 추가#
effect_sound_off_button = button(board_width, board_height, 0.65, 0.73, 0.08, 0.15, sound_off_button_image)
music_sound_off_button = button(board_width, board_height, 0.65, 0.53, 0.08, 0.15, sound_off_button_image)
effect_sound_on_button = button(board_width, board_height, 0.65, 0.73, 0.08, 0.15, sound_on_button_image)
music_sound_on_button = button(board_width, board_height, 0.65, 0.53, 0.08, 0.15, sound_on_button_image)

mute_check_button = button(board_width, board_height, 0.2, 0.4, 0.0625, 0.1111, check_button_image)
smallsize_check_button = button(board_width, board_height, 0.5, 0.25, 0.1875, 0.1444, smallsize_board)
midiumsize_check_button = button(board_width, board_height, 0.5, 0.45, 0.1875, 0.1444, midiumsize_board)
bigsize_check_button = button(board_width, board_height, 0.5, 0.65, 0.1875, 0.1444, bigsize_board)

#게임 중 버튼 생성하기위한 버튼객체 리스트 (버튼 전체)
button_list = [mute_button, default_button, single_button, pvp_button, help_button, quit_button, gravity_button, timeattack_button, resume_button, restart_button, setting_button, pause_quit_button, back_button,
        ok_button, menu_button, gameover_quit_button, effect_plus_button, effect_minus_button, sound_plus_button, sound_minus_button, level_plus_button,
        effect_sound_off_button, music_sound_off_button, effect_sound_on_button, music_sound_on_button, mute_check_button, smallsize_check_button, midiumsize_check_button, bigsize_check_button,
        setting_icon, leaderboard_icon, volume_icon, screen_icon, level_minus_button, combo_minus_button, combo_plus_button, speed_minus_button, speed_plus_button]
'''

# 이미지 화면에 띄우기 (매개변수 x, y가 이미지의 정중앙 좌표)
def draw_image(window, img_path, x, y, width, height):
    x = x - (width / 2) #해당 이미지의 가운데 x좌표, 가운데 좌표이기 때문에 2로 나눔
    y = y - (height / 2) #해당 이미지의 가운데 y좌표, 가운데 좌표이기 때문에 2로 나눔
    image = pygame.image.load(img_path)
    image = pygame.transform.smoothscale(image, (width, height))
    window.blit(image, (x, y))    

# Draw block
def draw_block(x, y, color):
    #사각형 내부 색 color로 지정
    pygame.draw.rect(
        screen,
        color,
        Rect(x, y, block_size, block_size)
    )
    #사각형 테두리 
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        Rect(x, y, block_size, block_size),
        1
    )

# Draw game screen
def draw_board(next, next2, hold, score, level, goal):
    screen.fill(ui_variables.grey_1)

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.white,
        Rect(204, 0, 96, 374)
    )

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]

    for i in range(4):
        for j in range(4):
            dx = 220 + block_size * j
            dy = 140 + block_size * i
            if grid_n[i][j] != 0:
                pygame.draw.rect(
                    screen,
                    ui_variables.t_color[grid_n[i][j]],
                    Rect(dx, dy, block_size, block_size)
                )

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for i in range(4):
            for j in range(4):
                dx = 220 + block_size * j
                dy = 50 + block_size * i
                if grid_h[i][j] != 0:
                    pygame.draw.rect(
                        screen,
                        ui_variables.t_color[grid_h[i][j]],
                        Rect(dx, dy, block_size, block_size)
                    )

    # Set max score
    if score > 999999:
        score = 999999

    # Draw texts
    text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.black)
    text_next = ui_variables.h5.render("NEXT", 1, ui_variables.black)
    text_score = ui_variables.h5.render("SCORE", 1, ui_variables.black)
    score_value = ui_variables.h4.render(str(score), 1, ui_variables.black)
    text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.black)
    level_value = ui_variables.h4.render(str(level), 1, ui_variables.black)
    text_goal = ui_variables.h5.render("GOAL", 1, ui_variables.black)
    goal_value = ui_variables.h4.render(str(goal), 1, ui_variables.black)

    # Place texts
    screen.blit(text_hold, (215, 14))
    screen.blit(text_next, (215, 104))
    screen.blit(text_score, (215, 194))
    screen.blit(score_value, (220, 210))
    screen.blit(text_level, (215, 254))
    screen.blit(level_value, (220, 270))
    screen.blit(text_goal, (215, 314))
    screen.blit(goal_value, (220, 330))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = 17 + block_size * x
            dy = 17 + block_size * y
            draw_block(dx, dy, ui_variables.t_color[matrix[x][y + 1]])

def draw_multiboard():
    screen.fill(ui_variables.real_white)
    # 22.05.04 pause화면 구현 위해 임시로 작성했습니다.

# Draw a tetrimino
def draw_mino(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    tx, ty = x, y
    while not is_bottom(tx, ty, mino, r):
        ty += 1

    # Draw ghost
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix[tx + j][ty + i] = 8

    # Draw mino
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix[x + j][y + i] = grid[i][j]

# Erase a tetrimino
def erase_mino(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    # Erase ghost
    for j in range(21):
        for i in range(10):
            if matrix[i][j] == 8:
                matrix[i][j] = 0

    # Erase mino
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix[x + j][y + i] = 0

# Returns true if mino is at bottom
def is_bottom(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (y + i + 1) > 20:
                    return True
                elif matrix[x + j][y + i + 1] != 0 and matrix[x + j][y + i + 1] != 8:
                    return True

    return False

# Returns true if mino is at the left edge
def is_leftedge(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j - 1) < 0:
                    return True
                elif matrix[x + j - 1][y + i] != 0:
                    return True

    return False

# Returns true if mino is at the right edge
def is_rightedge(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j + 1) > 9:
                    return True
                elif matrix[x + j + 1][y + i] != 0:
                    return True

    return False

# Returns true if turning right is possible
def is_turnable_r(x, y, mino, r):
    if r != 3:
        grid = tetrimino.mino_map[mino - 1][r + 1]
    else:
        grid = tetrimino.mino_map[mino - 1][0]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j) < 0 or (x + j) > 9 or (y + i) < 0 or (y + i) > 20:
                    return False
                elif matrix[x + j][y + i] != 0:
                    return False

    return True

# Returns true if turning left is possible
def is_turnable_l(x, y, mino, r):
    if r != 0:
        grid = tetrimino.mino_map[mino - 1][r - 1]
    else:
        grid = tetrimino.mino_map[mino - 1][3]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j) < 0 or (x + j) > 9 or (y + i) < 0 or (y + i) > 20:
                    return False
                elif matrix[x + j][y + i] != 0:
                    return False

    return True

# Returns true if new block is drawable
def is_stackable(mino):
    grid = tetrimino.mino_map[mino - 1][0]

    for i in range(4):
        for j in range(4):
            #print(grid[i][j], matrix[3 + j][i])
            if grid[i][j] != 0 and matrix[3 + j][i] != 0:
                return False

    return True

# Initial values
def set_initial_values():
    global combo_count, combo_count_2P, score, level, goal, score_2P, level_2P, goal_2P, bottom_count, bottom_count_2P, hard_drop, hard_drop_2P, attack_point, attack_point_2P, dx, dy, dx_2P, dy_2P, rotation, rotation_2P, mino, mino_2P, next_mino1, next_mino2, next_mino1_2P, hold, hold_2P, hold_mino, hold_mino_2P, framerate, framerate_2P, matrix, matrix_2P, Change_RATE, blink, start, pause, done, game_over, leader_board, setting, volume_setting, screen_setting, pvp, help, gravity_mode, debug, d, e, b, u, g, time_attack, start_ticks, textsize, CHANNELS, swidth, name_location, name, previous_time, current_time, pause_time, lines, leaders, volume, game_status, framerate_blockmove, framerate_2P_blockmove, game_speed, game_speed_2P, select_mode, hard
    framerate = 30 # Bigger -> Slower  기본 블록 하강 속도, 2도 할만 함, 0 또는 음수 이상이어야 함
    framerate_blockmove = framerate * 3 # 블록 이동 시 속도
    game_speed = framerate * 20 # 게임 기본 속도
    framerate_2P = 30 # 2P
    framerate_2P_blockmove = framerate_2P * 3 # 블록 이동 시 속도
    game_speed_2P = framerate_2P * 20 # 2P 게임 기본 속도

    # Initial values
    blink = False
    start = False
    pause = False
    done = False
    game_over = False
    leader_board = False
    setting = False
    volume_setting = False
    screen_setting = False
    pvp = False
    hard = False # 하드모드 변수 추가
    help = False
    select_mode = False
    gravity_mode = False #이 코드가 없으면 중력모드 게임을 했다가 Restart해서 일반모드로 갈때 중력모드로 게임이 진행됨#
    debug = False
    d = False
    e = False
    b = False
    u = False
    g = False
    time_attack = False
    start_ticks = pygame.time.get_ticks()
    textsize = False

    # 게임 음악 속도 조절 관련 변수
    CHANNELS = 1
    swidth = 2
    Change_RATE = 2

    combo_count = 0
    combo_count_2P = 0
    score = 0
    level = 1
    goal = level * 5
    score_2P = 0
    level_2P = 1
    goal_2P = level_2P * 5
    bottom_count = 0
    bottom_count_2P = 0
    hard_drop = False
    hard_drop_2P = False
    attack_point = 0
    attack_point_2P = 0

    dx, dy = 3, 0  # Minos location status
    dx_2P, dy_2P = 3, 0
    rotation = 0  # Minos rotation status
    rotation_2P = 0
    mino = randint(1, 7)  # Current mino #테트리스 블록 7가지 중 하나
    mino_2P = randint(1, 7)
    next_mino1 = randint(1, 7)  # Next mino1 # 다음 테트리스 블록 7가지 중 하나
    next_mino2 = randint(1, 7)  # Next mino2 # 다음 테트리스 블록 7가지 중 하나
    next_mino1_2P = randint(1, 7)
    hold = False  # Hold status
    hold_2P = False
    hold_mino = -1  # Holded mino #현재 hold하는 것 없는 상태
    hold_mino_2P = -1
    textsize = False

    name_location = 0
    name = [65, 65, 65]

    previous_time = pygame.time.get_ticks()
    current_time = pygame.time.get_ticks()
    pause_time = pygame.time.get_ticks()

    with open('leaderboard.txt') as f:
        lines = f.readlines()
    lines = [line.rstrip('\n') for line in open('leaderboard.txt')]  #leaderboard.txt 한줄씩 읽어옴

    leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
    for i in lines:
        leaders[i.split(' ')[0]] = int(i.split(' ')[1])
    leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)

    matrix = [[0 for y in range(height + 1)] for x in range(width)]  # Board matrix
    matrix_2P = [[0 for y in range(height + 1)] for x in range(width)]  # Board matrix

    volume = 1.0 # 필요 없는 코드, effect_volume으로 대체 가능
    ui_variables.click_sound.set_volume(volume) # 필요 없는 코드, 전체 코드에서 click_sound를 effect_volume로 설정하는 코드 하나만 있으면 됨
    pygame.mixer.init()
    '''
    ui_variables.intro_sound.set_volume(music_volume / 10)
    ui_variables.break_sound.set_volume(effect_volume / 10) # 소리 설정 부분도 set_volume 함수에 넣으면 됨
    ui_variables.intro_sound.play()
    '''
    game_status = ''
    '''
    pygame.mixer.music.load("assets/sounds/SFX_BattleMusic.wav")
    '''

set_initial_values()
pygame.time.set_timer(pygame.USEREVENT, 10)


###########################################################
# Loop Start
###########################################################

while not done:
    # Pause screen
    if pause:
        
        if start:
            screen.fill(ui_variables.real_white)
            draw_image(screen, gamebackground_image_nyc , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
            draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
            #화면 회색으로 약간 불투명하게
            pause_surface = screen.convert_alpha() #투명 가능하도록
            pause_surface.fill((0, 0, 0, 0))  #투명한 검정색으로 덮기
            pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(board_width), int(board_height)])  #(screen, 색깔, 위치 x, y좌표, 너비, 높이)
            screen.blit(pause_surface, (0, 0))

        if pvp:
            draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)
            #화면 회색으로 약간 불투명하게
            pause_surface = screen.convert_alpha() #투명 가능하도록
            pause_surface.fill((0, 0, 0, 0)) #투명한 검정색으로 덮기
            pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(board_width), int(board_height)])  #(screen, 색깔, 위치 x, y좌표, 너비, 높이)
            screen.blit(pause_surface, (0, 0))

        draw_image(screen, pause_board_image, board_width * 0.5, board_height * 0.5, int(board_height * 0.7428), board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        #resume_button.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색
        #restart_button.draw(screen, (0, 0, 0))
        pause_setting_button.draw(screen, (0, 0, 0))
        pause_quit_button.draw(screen, (0, 0, 0))
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True

            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                pygame.display.update()
            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation)
                if event.key == K_ESCAPE:
                    pause = False
                    ui_variables.click_sound.play()
                    #pygame.mixer.music.unpause()
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                  
            elif event.type == pygame.MOUSEMOTION:
            #     if resume_button.isOver_2(pos):
            #         resume_button.image = clicked_resume_button_image
            #     else:
            #         resume_button.image = resume_button_image

            #     if restart_button.isOver_2(pos):
            #         restart_button.image = clicked_restart_button_image
            #     else:
            #         restart_button.image = restart_button_image

                if pause_setting_button.isOver_2(pos):
                    pause_setting_button.image = clicked_setting_button_image
                else:
                    pause_setting_button.image = setting_button_image
                if pause_quit_button.isOver_2(pos):
                    pause_quit_button.image = clicked_quit_button_image
                else:
                    pause_quit_button.image = quit_button_image
                pygame.display.update()
            

            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                if pause_quit_button.isOver_2(pos):
                   ui_variables.click_sound.play()
                   done = True
                
                if pause_setting_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    setting = True
                '''
                if restart_button.isOver_2(pos):
                    ui_variables.click_sound.play()

                    pause = False
                    start = False

                    if pvp:
                        pvp = False
                
                if resume_button.isOver_2(pos):
                    pygame.mixer.music.unpause()
                    pause = False
                    ui_variables.click_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, 1) #0.001초
                '''

    # Game screen
    elif start:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                # Set speed
                if not game_over:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_DOWN]:
                        pygame.time.set_timer(pygame.USEREVENT, framerate * 1)
                    else:
                        pygame.time.set_timer(pygame.USEREVENT, framerate * 10)

                # Draw a mino
                draw_mino(dx, dy, mino, rotation)
                draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)

                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation)

                # Move mino down
                if not is_bottom(dx, dy, mino, rotation):
                    dy += 1

                # Create new mino
                else:
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        score += 10 * level
                        draw_mino(dx, dy, mino, rotation)
                        draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                        if is_stackable(next_mino1):
                            mino = next_mino1
                            next_mino1 = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                        else:
                            start = False
                            game_over = True
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count += 1

                # Erase line
                erase_count = 0
                for j in range(21):
                    is_full = True
                    for i in range(10):
                        if matrix[i][j] == 0:
                            is_full = False
                    if is_full:
                        erase_count += 1
                        k = j
                        while k > 0:
                            for i in range(10):
                                matrix[i][k] = matrix[i][k - 1]
                            k -= 1
                if erase_count == 1:
                    ui_variables.single_sound.play()
                    score += 50 * level
                elif erase_count == 2:
                    ui_variables.double_sound.play()
                    score += 150 * level
                elif erase_count == 3:
                    ui_variables.triple_sound.play()
                    score += 350 * level
                elif erase_count == 4:
                    ui_variables.tetris_sound.play()
                    score += 1000 * level

                # Increase level
                goal -= erase_count
                if goal < 1 and level < 15:
                    level += 1
                    goal += level * 5
                    framerate = int(framerate * 0.8)

            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation)
                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    pause = True
                # Hard drop
                elif event.key == K_SPACE:
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation):
                        dy += 1
                    hard_drop = True
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                # Hold
                elif event.key == K_LSHIFT or event.key == K_c:
                    if hold == False:
                        ui_variables.move_sound.play()
                        if hold_mino == -1:
                            hold_mino = mino
                            mino = next_mino1
                            next_mino1 = randint(1, 7)
                        else:
                            hold_mino, mino = mino, hold_mino
                        dx, dy = 3, 0
                        rotation = 0
                        hold = True
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                # Turn right
                elif event.key == K_UP or event.key == K_x:
                    if is_turnable_r(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        rotation += 1
                    # Kick
                    elif is_turnable_r(dx, dy - 1, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation += 1
                    elif is_turnable_r(dx + 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation += 1
                    elif is_turnable_r(dx - 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation += 1
                    elif is_turnable_r(dx, dy - 2, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_r(dx + 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_r(dx - 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation += 1
                    if rotation == 4:
                        rotation = 0
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                # Turn left
                elif event.key == K_z or event.key == K_LCTRL:
                    if is_turnable_l(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        rotation -= 1
                    # Kick
                    elif is_turnable_l(dx, dy - 1, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation -= 1
                    elif is_turnable_l(dx + 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation -= 1
                    elif is_turnable_l(dx - 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation -= 1
                    elif is_turnable_l(dx, dy - 2, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_l(dx + 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_l(dx - 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 2
                    if rotation == -1:
                        rotation = 3
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                # Move left
                elif event.key == K_LEFT:
                    if not is_leftedge(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                # Move right
                elif event.key == K_RIGHT:
                    if not is_rightedge(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)

        pygame.display.update()

    # Game over screen
    elif game_over:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                over_text_1 = ui_variables.h2_b.render("GAME", 1, ui_variables.white)
                over_text_2 = ui_variables.h2_b.render("OVER", 1, ui_variables.white)
                over_start = ui_variables.h5.render("Press return to continue", 1, ui_variables.white)

                draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                screen.blit(over_text_1, (58, 75))
                screen.blit(over_text_2, (62, 105))

                name_1 = ui_variables.h2_i.render(chr(name[0]), 1, ui_variables.white)
                name_2 = ui_variables.h2_i.render(chr(name[1]), 1, ui_variables.white)
                name_3 = ui_variables.h2_i.render(chr(name[2]), 1, ui_variables.white)

                underbar_1 = ui_variables.h2.render("_", 1, ui_variables.white)
                underbar_2 = ui_variables.h2.render("_", 1, ui_variables.white)
                underbar_3 = ui_variables.h2.render("_", 1, ui_variables.white)

                screen.blit(name_1, (65, 147))
                screen.blit(name_2, (95, 147))
                screen.blit(name_3, (125, 147))

                if blink:
                    screen.blit(over_start, (32, 195))
                    blink = False
                else:
                    if name_location == 0:
                        screen.blit(underbar_1, (65, 145))
                    elif name_location == 1:
                        screen.blit(underbar_2, (95, 145))
                    elif name_location == 2:
                        screen.blit(underbar_3, (125, 145))
                    blink = True

                pygame.display.update()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    ui_variables.click_sound.play()

                    outfile = open('leaderboard.txt','a')
                    outfile.write(chr(name[0]) + chr(name[1]) + chr(name[2]) + ' ' + str(score) + '\n')
                    outfile.close()

                    game_over = False
                    hold = False
                    dx, dy = 3, 0
                    rotation = 0
                    mino = randint(1, 7)
                    next_mino1 = randint(1, 7)
                    hold_mino = -1
                    framerate = 30
                    score = 0
                    score = 0
                    level = 1
                    goal = level * 5
                    bottom_count = 0
                    hard_drop = False
                    name_location = 0
                    name = [65, 65, 65]
                    matrix = [[0 for y in range(height + 1)] for x in range(width)]

                    with open('leaderboard.txt') as f:
                        lines = f.readlines()
                    lines = [line.rstrip('\n') for line in open('leaderboard.txt')]

                    leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
                    for i in lines:
                        leaders[i.split(' ')[0]] = int(i.split(' ')[1])
                    leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)

                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_RIGHT:
                    if name_location != 2:
                        name_location += 1
                    else:
                        name_location = 0
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_LEFT:
                    if name_location != 0:
                        name_location -= 1
                    else:
                        name_location = 2
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_UP:
                    ui_variables.click_sound.play()
                    if name[name_location] != 90:
                        name[name_location] += 1
                    else:
                        name[name_location] = 65
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_DOWN:
                    ui_variables.click_sound.play()
                    if name[name_location] != 65:
                        name[name_location] -= 1
                    else:
                        name[name_location] = 90
                    pygame.time.set_timer(pygame.USEREVENT, 1)
    elif select_mode:
        screen.fill(ui_variables.real_white)
        draw_image(screen, background_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        pause_surface = screen.convert_alpha() #투명 가능하도록
        pause_surface.fill((0, 0, 0, 0))  #투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(board_width), int(board_height)])  #(screen, 색깔, 위치 x, y좌표, 너비, 높이)
        screen.blit(pause_surface, (0, 0))

        single_button.draw(screen, (0,0,0))
        pvp_button.draw(screen, (0,0,0))
        hard_button.draw(screen, (0,0,0))
        
        pygame.display.update()  # select mode 화면으로 넘어가도록 전체 화면 업데이트

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True

            # 기존 pytris: 첫 화면에서 space만 누르면 게임 시작
            elif event.type == KEYDOWN:
                '''
                if event.key == K_SPACE:
                    ui_variables.click_sound.play()
                    start = True
                '''
            
            
            elif event.type == pygame.MOUSEMOTION:
                if single_button.isOver_2(pos):
                    single_button.image = clicked_single_button_image
                else:
                    single_button.image = single_button_image

                if pvp_button.isOver_2(pos):
                    pvp_button.image = clicked_pvp_button_image
                else:
                    pvp_button.image = pvp_button_image

                if hard_button.isOver_2(pos):
                    hard_button.image = clicked_hard_button_image
                else:
                    hard_button.image = hard_button_image
            

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if single_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    previous_time = pygame.time.get_ticks()
                    start = True
                    initalize = True
                    #pygame.mixer.music.play(-1) #play(-1) = 노래 반복재생
                    #ui_variables.intro_sound.stop()
                if pvp_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    pvp = True
                    initalize = True
                    # pygame.mixer.music.play(-1)
                    # ui_variables.intro_sound.stop()
                if hard_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    hard = True
                    initalize = True
                    # pygame.mixer.music.play(-1)
                    # ui_variables.intro_sound.stop()
                '''
                if single_button.isOver_2(pos):

                if pvp_button.isOver_2(pos):
                    
                if gravity_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    start = True
                    gravity_mode = True
                    initalize = True
                    pygame.mixer.music.play(-1)
                    ui_variables.intro_sound.stop()
                if timeattack_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    start = True
                    time_attack = True
                    initalize = True
                    pygame.mixer.music.play(-1)
                    ui_variables.intro_sound.stop()
                if leaderboard_icon.isOver(pos):
                    ui_variables.click_sound.play()
                    leader_board = True
                if setting_icon.isOver(pos):
                    ui_variables.click_sound.play()
                    setting = True
                if quit_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    done = True
                if help_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    help = True
                '''
            

    elif leader_board:
        pass
    elif setting:
        pass

    # Start screen
    else:
        # 초기화
        if initialize:
            set_initial_values()
        initialize = False
        

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True

            
            # 기존 pytris: 첫 화면에서 space만 누르면 게임 시작
            elif event.type == KEYDOWN:
                '''
                if event.key == K_SPACE:
                    ui_variables.click_sound.play()
                    start = True
                '''
            

            elif event.type == pygame.MOUSEMOTION:
                if select_mode_button.isOver_2(pos):
                    select_mode_button.image = clicked_select_mode_button_image
                else:
                    select_mode_button.image = select_mode_button_image

                if quit_button.isOver_2(pos):
                    quit_button.image = clicked_quit_button_image
                else:
                    quit_button.image = quit_button_image

                if setting_button.isOver_2(pos):
                    setting_button.image = clicked_setting_button_image
                else:
                    setting_button.image = setting_button_image

                if score_board_button.isOver_2(pos):
                    score_board_button.image = clicked_score_board_button_image
                else:
                    score_board_button.image = score_board_button_image


            elif event.type == pygame.MOUSEBUTTONDOWN:
                if select_mode_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    previous_time = pygame.time.get_ticks()
                    select_mode = True
                    # start = True
                    initialize = True
                    # #pygame.mixer.music.play(-1) #play(-1) = 노래 반복재생
                    # #ui_variables.intro_sound.stop()
                '''
                if single_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    previous_time = pygame.time.get_ticks()
                    start = True
                    initalize = True
                    pygame.mixer.music.play(-1) #play(-1) = 노래 반복재생
                    ui_variables.intro_sound.stop()
                if pvp_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    pvp = True
                    initalize = True
                    pygame.mixer.music.play(-1)
                    ui_variables.intro_sound.stop()
                if gravity_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    start = True
                    gravity_mode = True
                    initalize = True
                    pygame.mixer.music.play(-1)
                    ui_variables.intro_sound.stop()
                if timeattack_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    start = True
                    time_attack = True
                    initalize = True
                    pygame.mixer.music.play(-1)
                    ui_variables.intro_sound.stop()
                if leaderboard_icon.isOver(pos):
                    ui_variables.click_sound.play()
                    leader_board = True
                if setting_icon.isOver(pos):
                    ui_variables.click_sound.play()
                    setting = True
                if quit_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    done = True
                if help_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    help = True
                '''

        # pygame.time.set_timer(pygame.USEREVENT, 300)
        '''
        screen.fill(ui_variables.white)
        pygame.draw.rect(
            screen,
            ui_variables.grey_1,
            Rect(0, 187, 300, 187)
        )
        '''

        # 메인화면 배경
        draw_image(screen, background_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        
        # 버튼그리기
        select_mode_button.draw(screen, (0,0,0))
        setting_button.draw(screen, (0,0,0))
        score_board_button.draw(screen, (0,0,0))
        quit_button.draw(screen, (0,0,0))

        '''
        # 리더보드 
        leader_1 = ui_variables.h5_i.render('1st ' + leaders[0][0] + ' ' + str(leaders[0][1]), 1, ui_variables.grey_1)
        leader_2 = ui_variables.h5_i.render('2nd ' + leaders[1][0] + ' ' + str(leaders[1][1]), 1, ui_variables.grey_1)
        leader_3 = ui_variables.h5_i.render('3rd ' + leaders[2][0] + ' ' + str(leaders[2][1]), 1, ui_variables.grey_1)
        
        screen.blit(leader_1, (10, 10))
        screen.blit(leader_2, (10, 23))
        screen.blit(leader_3, (10, 36))
        '''

        if not start:
            pygame.display.update()
            clock.tick(3)

pygame.quit()
