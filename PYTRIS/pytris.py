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

total_time = 60 # 타임 어택 시간
speed_change = 2 # 레벨별 블록 하강 속도 상승 정도

board_width = 800  # 전체 창의 가로 길이
board_height = 450 # 전체 창의 세로 길이
board_rate = 0.5625 #가로세로비율

min_width = 400
min_height = 225
mid_width = 1200

# 기본 볼륨
music_volume = 5
effect_volume = 5

mino_matrix_x = 4 #mino는 4*4 배열이어서 이를 for문에 사용
mino_matrix_y = 4 #mino는 4*4 배열이어서 이를 for문에 사용
board_x = 10
board_y = 20

total_time = 60 # 타임 어택 시간

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)
pygame.time.set_timer(pygame.USEREVENT, framerate * 10)
pygame.display.set_caption("PYTRIS™")

initialize = True # Start Screen 에서 set_initial_values()로 초기화할지 여부를 boolean으로 저장

class ui_variables:
    # Fonts
    font_path = "assets/fonts/a옛날사진관2.ttf"
    font_path_b = "assets/fonts/a옛날사진관3.ttf"
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
<<<<<<< HEAD
    pygame.mixer.music.load("assets/sounds/BGM1.wav") #음악 불러옴
=======
    pygame.mixer.music.load("assets/sounds/SFX_Fall.wav") #음악 불러옴
>>>>>>> 2a0e0f9d8232bf48b40468d75a887f4e76dd76e9
    pygame.mixer.music.set_volume(0.5) # 이 부분도 필요 없음, set_volume에 추가해야 함
    intro_sound = pygame.mixer.Sound("assets/sounds/BGM1.wav")
    fall_sound = pygame.mixer.Sound("assets/sounds/SFX_Fall.wav")
    break_sound = pygame.mixer.Sound("assets/sounds/SFX_Break.wav")
    click_sound = pygame.mixer.Sound("assets/sounds/SFX_ButtonUp.wav") #여기부터
    move_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceMoveLR.wav")
    drop_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceHardDrop.wav")
    single_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearSingle.wav")
    double_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearDouble.wav")
    triple_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearTriple.wav") #여기까지는 기존코드
    tetris_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialTetris.wav")
    LevelUp_sound = pygame.mixer.Sound("assets/sounds/SFX_LevelUp.wav")
    GameOver_sound = pygame.mixer.Sound("assets/sounds/SFX_GameOver.wav")

    # Background colors
    black = (10, 10, 10) #rgb(10, 10, 10)
    black_pause = (0, 0, 0, 127)
    real_white = (255, 255, 255) #rgb(255, 255, 255)
    white = (211, 211, 211) #rgb(211, 211, 211) ##연회색
    grey_1 = (26, 26, 26) #rgb(26, 26, 26)
    grey_2 = (35, 35, 35) #rgb(35, 35, 35)
    grey_3 = (55, 55, 55) #rgb(55, 55, 55)
    pinkpurple = (250, 165, 255) #rgb(250, 165, 255) 핑크+보라#
    

    # Tetrimino colors
    cyan = (69, 206, 204) #rgb(69, 206, 204) # I
    blue = (64, 111, 249) #rgb(64, 111, 249) # J
    orange = (253, 189, 53) #rgb(253, 189, 53) # L
    yellow = (246, 227, 90) #rgb(246, 227, 90) # O
    green = (98, 190, 68) #rgb(98, 190, 68) # S
    pink = (242, 64, 235) #rgb(242, 64, 235) # T
    red = (225, 13, 27) #rgb(225, 13, 27) # Z

    t_color = [grey_2, cyan, blue, orange, yellow, green, pink, red, grey_3]
    cyan_image = 'assets/block_images/cyan.png'
    blue_image = 'assets/block_images/blue.png'
    orange_image = 'assets/block_images/orange.png'
    yellow_image = 'assets/block_images/yellow.png'
    green_image = 'assets/block_images/green.png'
    pink_image = 'assets/block_images/purple.png'
    red_image = 'assets/block_images/red.png'
    ghost_image = 'assets/block_images/ghost.png'
    table_image = 'assets/block_images/background.png'
    linessent_image = 'assets/block_images/linessent.png'
    t_block = [table_image, cyan_image, blue_image, orange_image, yellow_image, green_image, pink_image, red_image,
               ghost_image, linessent_image]



#각 이미지 주소
background_image = 'assets/images/background_image.png' #메뉴화면(첫 화면) 배경
gamebackground_image = 'assets/images/background_nyc.png' #게임 배경화면 : 기본값 뉴욕
pause_board_image = 'assets/vector/pause_board.png'

select_mode_button_image = 'assets/vector/select_mode_button.png'
clicked_select_mode_button_image = 'assets/vector/clicked_select_mode_button.png'

setting_button_image = 'assets/vector/settings_button.png'
clicked_setting_button_image = 'assets/vector/clicked_settings_button.png'

pause_setting_button_image = 'assets/vector/pause_settings_button.png'
clicked_pause_setting_button_image = 'assets/vector/clicked_pause_settings_button.png'

score_board_button_image = 'assets/vector/score_board_button.png'
clicked_score_board_button_image = 'assets/vector/clicked_score_board_button.png'

quit_button_image = 'assets/vector/quit_button.png'
clicked_quit_button_image = 'assets/vector/clicked_quit_button.png'

<<<<<<< HEAD
=======

resume_button_image = 'assets/vector/resume_button.png'
clicked_resume_button_image = 'assets/vector/clicked_resume_button.png'

help_button_image = 'assets/vector/help_button.png'
clicked_help_button_image = 'assets/vector/clicked_help_button.png'

>>>>>>> 2a0e0f9d8232bf48b40468d75a887f4e76dd76e9
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

<<<<<<< HEAD
'''
=======


>>>>>>> 2a0e0f9d8232bf48b40468d75a887f4e76dd76e9
help_button_image = 'assets/vector/help_button.png'
clicked_help_button_image = 'assets/vector/clicked_help_button.png'
gravity_button_image = 'assets/vector/gravity_button.png'
clicked_gravity_button_image = 'assets/vector/clicked_gravity_button.png'
setting_vector = 'assets/vector/setting_vector.png'
clicked_setting_vector = 'assets/vector/clicked_setting_vector.png'
setting_board_image = 'assets/vector/setting_board.png'
gameover_board_image = 'assets/vector/gameover_board.png'

gameover_image = 'assets/vector/gameover.png'

<<<<<<< HEAD
=======

>>>>>>> 2a0e0f9d8232bf48b40468d75a887f4e76dd76e9
setting_board_image = 'assets/vector/setting_board.png'
number_board = 'assets/vector/number_board.png'
mute_button_image = 'assets/vector/allmute_button.png'


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

sound_off_button_image = 'assets/vector/sound_off_button.png'
sound_on_button_image = 'assets/vector/sound_on_button.png'
check_button_image = 'assets/vector/checkbox_button.png'
clicked_check_button_image = 'assets/vector/clicked_checkbox_button.png'

pvp_win_image = 'assets/vector/pvp_win.png'
pvp_lose_image = 'assets/vector/pvp_lose.png'


leaderboard_vector = 'assets/vector/leaderboard_vector.png'
clicked_leaderboard_vector = 'assets/vector/clicked_leaderboard_vector.png'


leaderboard_vector = 'assets/vector/leaderboard_vector.png'
clicked_leaderboard_vector = 'assets/vector/clicked_leaderboard_vector.png'


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

# 메뉴 버튼

select_mode_button = button(board_width, board_height, 0.2, 0.2, 0.22, 0.2, select_mode_button_image)
setting_button = button(board_width, board_height, 0.2, 0.8, 0.22, 0.2, setting_button_image)

quit_button = button(board_width, board_height, 0.8, 0.8, 0.22, 0.2, quit_button_image)
score_board_button = button(board_width, board_height, 0.8, 0.2, 0.22, 0.2, score_board_button_image)

single_button = button(board_width,board_height, 0.25, 0.35, 0.22, 0.2, single_button_image)
hard_button = button(board_width, board_height, 0.5, 0.35, 0.22, 0.2, hard_button_image)
pvp_button = button(board_width, board_height, 0.75, 0.35, 0.22, 0.2, pvp_button_image)
hard_tutorial_button = button(board_width, board_height, 0.37, 0.65, 0.22, 0.2, hard_tutorial_button_image)
multi_tutorial_button = button(board_width, board_height, 0.63, 0.65, 0.22, 0.2, multi_tutorial_button_image)

resume_button = button(board_width, board_height, 0.5, 0.23, 0.17, 0.2, resume_button_image)
menu_button2 = button(board_width, board_height, 0.5, 0.43, 0.17, 0.2, menu_button_image)
help_button = button(board_width, board_height, 0.5, 0.63, 0.17, 0.2, help_button_image)
pause_quit_button = button(board_width, board_height, 0.5, 0.83, 0.17, 0.2, quit_button_image)
#pause_setting_button = button(board_width, board_height, 0.5, 0.63, 0.17, 0.2, pause_setting_button_image)

leaderboard_icon = button(board_width, board_height, 0.77, 0.85, 0.15, 0.2, leaderboard_vector)
mute_button = button(board_width, board_height, 0.5, 0.27, 0.25, 0.45, mute_button_image)
default_button = button(board_width, board_height, 0.5, 0.27, 0.25, 0.45, default_button_image)
back_button = button(board_width, board_height, 0.5, 0.85, 0.15, 0.35, back_button_image)

volume = 1.0

effect_plus_button = button(board_width, board_height, 0.37, 0.73, 0.0625, 0.1111, plus_button_image)
effect_minus_button = button(board_width, board_height, 0.52, 0.73, 0.0625, 0.1111, minus_button_image)

sound_plus_button = button(board_width, board_height, 0.37, 0.53, 0.0625, 0.1111, plus_button_image)
sound_minus_button = button(board_width, board_height, 0.52, 0.53, 0.0625, 0.1111, minus_button_image)

#음소거 추가#
effect_sound_off_button = button(board_width, board_height, 0.65, 0.73, 0.08, 0.15, sound_off_button_image)
music_sound_off_button = button(board_width, board_height, 0.65, 0.53, 0.08, 0.15, sound_off_button_image)
effect_sound_on_button = button(board_width, board_height, 0.65, 0.73, 0.08, 0.15, sound_on_button_image)
music_sound_on_button = button(board_width, board_height, 0.65, 0.53, 0.08, 0.15, sound_on_button_image)

mute_check_button = button(board_width, board_height, 0.2, 0.4, 0.0625, 0.1111, check_button_image)
smallsize_check_button = button(board_width, board_height, 0.5, 0.25, 0.1875, 0.1444, smallsize_board)
midiumsize_check_button = button(board_width, board_height, 0.5, 0.45, 0.1875, 0.1444, midiumsize_board)
bigsize_check_button = button(board_width, board_height, 0.5, 0.65, 0.1875, 0.1444, bigsize_board)

volume_icon = button(board_width, board_height, 0.4, 0.5, 0.12, 0.23, volume_vector)
screen_icon = button(board_width, board_height, 0.6, 0.5, 0.12, 0.23, screen_vector)

<<<<<<< HEAD
leaderboard_icon = button(board_width, board_height, 0.77, 0.85, 0.15, 0.2, leaderboard_vector)
mute_button = button(board_width, board_height, 0.5, 0.27, 0.25, 0.45, mute_button_image)
default_button = button(board_width, board_height, 0.5, 0.27, 0.25, 0.45, default_button_image)
back_button = button(board_width, board_height, 0.5, 0.85, 0.15, 0.35, back_button_image)

volume = 1.0

effect_plus_button = button(board_width, board_height, 0.37, 0.73, 0.0625, 0.1111, plus_button_image)
effect_minus_button = button(board_width, board_height, 0.52, 0.73, 0.0625, 0.1111, minus_button_image)

sound_plus_button = button(board_width, board_height, 0.37, 0.53, 0.0625, 0.1111, plus_button_image)
sound_minus_button = button(board_width, board_height, 0.52, 0.53, 0.0625, 0.1111, minus_button_image)

#음소거 추가#
effect_sound_off_button = button(board_width, board_height, 0.65, 0.73, 0.08, 0.15, sound_off_button_image)
music_sound_off_button = button(board_width, board_height, 0.65, 0.53, 0.08, 0.15, sound_off_button_image)
effect_sound_on_button = button(board_width, board_height, 0.65, 0.73, 0.08, 0.15, sound_on_button_image)
music_sound_on_button = button(board_width, board_height, 0.65, 0.53, 0.08, 0.15, sound_on_button_image)

mute_check_button = button(board_width, board_height, 0.2, 0.4, 0.0625, 0.1111, check_button_image)
smallsize_check_button = button(board_width, board_height, 0.5, 0.25, 0.1875, 0.1444, smallsize_board)
midiumsize_check_button = button(board_width, board_height, 0.5, 0.45, 0.1875, 0.1444, midiumsize_board)
bigsize_check_button = button(board_width, board_height, 0.5, 0.65, 0.1875, 0.1444, bigsize_board)

volume_icon = button(board_width, board_height, 0.4, 0.5, 0.12, 0.23, volume_vector)
screen_icon = button(board_width, board_height, 0.6, 0.5, 0.12, 0.23, screen_vector)

=======
>>>>>>> 2a0e0f9d8232bf48b40468d75a887f4e76dd76e9
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

'''
<<<<<<< HEAD

=======
'''
>>>>>>> 2a0e0f9d8232bf48b40468d75a887f4e76dd76e9
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
<<<<<<< HEAD

#음소거 추가#
effect_sound_off_button = button(board_width, board_height, 0.65, 0.73, 0.08, 0.15, sound_off_button_image)
music_sound_off_button = button(board_width, board_height, 0.65, 0.53, 0.08, 0.15, sound_off_button_image)
effect_sound_on_button = button(board_width, board_height, 0.65, 0.73, 0.08, 0.15, sound_on_button_image)
music_sound_on_button = button(board_width, board_height, 0.65, 0.53, 0.08, 0.15, sound_on_button_image)
mute_check_button = button(board_width, board_height, 0.2, 0.4, 0.0625, 0.1111, check_button_image)
smallsize_check_button = button(board_width, board_height, 0.5, 0.25, 0.1875, 0.1444, smallsize_board)
midiumsize_check_button = button(board_width, board_height, 0.5, 0.45, 0.1875, 0.1444, midiumsize_board)
bigsize_check_button = button(board_width, board_height, 0.5, 0.65, 0.1875, 0.1444, bigsize_board)
=======
'''
>>>>>>> 2a0e0f9d8232bf48b40468d75a887f4e76dd76e9

'''

#게임 중 버튼 생성하기위한 버튼객체 리스트 (버튼 전체)
button_list = [mute_button, default_button, single_button, pvp_button, help_button, quit_button, gravity_button, timeattack_button, resume_button, restart_button, setting_button, pause_quit_button, back_button,
        ok_button, menu_button, gameover_quit_button, effect_plus_button, effect_minus_button, sound_plus_button, sound_minus_button, level_plus_button,
        effect_sound_off_button, music_sound_off_button, effect_sound_on_button, music_sound_on_button, mute_check_button, smallsize_check_button, midiumsize_check_button, bigsize_check_button,
        setting_icon, leaderboard_icon, volume_icon, screen_icon, level_minus_button, combo_minus_button, combo_plus_button, speed_minus_button, speed_plus_button]
'''

def set_volume():
    ui_variables.fall_sound.set_volume(effect_volume / 10) #set_volume의 argument는 0.0~1.0으로 이루어져야하기 때문에 소수로 만들어주기 위해 10으로 나눔#
    ui_variables.click_sound.set_volume(effect_volume / 10)
    ui_variables.break_sound.set_volume(effect_volume / 10)
    ui_variables.move_sound.set_volume(effect_volume / 10)
    ui_variables.drop_sound.set_volume(effect_volume / 10)
    ui_variables.single_sound.set_volume(effect_volume / 10)
    ui_variables.double_sound.set_volume(effect_volume / 10)
    ui_variables.triple_sound.set_volume(effect_volume / 10)
    ui_variables.tetris_sound.set_volume(effect_volume / 10)
    ui_variables.LevelUp_sound.set_volume(effect_volume / 10)
    ui_variables.GameOver_sound.set_volume(music_volume / 10)
    ui_variables.intro_sound.set_volume(music_volume / 10)
    pygame.mixer.music.set_volume(music_volume / 10)


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


def draw_block_image(x, y, image):
    draw_image(screen, image, x, y, block_size, block_size) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)



# Draw game screen
def draw_board(next1, next2, hold, score, level, goal):
    sidebar_width = int(board_width * 0.5312) #크기 비율 고정, 전체 board 가로길이에서 원하는 비율을 곱해줌
    # screen.fill(ui_variables.grey_1)

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        Rect(sidebar_width, 0, int(board_width * 0.2375), board_height) #크기 비율 고정
    )

    # Draw 2 next minos
    grid_n1 = tetrimino.mino_map[next1 - 1][0]
    grid_n2 = tetrimino.mino_map[next2 - 1][0]


    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            dx1 = int(board_width * 0.025) + sidebar_width + block_size * j #위치 비율 고정, 전체 board 가로 길이에서 원하는 비율을 곱해줌
            dy1 = int(board_height * 0.3743) + block_size * i #위치 비율 고정, 전체 board 세로 길이에서 원하는 비율을 곱해줌#
            if grid_n1[i][j] != 0:
                draw_block_image(dx1, dy1, ui_variables.t_block[grid_n1[i][j]])
    
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            dx2 = int(board_width * 0.145) + sidebar_width + block_size * j #위치 비율 고정, 전체 board 가로길이에서 원하는 비율을 곱해줌#
            dy2 = int(board_height * 0.3743) + block_size * i #위치 비율 고정, 전체 board 세로길이에서 원하는 비율을 곱해줌#
            if grid_n2[i][j] != 0:
                draw_block_image(dx2, dy2, ui_variables.t_block[grid_n2[i][j]])

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for i in range(4):
            for j in range(4):
                dx = 220 + block_size * j
                dy = 50 + block_size * i
                if grid_h[i][j] != 0:
                    draw_block_image(dx, dy, ui_variables.t_block[grid_h[i][j]]) #hold 블록 출력


    # Set max score
    if score > 999999:
        score = 999999

    # Draw texts
    text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.real_white)
    text_next = ui_variables.h5.render("NEXT", 1, ui_variables.real_white)
    text_score = ui_variables.h5.render("SCORE", 1, ui_variables.real_white)
    score_value = ui_variables.h4.render(str(score), 1, ui_variables.real_white)
    text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.real_white)
    level_value = ui_variables.h4.render(str(level), 1, ui_variables.real_white)
    text_goal = ui_variables.h5.render("GOAL", 1, ui_variables.real_white)
    goal_value = ui_variables.h4.render(str(goal), 1, ui_variables.real_white)

    # Place texts
    screen.blit(text_hold, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.0374)))
    screen.blit(text_next, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.2780)))
    screen.blit(text_score, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.5187)))
    screen.blit(score_value, (int(board_width * 0.055) + sidebar_width, int(board_height * 0.5614)))
    screen.blit(text_level, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.6791)))
    screen.blit(level_value, (int(board_width * 0.055) + sidebar_width, int(board_height * 0.7219)))
    screen.blit(text_goal, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.8400)))
    screen.blit(goal_value, (int(board_width * 0.055) + sidebar_width, int(board_height * 0.8823)))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(board_width * 0.25) + block_size * x  #위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#
            dy = int(board_height * 0.055) + block_size * y #위치비율 고정, board 세로길이에 원하는 비율을 곱해줌#
            draw_block_image(dx, dy, ui_variables.t_block[matrix[x][y + 1]])


def draw_1Pboard(next, hold, score, level, goal):
    sidebar_width = int(board_width * 0.31) #위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        Rect(sidebar_width, 0, int(board_width * 0.1875), board_height) #크기비율 고정, board 가로길이에 원하는 비율을 곱해줌#
    )

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]  #(배열이라-1) 다음 블록의 원래 모양

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            dx = int(board_width * 0.045) + sidebar_width + block_size * j #위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#
            dy = int(board_height * 0.3743) + block_size * i #위치비율 고정, board 세로길이에 원하는 비율을 곱해줌#
            if grid_n[i][j] != 0:
                draw_block_image(dx, dy, ui_variables.t_block[grid_n[i][j]])

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]  #(배열이라-1) 기본 모양

    if hold_mino != -1: #기본값이 -1. 즉 hold블록 존재할 떄
        for i in range(mino_matrix_y):
            for j in range(mino_matrix_x):
                dx = int(board_width * 0.045) + sidebar_width + block_size * j #위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#
                dy = int(board_height * 0.1336) + block_size * i #위치비율 고정, board 세로길이에 원하는 비율을 곱해줌#
                if grid_h[i][j] != 0:
                    draw_block_image(dx, dy, ui_variables.t_block[grid_h[i][j]]) #hold 블록 그림

    # Set max score
    if score > 999999:
        score = 999999 #최대 점수가 999999가 넘지 않도록 설정해줌

    # Draw texts
    #render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
    if textsize==False:
        text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h5.render("NEXT", 1, ui_variables.real_white)
        text_score = ui_variables.h5.render("SCORE", 1, ui_variables.real_white)
        score_value = ui_variables.h4.render(str(score), 1, ui_variables.real_white)
        text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.real_white)
        level_value = ui_variables.h4.render(str(level), 1, ui_variables.real_white)
        text_combo = ui_variables.h5.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h4.render(str(combo_count), 1, ui_variables.real_white)
    if textsize==True:
        text_hold = ui_variables.h3.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h3.render("NEXT", 1, ui_variables.real_white)
        text_score = ui_variables.h3.render("SCORE", 1, ui_variables.real_white)
        score_value = ui_variables.h2.render(str(score), 1, ui_variables.real_white)
        text_level = ui_variables.h3.render("LEVEL", 1, ui_variables.real_white)
        level_value = ui_variables.h2.render(str(level), 1, ui_variables.real_white)
        text_combo = ui_variables.h3.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h2.render(str(combo_count), 1, ui_variables.real_white)
    if debug:
        speed_value = ui_variables.h5.render("SPEED : "+str(framerate), 1, ui_variables.real_white) #speed를 알려주는 framerate(기본값 30. 빨라질 수록 숫자 작아짐)
        screen.blit(speed_value, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.015))) #각각 전체 board 가로길이, 세로길이에 원하는 비율을 곱해줌
    screen.blit(text_hold, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.0374)))
    screen.blit(text_next, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.2780)))
    screen.blit(text_score, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.5187)))
    screen.blit(score_value, (int(board_width * 0.055) + sidebar_width, int(board_height * 0.5614)))
    screen.blit(text_level, (int(board_width*0.045) + sidebar_width, int(board_height*0.6791)))
    screen.blit(level_value, (int(board_width*0.055) + sidebar_width , int(board_height*0.7219)))
    screen.blit(text_combo, (int(board_width*0.045) + sidebar_width , int(board_height*0.8395)))
    screen.blit(combo_value, (int(board_width*0.055) + sidebar_width, int(board_height*0.8823)))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(board_width * 0.05) + block_size * x #위치 비율 고정, board의 가로길이에 원하는 비율을 곱해줌
            dy = int(board_height * 0.055) + block_size * y #위치 비율 고정, board의 세로길이에 원하는 비율을 곱해줌
            draw_block_image(dx, dy, ui_variables.t_block[matrix[x][y + 1]])


def draw_2Pboard(next, hold, score, level, goal):
    sidebar_width = int(board_width * 0.82) #위치 비율 고정, , board의 가로길이에 원하는 비율을 곱해줌

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        Rect(sidebar_width, 0, int(board_width * 0.1875), board_height) #크기 비율 고정, , board의 가로길이에 원하는 비율을 곱해줌, Rect(x축, y축, 가로길이, 세로길이)#
    )

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]

    for i in range(mino_matrix_y):  # 16개의 그리드 칸에서 true인 값만 뽑아서 draw.rect
        for j in range(mino_matrix_x):
            dx = int(board_width * 0.05) + sidebar_width + block_size * j  #위치 비율 고정, board의 가로길이에 원하는 비율을 곱해줌
            dy = int(board_height * 0.3743) + block_size * i  #위치 비율 고정, board의 세로길이에 원하는 비율을 곱해줌
            if grid_n[i][j] != 0:
                draw_block_image(dx, dy, ui_variables.t_block[grid_n[i][j]])

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino_2P != -1:  #기본값이 -1. 즉 hold블록 존재할 떄
        for i in range(mino_matrix_y):
            for j in range(mino_matrix_x):
                dx = int(board_width * 0.045) + sidebar_width + block_size * j  #위치 비율 고정, board의 가로길이에 원하는 비율을 곱해줌
                dy = int(board_height * 0.1336) + block_size * i  #위치 비율 고정, board의 세로길이에 원하는 비율을 곱해줌
                if grid_h[i][j] != 0:
                    draw_block_image(dx, dy, ui_variables.t_block[grid_h[i][j]])

    # Set max score
    if score > 999999:
        score = 999999 #최대 점수가 999999가 넘지 못하도록 설정#

    #render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래 코드의 숫자 1=안티에일리어싱 적용에 대한 코드
    if textsize==False:
        text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h5.render("NEXT", 1, ui_variables.real_white)
        text_score = ui_variables.h5.render("SCORE", 1, ui_variables.real_white)
        score_value = ui_variables.h4.render(str(score), 1, ui_variables.real_white)
        text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.real_white)
        level_value = ui_variables.h4.render(str(level), 1, ui_variables.real_white)
        text_combo = ui_variables.h5.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h4.render(str(combo_count), 1, ui_variables.real_white)
    if textsize==True:
        text_hold = ui_variables.h4.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h4.render("NEXT", 1, ui_variables.real_white)
        text_score = ui_variables.h4.render("SCORE", 1, ui_variables.real_white)
        score_value = ui_variables.h3.render(str(score), 1, ui_variables.real_white)
        text_level = ui_variables.h4.render("LEVEL", 1, ui_variables.real_white)
        level_value = ui_variables.h3.render(str(level), 1, ui_variables.real_white)
        text_combo = ui_variables.h4.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h3.render(str(combo_count), 1, ui_variables.real_white)
    if debug:
        speed_value = ui_variables.h5.render("SPEED : "+str(framerate_2P), 1, ui_variables.real_white) #speed를 알려주는 framerate(기본값 30. 빨라질 수록 숫자 작아짐)
        screen.blit(speed_value, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.015))) #각각 전체 board의 가로길이, 세로길이에 대해 원하는 비율을 곱해줌
    screen.blit(text_hold, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.0374)))
    screen.blit(text_next, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.2780)))
    screen.blit(text_score, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.5187)))
    screen.blit(score_value, (int(board_width * 0.055) + sidebar_width, int(board_height * 0.5614)))
    screen.blit(text_level, (int(board_width*0.045) + sidebar_width, int(board_height*0.6791)))
    screen.blit(level_value, (int(board_width*0.055) + sidebar_width , int(board_height*0.7219)))
    screen.blit(text_combo, (int(board_width*0.045) + sidebar_width , int(board_height*0.8395)))
    screen.blit(combo_value, (int(board_width*0.055) + sidebar_width, int(board_height*0.8823)))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(board_width * 0.54) + block_size * x #위치비율 고정
            dy = int(board_height * 0.055) + block_size * y #위치비율 고정
            draw_block_image(dx, dy, ui_variables.t_block[matrix_2P[x][y + 1]])


def draw_multiboard(next_1P, hold_1P, next_2P, hold_2P, score1P, score2P, level1P, level2P, goal1P, goal2P):
    screen.fill(ui_variables.real_white)
    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
    draw_1Pboard(next_1P, hold_1P, score1P, level1P, goal1P)
    draw_2Pboard(next_2P, hold_2P, score2P, level2P, goal2P)



# Draw a tetrimino
def draw_mino(x, y, mino, r, matrix):  # mino는 모양, r은 회전된 모양 중 하나
    grid = tetrimino.mino_map[mino - 1][r]  # grid : 출력할 테트리스

    tx, ty = x, y
    while not is_bottom(tx, ty, mino, r, matrix):  # 테트리스가 바닥에 존재하면 true -> not이니까 바닥에 없는 상태
        ty += 1  # 한칸 밑으로 하강

    # Draw ghost
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                matrix[tx + j][ty + i] = 8  # 테트리스가 쌓일 위치에 8 이라는 ghost 만듦

    # Draw mino
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                matrix[x + j][y + i] = grid[i][j]  # 해당 위치에 블록 만듦


# Erase a tetrimino
def erase_mino(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - 1][r]

    # Erase ghost
    for j in range(board_y + 1):
        for i in range(board_x):
            if matrix[i][j] == 8:  # 테트리스 블록에서 해당 행렬위치에 ghost블록 존재하면
                matrix[i][j] = 0  # 없애서 빈 곳으로 만들기

    # Erase mino
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                matrix[x + j][y + i] = 0  # 해당 위치에 블록 없애서 빈 곳으로 만들기


# Returns true if mino is at bottom
def is_bottom(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - 1][r]  # grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (y + i + 1) > board_y:  # 바닥의 y좌표에 있음(바닥에 닿음)
                    return True
                elif matrix[x + j][y + i + 1] != 0 and matrix[x + j][y + i + 1] != 8:  # 그 블록위치에 0, 8 아님(즉 블록 존재 함)
                    return True

    return False


# Returns true if mino is at the left edge
def is_leftedge(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - 1][r] #grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0: #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j - 1) < 0:  #맨 왼쪽에 위치함
                    return True
                elif matrix[x + j - 1][y + i] != 0:  #그 위치의 왼쪽에 이미 무엇인가 존재함
                    return True

    return False

# Returns true if mino is at the right edge
def is_rightedge(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - 1][r] #grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0: #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j + 1) >= board_x :  #맨 오른쪽에 위치
                    return True
                elif matrix[x + j + 1][y + i] != 0:   #그 위치의 오른쪽에 이미 무엇인가 존재함
                    return True

    return False
  
def is_turnable_r(x, y, mino, r, matrix):
    if r != 3:  #회전모양 총 0, 1, 2, 3번째 총 4가지 있음
        grid = tetrimino.mino_map[mino - 1][r + 1] #3이 아니면 그 다음 모양
    else:
        grid = tetrimino.mino_map[mino - 1][0] #3이면 0번째 모양으로

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j) < 0 or (x + j) >= board_x or (y + i) < 0 or (y + i) > board_y :  #테트리스 matrix크기 벗어나면 못돌림
                    return False
                elif matrix[x + j][y + i] != 0:  #해당 자리에 이미 블록이 있으면 못돌림
                    return False
    return True

# Returns true if turning left is possible
def is_turnable_l(x, y, mino, r, matrix):
    if r != 0:  #회전모양 총 0, 1, 2, 3번째 총 4가지 있음
        grid = tetrimino.mino_map[mino - 1][r - 1]  #0이 아니면 그 다음 모양
    else:
        grid = tetrimino.mino_map[mino - 1][3] #0이면 3번째 모양으로

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j) < 0 or (x + j) >= board_x or (y + i) < 0 or (y + i) > board_y:  #테트리스 matrix크기 벗어나면 못돌림
                    return False
                elif matrix[x + j][y + i] != 0: #해당 자리에 이미 블록이 있으면 못돌림
                    return False

    return True

# Returns true if new block is drawable
def is_stackable(mino, matrix):
    grid = tetrimino.mino_map[mino - 1][0] #grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0 and matrix[3 + j][i] != 0: ###
                return False

    return True

'''
# Draw a tetrimino
def draw_mino(x, y, mino, r, matrix):  # mino는 모양, r은 회전된 모양 중 하나
    grid = tetrimino.mino_map[mino - 1][r]  # grid : 출력할 테트리스

    tx, ty = x, y
    while not is_bottom(tx, ty, mino, r, matrix):  # 테트리스가 바닥에 존재하면 true -> not이니까 바닥에 없는 상태
        ty += 1  # 한칸 밑으로 하강

    # Draw ghost
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                matrix[tx + j][ty + i] = 8  # 테트리스가 쌓일 위치에 8 이라는 ghost 만듦

    # Draw mino
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                matrix[x + j][y + i] = grid[i][j]  # 해당 위치에 블록 만듦


# Erase a tetrimino
def erase_mino(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - 1][r]

    # Erase ghost
    for j in range(board_y + 1):
        for i in range(board_x):
            if matrix[i][j] == 8:  # 테트리스 블록에서 해당 행렬위치에 ghost블록 존재하면
                matrix[i][j] = 0  # 없애서 빈 곳으로 만들기

    # Erase mino
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                matrix[x + j][y + i] = 0  # 해당 위치에 블록 없애서 빈 곳으로 만들기


# Returns true if mino is at bottom
def is_bottom(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - 1][r]  # grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (y + i + 1) > board_y:  # 바닥의 y좌표에 있음(바닥에 닿음)
                    return True
                elif matrix[x + j][y + i + 1] != 0 and matrix[x + j][y + i + 1] != 8:  # 그 블록위치에 0, 8 아님(즉 블록 존재 함)
                    return True

    return False



# Returns true if mino is at the left edge
def is_leftedge(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - 1][r] #grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0: #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j - 1) < 0:  #맨 왼쪽에 위치함
                    return True
                elif matrix[x + j - 1][y + i] != 0:  #그 위치의 왼쪽에 이미 무엇인가 존재함
                    return True

    return False

# Returns true if mino is at the right edge
def is_rightedge(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - 1][r] #grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0: #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j + 1) >= board_x :  #맨 오른쪽에 위치
                    return True
                elif matrix[x + j + 1][y + i] != 0:   #그 위치의 오른쪽에 이미 무엇인가 존재함
                    return True

    return False

def is_turnable_r(x, y, mino, r, matrix):
    if r != 3:  #회전모양 총 0, 1, 2, 3번째 총 4가지 있음
        grid = tetrimino.mino_map[mino - 1][r + 1] #3이 아니면 그 다음 모양
    else:
        grid = tetrimino.mino_map[mino - 1][0] #3이면 0번째 모양으로

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j) < 0 or (x + j) >= board_x or (y + i) < 0 or (y + i) > board_y :  #테트리스 matrix크기 벗어나면 못돌림
                    return False
                elif matrix[x + j][y + i] != 0:  #해당 자리에 이미 블록이 있으면 못돌림
                    return False
    return True

# Returns true if turning left is possible
def is_turnable_l(x, y, mino, r, matrix):
    if r != 0:  #회전모양 총 0, 1, 2, 3번째 총 4가지 있음
        grid = tetrimino.mino_map[mino - 1][r - 1]  #0이 아니면 그 다음 모양
    else:
        grid = tetrimino.mino_map[mino - 1][3] #0이면 3번째 모양으로

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j) < 0 or (x + j) >= board_x or (y + i) < 0 or (y + i) > board_y:  #테트리스 matrix크기 벗어나면 못돌림
                    return False
                elif matrix[x + j][y + i] != 0: #해당 자리에 이미 블록이 있으면 못돌림
                    return False

    return True

# Returns true if new block is drawable
def is_stackable(mino, matrix):
    grid = tetrimino.mino_map[mino - 1][0] #grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0 and matrix[3 + j][i] != 0: ###
                return False

    return True

'''

def set_vol(val):
    volume = int(val) / 100 #set_volume argenment로 넣기 위해서(소수점을 만들어주기 위해서) 100으로 나눠줌
    print(volume)
    ui_variables.click_sound.set_volume(volume)

# Initial values
def set_initial_values():
    global combo_count, combo_count_2P, score, level, goal, score_2P, level_2P, goal_2P, bottom_count, bottom_count_2P, hard_drop, hard_drop_2P, attack_point, attack_point_2P, dx, dy, dx_2P, dy_2P, rotation, rotation_2P, mino, mino_2P, next_mino1, next_mino2, next_mino1_2P, hold, hold_2P, hold_mino, hold_mino_2P, framerate, framerate_2P, matrix, matrix_2P, Change_RATE, blink, start, pause, done, game_over, leader_board, setting, volume_setting, screen_setting, pvp, help, gravity_mode, debug, d, e, b, u, g, start_ticks, textsize, CHANNELS, swidth, name_location, name, previous_time, current_time, pause_time, lines, leaders, volume, game_status, framerate_blockmove, framerate_2P_blockmove, game_speed, game_speed_2P, select_mode, hard, hard_tutorial, multi_tutorial, hard_time_setting
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
    hard_tutorial = False # 하드 튜토리얼 변수 추가
    multi_tutorial = False # 멀티 튜토리얼 변수 추가
    help = False
    select_mode = False
    gravity_mode = False #이 코드가 없으면 중력모드 게임을 했다가 Restart해서 일반모드로 갈때 중력모드로 게임이 진행됨#
    debug = False
    d = False
    e = False
    b = False
    u = False
    g = False
    hard_time_setting = False # 하드모드 시작하였을 때 타임 세팅을 시작하여 경과 시간을 계산하기 위해 추가한 변수
    start_ticks = pygame.time.get_ticks()
    textsize = False

    # 게임 음악 속도 조절 관련 변수
    CHANNELS = 1
    swidth = 2
    Change_RATE = 2

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
    ui_variables.intro_sound.set_volume(music_volume / 10)
    ui_variables.break_sound.set_volume(effect_volume / 10) # 소리 설정 부분도 set_volume 함수에 넣으면 됨
    ui_variables.intro_sound.play()
    game_status = ''
    pygame.mixer.music.load("assets/sounds/SFX_BattleMusic.wav")

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
            draw_image(screen, gamebackground_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
            draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
            #화면 회색으로 약간 불투명하게
            pause_surface = screen.convert_alpha() #투명 가능하도록
            pause_surface.fill((0, 0, 0, 0))  #투명한 검정색으로 덮기
            pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(board_width), int(board_height)])  #(screen, 색깔, 위치 x, y좌표, 너비, 높이)
            screen.blit(pause_surface, (0, 0))

        if hard:
            screen.fill(ui_variables.real_white)
            draw_image(screen, gamebackground_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
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
<<<<<<< HEAD
        #resume_button.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색
        #restart_button.draw(screen, (0, 0, 0))

        setting_button.draw(screen, (0, 0, 0))
=======
        resume_button.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색
        menu_button2.draw(screen, (0, 0, 0))
        help_button.draw(screen, (0, 0, 0))
>>>>>>> 2a0e0f9d8232bf48b40468d75a887f4e76dd76e9
        pause_quit_button.draw(screen, (0, 0, 0))

        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True

            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                pygame.display.update()
            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation, matrix)
                if event.key == K_ESCAPE:
                    pause = False
                    ui_variables.click_sound.play()
                    #pygame.mixer.music.unpause()
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                  
            elif event.type == pygame.MOUSEMOTION:
<<<<<<< HEAD
            #     if resume_button.isOver_2(pos):
            #         resume_button.image = clicked_resume_button_image
            #     else:
            #         resume_button.image = resume_button_image

            #     if restart_button.isOver_2(pos):
            #         restart_button.image = clicked_restart_button_image
            #     else:
            #         restart_button.image = restart_button_image

                if setting_button.isOver_2(pos):
                    setting_button.image = clicked_setting_button_image
                else:
                    setting_button.image = setting_button_image
=======
                if resume_button.isOver_2(pos):
                    resume_button.image = clicked_resume_button_image
                else:
                    resume_button.image = resume_button_image

                if menu_button2.isOver_2(pos):
                    menu_button2.image = clicked_menu_button_image
                else:
                    menu_button2.image = menu_button_image

                if help_button.isOver_2(pos):
                    help_button.image = clicked_help_button_image
                else:
                    help_button.image = help_button_image

>>>>>>> 2a0e0f9d8232bf48b40468d75a887f4e76dd76e9
                if pause_quit_button.isOver_2(pos):
                    pause_quit_button.image = clicked_quit_button_image
                else:
                    pause_quit_button.image = quit_button_image
                pygame.display.update()
            

            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                if pause_quit_button.isOver_2(pos):
                   ui_variables.click_sound.play()
                   done = True
                
<<<<<<< HEAD
                if setting_button.isOver_2(pos):
=======
                if help_button.isOver_2(pos):
>>>>>>> 2a0e0f9d8232bf48b40468d75a887f4e76dd76e9
                    ui_variables.click_sound.play()
                    setting = True

                if menu_button.isOver_2(pos):
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


    # Game screen
    elif start:
        #if time_attack:
         #   elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # 경과 시간 계산

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
                draw_mino(dx, dy, mino, rotation,matrix)
                draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)

                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation,matrix)

                # Move mino down
                if not is_bottom(dx, dy, mino, rotation,matrix):
                    dy += 1

                # Create new mino
                else:
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        score += 10 * level
                        draw_mino(dx, dy, mino, rotation,matrix)
                        screen.fill(ui_variables.real_white)
                        draw_image(screen, gamebackground_image, board_width * 0.5, board_height * 0.5, board_width, board_height)
                        draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                        pygame.display.update()
                        if is_stackable(next_mino1, matrix):
                            mino = next_mino1
                            next_mino1 = next_mino2
                            next_mino2 = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                        else:
                            start = False
                            game_status = 'start'
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
                erase_mino(dx, dy, mino, rotation,matrix)
                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    pause = True
                # Hard drop
                elif event.key == K_SPACE:
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation,matrix):
                        dy += 1
                    hard_drop = True
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                    draw_mino(dx, dy, mino, rotation,matrix)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                # Hold
                elif event.key == K_LSHIFT or event.key == K_c:
                    if hold == False:
                        ui_variables.move_sound.play()
                        if hold_mino == -1:
                            hold_mino = mino
                            mino = next_mino1
                            next_mino1 = next_mino2
                            next_mino2 = randint(1, 7)
                        else:
                            hold_mino, mino = mino, hold_mino
                        dx, dy = 3, 0
                        rotation = 0
                        hold = True
                    draw_mino(dx, dy, mino, rotation,matrix)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                # Turn right
                elif event.key == K_UP or event.key == K_x:
                    if is_turnable_r(dx, dy, mino, rotation,matrix):
                        ui_variables.move_sound.play()
                        rotation += 1
                    # Kick
                    elif is_turnable_r(dx, dy - 1, mino, rotation,matrix):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation += 1
                    elif is_turnable_r(dx + 1, dy, mino, rotation,matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation += 1
                    elif is_turnable_r(dx - 1, dy, mino, rotation,matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation += 1
                    elif is_turnable_r(dx, dy - 2, mino, rotation,matrix):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_r(dx + 2, dy, mino, rotation,matrix):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_r(dx - 2, dy, mino, rotation,matrix):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation += 1
                    if rotation == 4:
                        rotation = 0
                    draw_mino(dx, dy, mino, rotation,matrix)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                # Turn left
                elif event.key == K_z or event.key == K_LCTRL:
                    if is_turnable_l(dx, dy, mino, rotation,matrix):
                        ui_variables.move_sound.play()
                        rotation -= 1
                    # Kick
                    elif is_turnable_l(dx, dy - 1, mino, rotation,matrix):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation -= 1
                    elif is_turnable_l(dx + 1, dy, mino, rotation,matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation -= 1
                    elif is_turnable_l(dx - 1, dy, mino, rotation,matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation -= 1
                    elif is_turnable_l(dx, dy - 2, mino, rotation,matrix):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_l(dx + 2, dy, mino, rotation,matrix):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_l(dx - 2, dy, mino, rotation,matrix):
                        ui_variables.move_sound.play()
                        dx -= 2
                    if rotation == -1:
                        rotation = 3
                    draw_mino(dx, dy, mino, rotation,matrix)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                # Move left
                elif event.key == K_LEFT:
                    if not is_leftedge(dx, dy, mino, rotation,matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation,matrix)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                # Move right
                elif event.key == K_RIGHT:
                    if not is_rightedge(dx, dy, mino, rotation,matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                    draw_mino(dx, dy, mino, rotation,matrix)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)

        pygame.display.update()

    elif hard:
        if hard_time_setting == False:  # 타임 세팅이 안 되어 있으면
                start_ticks = pygame.time.get_ticks()  # 현재 시간을 타임어택 모드 시작 시간이라고 설정하고
                hard_time_setting = True  # 타임 세팅이 완료되었다고 바꾼다.

        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # 경과 시간 계산
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                # Set speed
                if not game_over:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_DOWN]:
                        pygame.time.set_timer(pygame.USEREVENT, framerate) #프레임 시간만큼 빠르게 소프트드롭
                    else:
                        pygame.time.set_timer(pygame.USEREVENT, game_speed)

                # Draw a mino
                draw_mino(dx, dy, mino, rotation, matrix)
                screen.fill(ui_variables.real_white)
                draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                pygame.display.update()

                current_time = pygame.time.get_ticks()
                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation, matrix)

                # Move mino down
                if not is_bottom(dx, dy, mino, rotation, matrix):
                    dy += 1

                
                # # Create new mino: 중력 모드
                # elif gravity_mode:
                #     if hard_drop or bottom_count == 6:
                #         if gravity(dx, dy, mino, rotation, matrix):
                #             erase_mino(dx, dy, mino, rotation, matrix)
                #         hard_drop = False
                #         bottom_count = 0
                #         score += 10 * level
                #         screen.fill(ui_variables.real_white)
                #         draw_image(screen, background_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                #         draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                #         pygame.display.update()
                #         if is_stackable(next_mino1, matrix):
                #             mino = next_mino1
                #             next_mino1 = next_mino2
                #             next_mino2 = randint(1, 7)
                #             dx, dy = 3, 0
                #             rotation = 0
                #             hold = False
                #         else:
                #             ui_variables.GameOver_sound.play()
                #             start = False
                #             game_status = 'start'
                #             game_over = True
                #             gravity_mode = False
                #             pygame.time.set_timer(pygame.USEREVENT, 1) #0.001초
                #     else:
                #         bottom_count += 1
                
                # Create new mino: 일반 모드
                else:
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        score += 10 * level
                        draw_mino(dx, dy, mino, rotation, matrix)
                        screen.fill(ui_variables.real_white)
                        draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                        draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                        pygame.display.update()

                        if is_stackable(next_mino1, matrix):
                            mino = next_mino1
                            next_mino1 = next_mino2
                            next_mino2 = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                        else:
                            ui_variables.GameOver_sound.play()
                            start = False
                            game_status = 'start'
                            game_over = True
                            pygame.time.set_timer(pygame.USEREVENT, 1) #0.001초
                    else:
                        bottom_count += 1

                # Erase line
                erase_count = 0
                rainbow_count = 0
                matrix_contents = []
                combo_value = 0

                for j in range(board_y+1):
                    is_full = True
                    for i in range(board_x):
                        if matrix[i][j] == 0 or matrix[i][j] == 9 : #빈 공간이거나, 장애물블록
                            is_full = False
                    if is_full: # 한 줄 꽉 찼을 때
                        erase_count += 1
                        k = j
                        combo_value += 1

                        # #rainbow보너스 점수
                        # rainbow = [1,2,3,4,5,6,7] #각 mino에 해당하는 숫자

                        for i in range(board_x):
                            matrix_contents.append(matrix[i][j]) #현재 클리어된 줄에 있는 mino 종류들 저장
                            
                        # rainbow_check = list(set(matrix_contents).intersection(rainbow)) #현재 클리어된 줄에 있는 mino와 mino의 종류중 겹치는 것 저장
                        # if rainbow == rainbow_check: #현재 클리어된 줄에 모든 종류 mino 있다면
                        #     rainbow_count += 1

                        while k > 0:
                            for i in range(board_x):
                                matrix[i][k] = matrix[i][k - 1]  # 남아있는 블록 한 줄씩 내리기(덮어쓰기)
                            k -= 1
                if erase_count >= 1:

                    # if rainbow_count >= 1:
                    #     score += 500 * rainbow_count #임의로 rainbow는 한 줄당 500점으로 잡음
                    #     rainbow_count = 0 #다시 초기화
                    #     screen.blit(ui_variables.rainbow_vector, (board_width * 0.28, board_height * 0.1)) #blit(이미지, 위치)
                    #     pygame.display.update()
                    #     pygame.time.delay(400) #0.4초

                    # previous_time = current_time
                    # combo_count += 1

                    #점수 계산
                    if erase_count == 1:
                        ui_variables.break_sound.play()
                        ui_variables.single_sound.play()
                        score += 50 * level * erase_count + combo_count
                    elif erase_count == 2:
                        ui_variables.break_sound.play()
                        ui_variables.double_sound.play()
                        ui_variables.double_sound.play()
                        score += 150 * level * erase_count + 2 * combo_count
                    elif erase_count == 3:
                        ui_variables.break_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        score += 350 * level * erase_count + 3 * combo_count
                    elif erase_count == 4:
                        ui_variables.break_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        score += 1000 * level * erase_count + 4 * combo_count
                        screen.blit(ui_variables.combo_4ring, (250, 160)) #blit(이미지, 위치)
                    total_time += 5 # 콤보 시 시간 5초 연장

                    for i in range(1, 11):
                        if combo_count == i:  # 1 ~ 10 콤보 이미지
                            screen.blit(ui_variables.large_combos[i - 1], (board_width * 0.27, board_height * 0.35)) #각 콤보 이미지에 대해 blit(이미지, 위치)
                            pygame.display.update()
                            pygame.time.delay(500)
                        elif combo_count > 10:  # 11 이상 콤보 이미지
                            pygame.display.update()
                            pygame.time.delay(300)

                    for i in range(1, 9): # 1~8의 콤보 사운드
                        if combo_count == i + 2:  # 3 ~ 11 콤보 사운드
                            ui_variables.combos_sound[i - 1].play()
                        if combo_count > 11:
                            ui_variables.combos_sound[8].play()
                if current_time - previous_time > 10000: #10초가 지나면
                    previous_time = current_time #현재 시간을 과거시간으로 하고
                    combo_count = 0 #콤보 수 초기화


                # Increase level
                goal -= erase_count
                if goal < 1 and level < 15:
                    level += 1
                    ui_variables.LevelUp_sound.play()
                    goal += level * 5
                    framerate = int(framerate-speed_change)
                    Change_RATE += 1
                    # set_music_playing_speed(CHANNELS, swidth, Change_RATE)

            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation, matrix)
                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    pause = True
                # Hard drop
                elif event.key == K_SPACE:
                    ui_variables.fall_sound.play()
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation, matrix):
                        dy += 1
                    hard_drop = True
                    pygame.time.set_timer(pygame.USEREVENT, framerate)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                    pygame.display.update()
                elif event.key == K_j :
                    framerate = int(framerate-speed_change)
                    print(framerate)

                # Hold
                elif event.key == K_RSHIFT : #keyboard 변경하기
                    if hold == False:
                        ui_variables.move_sound.play()
                        if hold_mino == -1:
                            hold_mino = mino
                            mino = next_mino1
                            next_mino1 = next_mino2
                            next_mino2 = randint(1, 7)
                        else:
                            hold_mino, mino = mino, hold_mino
                        dx, dy = 3, 0
                        rotation = 0
                        hold = True
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)

                #dx, dy는 각각 좌표위치 이동에 해당하며, rotation은 mino.py의 테트리스 블록 회전에 해당함
                # Turn right
                elif event.key == K_UP:
                    if is_turnable_r(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        rotation += 1
                    # Kick
                    elif is_turnable_r(dx, dy - 1, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation += 1
                    elif is_turnable_r(dx + 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation += 1
                    elif is_turnable_r(dx - 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation += 1
                    elif is_turnable_r(dx, dy - 2, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_r(dx + 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_r(dx - 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation += 1
                    if rotation == 4:
                        rotation = 0
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                # Turn left
                elif event.key == K_m:
                    if is_turnable_l(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        rotation -= 1
                    # Kick
                    elif is_turnable_l(dx, dy - 1, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation -= 1
                    elif is_turnable_l(dx + 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation -= 1
                    elif is_turnable_l(dx - 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation -= 1
                    elif is_turnable_l(dx, dy - 2, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_l(dx + 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_l(dx - 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 2
                    if rotation == -1:
                        rotation = 3
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)

                # Move left
                elif event.key == K_LEFT:
                    if not is_leftedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                # Move right
                elif event.key == K_RIGHT:
                    if not is_rightedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)

                # # rainbow test
                # elif event.key == K_F1:
                #     ui_variables.click_sound.play()
                #     matrix[0][20] = 7 #빨
                #     matrix[1][20] = 7 #빨
                #     matrix[2][20] = 3#주
                #     matrix[3][20] = 3#주
                #     matrix[4][20] = 4#노
                #     matrix[5][20] = 5#초
                #     matrix[6][20] = 5#초
                #     matrix[7][20] = 1#하
                #     matrix[8][20] = 2#파
                #     mino = 6
                # debug mode block change

                elif debug:
                    if event.key == K_1:
                        ui_variables.click_sound.play()
                        mino = 1 #빨
                    if event.key == K_2:
                        ui_variables.click_sound.play()
                        mino = 2 #빨
                    if event.key == K_3:
                        ui_variables.click_sound.play()
                        mino = 3 #빨
                    if event.key == K_4:
                        ui_variables.click_sound.play()
                        mino = 4 #빨
                    if event.key == K_5:
                        ui_variables.click_sound.play()
                        mino = 5 #빨
                    if event.key == K_6:
                        ui_variables.click_sound.play()
                        mino = 6 #빨
                    if event.key == K_7:
                        ui_variables.click_sound.play()
                        mino = 7 #빨

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌
                if board_width>= mid_width: #화면 사이즈가 큰 경우
                    textsize=True #큰 글자크기 사용
                if board_width < mid_width: #화면 사이즈가 작은 경우
                    textsize=False #작은 글자크기 사용

                block_size = int(board_height * 0.045)
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                # for i in range(len(button_list)):
                #         button_list[i].change(board_width, board_height)

        if total_time - elapsed_time < 0: # 60초가 지났으면
            ui_variables.GameOver_sound.play()
            start = False
            game_status = 'start'
            game_over = True
            hard_mode = False
            pygame.time.set_timer(pygame.USEREVENT, 1)

        pygame.display.update()
        
    elif pvp:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                # Set speed
                if not game_over:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_s]:  # 프레임만큼의 시간으로 소프트드롭 되도록 함
                        pygame.time.set_timer(pygame.USEREVENT, framerate)
                    elif keys_pressed[K_DOWN]:  # 프레임만큼의 시간으로 소프트드롭 되도록 함
                        pygame.time.set_timer(pygame.USEREVENT, framerate_2P)
                    else:
                        pygame.time.set_timer(pygame.USEREVENT, game_speed)  # 기본 게임속도
                        pygame.time.set_timer(pygame.USEREVENT, game_speed_2P)

                # Draw a mino
                draw_mino(dx, dy, mino, rotation, matrix)
                draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P,
                                goal, goal_2P)

                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation, matrix)
                    erase_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)

                # Move mino down
                if not is_bottom(dx, dy, mino, rotation, matrix):
                    dy += 1

                # Create new mino
                else:
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        draw_mino(dx, dy, mino, rotation, matrix)

                        if is_stackable(next_mino1, matrix):
                            mino = next_mino1
                            # next_mino1 = next_mino2
                            next_mino1 = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                            score += 10 * level
                        else:  # 더이상 쌓을 수 없으면 게임오버
                            pvp = True
                            game_status = 'pvp'

                            if score >= score_2P:
                                draw_image(screen, gameover_image, board_width * 0.15, board_height * 0.5,
                                           int(board_width * 0.25),
                                           int(board_height * 0.45))  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                            else:
                                ui_variables.GameOver_sound.play()
                                draw_image(screen, pvp_lose_image, board_width * 0.15, board_height * 0.5,
                                           int(board_width * 0.25),
                                           int(board_height * 0.6))  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                                draw_image(screen, pvp_win_image, board_width * 0.6, board_height * 0.5,
                                           int(board_width * 0.25),
                                           int(board_height * 0.55))  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                                pvp = False
                                pygame.mixer.music.stop()
                                if game_status == 'start':
                                    start = True
                                    pygame.mixer.music.play(-1)
                                if game_status == 'pvp':
                                    pvp = True
                                    pygame.mixer.music.play(-1)
                                ui_variables.click_sound.play()
                                game_over = False
                                pause = False
                    else:
                        bottom_count += 1

                # Move mino down
                if not is_bottom(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                    dy_2P += 1

                # Create new mino
                else:
                    if hard_drop_2P or bottom_count_2P == 6:
                        hard_drop_2P = False
                        bottom_count_2P = 0
                        draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)

                        if is_stackable(next_mino1_2P, matrix_2P):
                            mino_2P = next_mino1_2P
                            next_mino1_2P = randint(1, 7)
                            dx_2P, dy_2P = 3, 0
                            rotation_2P = 0
                            hold_2P = False
                            score_2P += 10 * level_2P
                        else:  # 더이상 쌓을 수 없으면 게임오버
                            pvp = True
                            gagame_status = 'pvp'
                            if score <= score_2P:
                                draw_image(screen, gameover_image, board_width * 0.6, board_height * 0.5,
                                           int(board_width * 0.25),
                                           int(board_height * 0.45))  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                            else:
                                ui_variables.GameOver_sound.play()
                                draw_image(screen, pvp_win_image, board_width * 0.15, board_height * 0.5,
                                           int(board_width * 0.25),
                                           int(board_height * 0.55))  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                                draw_image(screen, pvp_lose_image, board_width * 0.6, board_height * 0.5,
                                           int(board_width * 0.25),
                                           int(board_height * 0.6))  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                                pvp = False
                                pygame.mixer.music.stop()
                                if game_status == 'start':
                                    start = True
                                    pygame.mixer.music.play(-1)
                                if game_status == 'pvp':
                                    pvp = True
                                    pygame.mixer.music.play(-1)
                                ui_variables.click_sound.play()
                                game_over = False
                                pause = False
                    else:
                        bottom_count_2P += 1

                # Erase line
                # 콤보 카운트
                erase_count = 0
                erase_count_2P = 0
                combo_value = 0
                combo_value_2P = 0
                attack_line = 0
                attack_line_2P = 0

                for j in range(board_y + 1):
                    is_full = True
                    for i in range(board_x):
                        if matrix[i][j] == 0 or matrix[i][j] == 9:  # 빈 곳이거나 장애물 블록이 있는 경우
                            is_full = False  # 클리어 되지 못함
                    if is_full:
                        erase_count += 1
                        attack_line += 1
                        k = j
                        combo_value += 1
                        while k > 0:  # y좌표가 matrix 안에 있는 동안
                            for i in range(board_x):  # 해당 줄의 x좌표들 모두
                                matrix[i][k] = matrix[i][k - 1]  # 한줄씩 밑으로 내림
                            k -= 1

                for j in range(board_y + 1):
                    is_full = True
                    for i in range(board_x):
                        if matrix_2P[i][j] == 0 or matrix_2P[i][j] == 9:  # 빈 곳이거나 장애물 블록이 있는 경우
                            is_full = False  # 클리어 되지 못함
                    if is_full:
                        erase_count_2P += 1
                        attack_line_2P += 1
                        k = j
                        combo_value_2P += 1
                        while k > 0:  # y좌표가 matrix 안에 있는 동안
                            for i in range(board_x):  # 해당 줄의 x좌표들 모두
                                matrix_2P[i][k] = matrix_2P[i][k - 1]  # 한줄씩 밑으로 내림
                            k -= 1

                while attack_line >= 1:  # 2p에게 공격 보내기
                    for i in range(board_x):
                        if matrix_2P[i][board_y - attack_point] == 0:  # 비어있는 공간을
                            matrix_2P[i][board_y - attack_point] = 9  # 모두 장애물 블록으로 채움
                    attack_line -= 1
                    attack_point += 1

                while attack_line_2P >= 1:  # 1p에게 공격 보내기
                    for i in range(board_x):
                        if matrix[i][board_y - attack_point_2P] == 0:  # 비어있는 공간을
                            matrix[i][board_y - attack_point_2P] = 9  # 모두 장애물 블록으로 채움
                    attack_line_2P -= 1
                    attack_point_2P += 1

                # 1P
                if erase_count >= 1:
                    combo_count += 1
                    if erase_count == 1:
                        ui_variables.break_sound.play()
                        ui_variables.single_sound.play()
                        score += 50 * level * erase_count + combo_count

                    elif erase_count == 2:
                        ui_variables.break_sound.play()
                        ui_variables.double_sound.play()
                        ui_variables.double_sound.play()
                        score += 150 * level * erase_count + 2 * combo_count

                    elif erase_count == 3:
                        ui_variables.break_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        score += 350 * level * erase_count + 3 * combo_count

                    elif erase_count == 4:
                        ui_variables.break_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        score += 1000 * level * erase_count + 4 * combo_count

                        screen.blit(ui_variables.combo_4ring, (250, 160))  # blit(이미지, 위치)

                    for i in range(1, 11):
                        if combo_count == i:  # 1 ~ 10 콤보 이미지
                            screen.blit(ui_variables.large_combos[i - 1], (124, 190))  # blits the combo number
                        elif combo_count > 10:  # 11 이상 콤보 이미지
                            screen.blit(tetris4, (100, 190))  # blits the combo number

                    for i in range(1, 10):
                        if combo_count == i + 2:  # 3 ~ 11 콤보 사운드
                            ui_variables.combos_sound[i - 1].play()

                # Increase level
                goal -= erase_count
                if goal < 1 and level < 15:
                    level += 1
                    ui_variables.LevelUp_sound.play()
                    goal += level * 5
                    framerate = int(framerate - speed_change)
                if level > level_2P and Change_RATE < level + 1:
                    Change_RATE += 1
                    set_music_playing_speed(CHANNELS, swidth, Change_RATE)
                # 2P
                if erase_count_2P >= 1:
                    combo_count_2P += 1
                    if erase_count_2P == 1:
                        ui_variables.break_sound.play()
                        ui_variables.single_sound.play()
                        score_2P += 50 * level_2P * erase_count_2P + combo_count_2P

                    elif erase_count_2P == 2:
                        ui_variables.break_sound.play()
                        ui_variables.double_sound.play()
                        ui_variables.double_sound.play()
                        score_2P += 150 * level_2P * erase_count_2P + 2 * combo_count_2P

                    elif erase_count_2P == 3:
                        ui_variables.break_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        score_2P += 350 * level_2P * erase_count_2P + 3 * combo_count_2P

                    elif erase_count_2P == 4:
                        ui_variables.break_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        score_2P += 1000 * level_2P * erase_count_2P + 4 * combo_count_2P

                        screen.blit(ui_variables.combo_4ring, (250, 160))  # blit(이미지, 위치)

                    for i in range(1, 11):
                        if combo_count_2P == i:  # 1 ~ 10 콤보 이미지
                            screen.blit(ui_variables.large_combos[i - 1], (124, 190))  # blit(이미지, 위치)
                        elif combo_count_2P > 10:  # 11 이상 콤보 이미지
                            screen.blit(tetris4, (100, 190))  # blit(이미지, 위치)

                    for i in range(1, 10):
                        if combo_count_2P == i + 2:  # 3 ~ 11 콤보 사운드
                            ui_variables.combos_sound[i - 1].play()

                # Increase level
                goal_2P -= erase_count_2P
                if goal_2P < 1 and level_2P < 15:
                    level_2P += 1
                    ui_variables.LevelUp_sound.play()
                    goal_2P += level_2P * 5
                    framerate_2P = int(framerate_2P - speed_change)
                if level < level_2P and Change_RATE < level_2P + 1:
                    Change_RATE += 1
                    set_music_playing_speed(CHANNELS, swidth, Change_RATE)

            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation, matrix)
                erase_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)

                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    pause = True

                # dx, dy는 각각 좌표위치 이동에 해당하며, rotation은 mino.py의 테트리스 블록 회전에 해당함
                # Hard drop
                elif event.key == K_e:  # 왼쪽창#
                    ui_variables.fall_sound.play()
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation, matrix):
                        dy += 1
                    hard_drop = True
                    pygame.time.set_timer(pygame.USEREVENT, framerate)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level,
                                    level_2P, goal, goal_2P)
                elif event.key == K_SPACE:  # 오른쪽창#
                    ui_variables.fall_sound.play()
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        dy_2P += 1
                    hard_drop_2P = True
                    pygame.time.set_timer(pygame.USEREVENT, framerate_2P)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level,
                                    level_2P, goal, goal_2P)

                # Hold
                elif event.key == K_LSHIFT:
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
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level,
                                    level_2P, goal, goal_2P)
                elif event.key == K_RSHIFT:
                    if hold_2P == False:
                        ui_variables.move_sound.play()
                        if hold_mino_2P == -1:
                            hold_mino_2P = mino_2P
                            mino_2P = next_mino1_2P
                            next_mino1_2P = randint(1, 7)
                        else:
                            hold_mino_2P, mino_2P = mino_2P, hold_mino_2P
                        dx_2P, dy_2P = 3, 0
                        rotation_2P = 0
                        hold_2P = True
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level,
                                    level_2P, goal, goal_2P)

                # Turn right
                elif event.key == K_w:  # 왼쪽창#
                    if is_turnable_r(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        rotation += 1
                    # Kick
                    elif is_turnable_r(dx, dy - 1, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation += 1
                    elif is_turnable_r(dx + 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation += 1
                    elif is_turnable_r(dx - 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation += 1
                    elif is_turnable_r(dx, dy - 2, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_r(dx + 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_r(dx - 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation += 1
                    if rotation == 4:
                        rotation = 0
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level,
                                    level_2P, goal, goal_2P)
                elif event.key == K_UP:  # 오른쪽창#
                    if is_turnable_r(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        rotation_2P += 1
                    # Kick
                    elif is_turnable_r(dx_2P, dy_2P - 1, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dy_2P -= 1
                        rotation_2P += 1
                    elif is_turnable_r(dx_2P + 1, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P += 1
                        rotation_2P += 1
                    elif is_turnable_r(dx_2P - 1, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P -= 1
                        rotation_2P += 1
                    elif is_turnable_r(dx_2P, dy_2P - 2, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dy_2P -= 2
                        rotation_2P += 1
                    elif is_turnable_r(dx_2P + 2, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P += 2
                        rotation_2P += 1
                    elif is_turnable_r(dx_2P - 2, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P -= 2
                        rotation_2P += 1
                    if rotation_2P == 4:
                        rotation_2P = 0
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level,
                                    level_2P, goal, goal_2P)

                # Turn left
                elif event.key == K_q:
                    if is_turnable_l(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        rotation -= 1
                    # Kick
                    elif is_turnable_l(dx, dy - 1, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation -= 1
                    elif is_turnable_l(dx + 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation -= 1
                    elif is_turnable_l(dx - 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation -= 1
                    elif is_turnable_l(dx, dy - 2, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation -= 1
                    elif is_turnable_l(dx + 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation -= 1
                    elif is_turnable_l(dx - 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation -= 1
                    if rotation == -1:
                        rotation = 3
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level,
                                    level_2P, goal, goal_2P)
                elif event.key == K_m:  # 오른쪽창#
                    if is_turnable_l(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        rotation_2P -= 1
                    # Kick
                    elif is_turnable_l(dx_2P, dy_2P - 1, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dy_2P -= 1
                        rotation_2P -= 1
                    elif is_turnable_l(dx_2P + 1, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P += 1
                        rotation_2P -= 1
                    elif is_turnable_l(dx_2P - 1, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P -= 1
                        rotation_2P -= 1
                    elif is_turnable_l(dx_2P, dy_2P - 2, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dy_2P -= 2
                        rotation_2P -= 1
                    elif is_turnable_l(dx_2P + 2, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P += 2
                        rotation_2P -= 1
                    elif is_turnable_l(dx_2P - 2, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P -= 2
                        rotation_2P -= 1
                    if rotation_2P == -1:
                        rotation_2P = 3
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level,
                                    level_2P, goal, goal_2P)

                # Move left
                elif event.key == K_a:  # key = pygame.key.get_pressed()
                    if not is_leftedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(pygame.KEYUP, framerate_blockmove)
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level,
                                    level_2P, goal, goal_2P)
                # Move right
                elif event.key == K_d:
                    if not is_rightedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(pygame.KEYUP, framerate_blockmove)
                        dx += 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level,
                                    level_2P, goal, goal_2P)

                # Move left
                elif event.key == K_LEFT:
                    if not is_leftedge(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(pygame.KEYUP, framerate_2P_blockmove)
                        dx_2P -= 1
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level,
                                    level_2P, goal, goal_2P)
                # Move right
                elif event.key == K_RIGHT:
                    if not is_rightedge(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(pygame.KEYUP, framerate_2P_blockmove)
                        dx_2P += 1
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level,
                                    level_2P, goal, goal_2P)

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate - 0.1) < (board_height / board_width) < (
                        board_rate + 0.05)):  # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate)  # 너비를 적정 비율로 바꿔줌
                    board_height = int(board_width * board_rate)  # 높이를 적정 비율로 바꿔줌
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)  # 블록 크기비율 고정
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)

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
        hard_tutorial_button.draw(screen, (0,0,0))
        multi_tutorial_button.draw(screen, (0,0,0))

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

                if hard_tutorial_button.isOver_2(pos):
                    hard_tutorial_button.image = clicked_hard_tutorial_button_image
                else:
                    hard_tutorial_button.image = hard_tutorial_button_image

                if multi_tutorial_button.isOver_2(pos):
                    multi_tutorial_button.image = clicked_multi_tutorial_button_image
                else:
                    multi_tutorial_button.image = multi_tutorial_button_image

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
                if hard_tutorial_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    hard_tutorial = True
                    initalize = True
                    # pygame.mixer.music.play(-1)
                    # ui_variables.intro_sound.stop()
                if multi_tutorial_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    multi_tutorial = True
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

    elif screen_setting:
            screen.fill(ui_variables.pinkpurple)
            draw_image(screen, background_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
            select_mode_button.draw(screen, (0,0,0))
            setting_button.draw(screen, (0,0,0))
            score_board_button.draw(screen, (0,0,0))
            quit_button.draw(screen, (0,0,0))
            #배경 약간 어둡게
            leaderboard_icon.draw(screen, (0, 0, 0))
            pause_surface = screen.convert_alpha() #투명 가능하도록
            pause_surface.fill((0, 0, 0, 0)) #투명한 검정색으로 덮기
            pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(board_width), int(board_height)]) #(screen, 색깔, 위치 x, y좌표, 너비, 높이)

            screen.blit(pause_surface, (0, 0))

            draw_image(screen, setting_board_image, board_width * 0.5, board_height * 0.5, int(board_height * 1.3), board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
            smallsize_check_button.draw(screen, (0, 0, 0))
            bigsize_check_button.draw(screen, (0, 0, 0))
            midiumsize_check_button.draw(screen, (0, 0, 0))
            back_button.draw(screen, (0, 0, 0))

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()

                if event.type == QUIT:
                    done = True
                elif event.type == USEREVENT:
                    pygame.time.set_timer(pygame.USEREVENT, 300) #0.3초로 설정
                    pygame.display.update()

                elif event.type == pygame.MOUSEMOTION:
                    if back_button.isOver(pos):
                        back_button.image = clicked_back_button_image
                    else:
                        back_button.image = back_button_image

                    pygame.display.update()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.isOver(pos):
                        ui_variables.click_sound.play()
                        screen_setting = False
                    if smallsize_check_button.isOver(pos):
                        ui_variables.click_sound.play()
                        board_width = 800
                        board_height = 450
                        block_size = int(board_height * 0.045) #블록 크기 비율 고정
                        screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)
                        textsize=False
                        
                        #for i in range(len(button_list):
                        #    button_list[i].change(board_width, board_height)
                        pygame.display.update()
                        

                    if midiumsize_check_button.isOver(pos):
                        ui_variables.click_sound.play()
                        board_width = 1200
                        board_height = 675
                        block_size = int(board_height * 0.045) #블록 크기 비율 고정
                        screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)
                        textsize=True
                        
                        #for i in range(len(button_list)):
                        #    button_list[i].change(board_width, board_height)
                        
                        pygame.display.update()

                    if bigsize_check_button.isOver(pos):
                        ui_variables.click_sound.play()
                        board_width = 1600
                        board_height = 900
                        block_size = int(board_height * 0.045) #블록 크기 비율 고정
                        screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)
                        textsize=True
                        
                        #for i in range(len(button_list)):
                        #    button_list[i].change(board_width, board_height)
                        pygame.display.update()
                        
    elif volume_setting:
        #배경 약간 어둡게
        leaderboard_icon.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색#
        pause_surface = screen.convert_alpha() #투명 가능하도록
        pause_surface.fill((0, 0, 0, 0)) #투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(board_width), int(board_height)]) #(screen, 색깔, 위치 x, y좌표, 너비, 높이)
        screen.blit(pause_surface, (0, 0)) #위치 비율 고정

        #draw_image(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        draw_image(screen, setting_board_image, board_width * 0.5, board_height * 0.5, int(board_height * 1.3), board_height)
        draw_image(screen, number_board, board_width * 0.45, board_height * 0.53, int(board_width * 0.09), int(board_height * 0.1444))
        draw_image(screen, number_board, board_width * 0.45, board_height * 0.73, int(board_width * 0.09), int(board_height * 0.1444))
        mute_button.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색#
        effect_plus_button.draw(screen, (0, 0, 0))
        effect_minus_button.draw(screen, (0, 0, 0))
        sound_plus_button.draw(screen, (0, 0, 0))
        sound_minus_button.draw(screen, (0, 0, 0))
        #음소거 추가#
        effect_sound_on_button.draw(screen,(0,0,0))
        music_sound_on_button.draw(screen,(0,0,0))
<<<<<<< HEAD
=======
        BGM1_sound_on_button.draw(screen,(0,0,0))
        BGM2_sound_on_button.draw(screen,(0,0,0))
        BGM3_sound_on_button.draw(screen,(0,0,0))
>>>>>>> 2a0e0f9d8232bf48b40468d75a887f4e76dd76e9
        back_button.draw(screen, (0, 0, 0))

        #render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
        music_volume_text = ui_variables.h5.render('Music Volume', 1, ui_variables.grey_1)
        effect_volume_text = ui_variables.h5.render('Effect Volume', 1, ui_variables.grey_1)
        screen.blit(music_volume_text, (board_width * 0.4, board_height * 0.4)) #위치 비율 고정
        screen.blit(effect_volume_text, (board_width * 0.4, board_height * 0.6)) #위치 비율 고정

        music_volume_text = ui_variables.h5.render('Music On/Off', 1, ui_variables.grey_1)
        effect_volume_text = ui_variables.h5.render('Effect On/Off', 1, ui_variables.grey_1)
        screen.blit(music_volume_text, (board_width * 0.6, board_height * 0.4)) #위치 비율 고정
        screen.blit(effect_volume_text, (board_width * 0.6, board_height * 0.6)) #위치 비율 고정

        music_volume_size_text = ui_variables.h4.render(str(music_volume), 1, ui_variables.grey_1)
        effect_volume_size_text = ui_variables.h4.render(str(effect_volume), 1, ui_variables.grey_1)
        screen.blit(music_volume_size_text, (board_width * 0.43, board_height * 0.5)) #위치 비율 고정
        screen.blit(effect_volume_size_text, (board_width * 0.43, board_height * 0.7)) #위치 비율 고정

<<<<<<< HEAD
=======
        BGM1_text = ui_variables.h5.render('BGM1', 1, ui_variables.grey_1)
        BGM2_text = ui_variables.h5.render('BGM2', 1, ui_variables.grey_1)
        BGM3_text = ui_variables.h5.render('BGM3', 1, ui_variables.grey_1)
        screen.blit(BGM1_text, (board_width * 0.75, board_height * 0.3)) #위치 비율 고정
        screen.blit(BGM2_text, (board_width * 0.75, board_height * 0.5)) #위치 비율 고정
        screen.blit(BGM3_text, (board_width * 0.75, board_height * 0.7)) #위치 비율 고정

>>>>>>> 2a0e0f9d8232bf48b40468d75a887f4e76dd76e9
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300) #0.3초로 설정

                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver(pos):
                    back_button.image = clicked_back_button_image
                else:
                    back_button.image = back_button_image

                if effect_plus_button.isOver(pos):
                    effect_plus_button.image = clicked_plus_button_image
                else:
                    effect_plus_button.image = plus_button_image

                if effect_minus_button.isOver(pos):
                    effect_minus_button.image = clicked_minus_button_image
                else:
                    effect_minus_button.image = minus_button_image

                if sound_plus_button.isOver(pos):
                    sound_plus_button.image = clicked_plus_button_image
                else:
                    sound_plus_button.image = plus_button_image

                if sound_minus_button.isOver(pos):
                    sound_minus_button.image = clicked_minus_button_image
                else:
                    sound_minus_button.image = minus_button_image

                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    volume_setting = False
                if sound_plus_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if music_volume >= 10: #음량 최대크기
                        music_volume = 10
                    else:
                        music_sound_on_button.image=sound_on_button_image
                        music_volume += 1
                if sound_minus_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if music_volume <= 0: #음량 최소크기
                        music_volume = 0
                        music_sound_on_button.image=sound_off_button_image
                    else:
                        if music_volume == 1:
                            music_sound_on_button.image=sound_off_button_image
                            music_volume -= 1
                        else:
                            music_sound_on_button.image=sound_on_button_image
                            music_volume -= 1
                if effect_plus_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if effect_volume >= 10: #음량 최대크기
                        effect_volume = 10
                    else:
                        effect_sound_on_button.image=sound_on_button_image
                        effect_volume += 1
                if effect_minus_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if effect_volume <= 0: #음량 최소크기
                        effect_volume = 0
                        effect_sound_on_button.image=sound_off_button_image
                    else:
                        if effect_volume == 1:
                            effect_sound_on_button.image=sound_off_button_image
                            effect_volume -= 1
                        else:
                            effect_sound_on_button.image=sound_on_button_image
                            effect_volume -= 1
<<<<<<< HEAD
=======
                #BGM 선택 기능 추가#
                if BGM1_sound_on_button.isOver(pos): 
                    #ui_variables.intro_sound.("assets/sounds/BGM2.wav")#
                    ui_variables.intro_sound.stop()
                    ui_variables.intro_sound = pygame.mixer.Sound("assets/sounds/BGM1.wav")
                    ui_variables.intro_sound.play()
                if BGM2_sound_on_button.isOver(pos): 
                    #ui_variables.intro_sound.("assets/sounds/BGM2.wav")#
                    ui_variables.intro_sound.stop()
                    ui_variables.intro_sound = pygame.mixer.Sound("assets/sounds/BGM2.wav")
                    ui_variables.intro_sound.play()
                if BGM3_sound_on_button.isOver(pos): 
                    #ui_variables.intro_sound.("assets/sounds/BGM2.wav")#
                    ui_variables.intro_sound.stop()
                    ui_variables.intro_sound = pygame.mixer.Sound("assets/sounds/BGM3.wav")
                    ui_variables.intro_sound.play()    
                    
                   
>>>>>>> 2a0e0f9d8232bf48b40468d75a887f4e76dd76e9
                #음소거 추가#
                if music_sound_on_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if music_volume == 0 :
                        music_volume = 5 #중간 음량으로
                        music_sound_on_button.image=sound_on_button_image
                    else:
                        music_volume = 0
                        music_sound_off_button.draw(screen,(0,0,0)) #rgb(0,0,0) = 검정색
                        music_sound_on_button.image=sound_off_button_image
                if effect_sound_on_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if effect_volume == 0 :
                        effect_volume = 5  #중간 음량으로
                        effect_sound_on_button.image=sound_on_button_image
                    else:
                        effect_volume = 0
                        effect_sound_off_button.draw(screen,(0,0,0))
                        effect_sound_on_button.image=sound_off_button_image
                if mute_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if (effect_volume == 0) and (music_volume == 0):
                        music_volume = 5  #중간 음량으로
                        effect_volume = 5  #중간 음량으로
                        mute_button.image=mute_button_image
                    else:
                        music_volume = 0 #최소 음량으로
                        effect_volume = 0 #최소 음량으로
                        default_button.draw(screen,(0,0,0))
                        mute_button.image=default_button_image
<<<<<<< HEAD
=======
                

>>>>>>> 2a0e0f9d8232bf48b40468d75a887f4e76dd76e9

                set_volume()

    elif setting:
        select_mode_button.draw(screen, (0,0,0))
        setting_button.draw(screen, (0,0,0))
        score_board_button.draw(screen, (0,0,0))
        quit_button.draw(screen, (0,0,0))
        #배경 약간 어둡게
        leaderboard_icon.draw(screen, (0, 0, 0))
        pause_surface = screen.convert_alpha() #투명 가능하도록
        pause_surface.fill((0, 0, 0, 0))  #투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(board_width), int(board_height)]) #(screen, 색깔, 위치 x, y좌표, 너비, 높이)
        screen.blit(pause_surface, (0, 0))

        draw_image(screen, setting_board_image, board_width * 0.5, board_height * 0.5, int(board_height * 1.3), board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)

        screen_icon.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색
        volume_icon.draw(screen, (0, 0, 0))

        back_button.draw(screen, (0, 0, 0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300) #0.3초로 설정
                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver(pos):
                    back_button.image = clicked_back_button_image
                else:
                    back_button.image = back_button_image

                if volume_icon.isOver(pos):
                    volume_icon.image = clicked_volume_vector
                else:
                    volume_icon.image = volume_vector

                if screen_icon.isOver(pos):
                    screen_icon.image = clicked_screen_vector
                else:
                    screen_icon.image = screen_vector

                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    setting = False

                if volume_icon.isOver(pos):
                    ui_variables.click_sound.play()
                    volume_setting = True

                if screen_icon.isOver(pos):
                    ui_variables.click_sound.play()
                    screen_setting = True

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌
                if board_width>= mid_width: #화면 사이즈가 큰 경우
                    textsize=True #큰 글자크기 사용
                if board_width < mid_width: #화면 사이즈가 작은 경우
                    textsize=False #작은 글자크기 사용

                block_size = int(board_height * 0.045) #블록 크기 고정
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)
                '''
                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)
                '''

    elif pause:
        pygame.mixer.music.pause()

    
  
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
                if setting_button.isOver(pos):
                    ui_variables.click_sound.play()
                    setting = True
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
