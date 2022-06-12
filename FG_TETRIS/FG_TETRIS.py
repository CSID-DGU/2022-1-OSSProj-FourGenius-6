# -*-coding:utf-8-*-
# PYTRIS™ Copyright (c) 2017 Jason Kim All Rights Reserved.

from contextlib import nullcontext
import pygame
import operator

from mino import *
from random import *
from pygame.locals import *


# Define
block_size = 17  # Height, width of single block
width = 10  # Board에 가로로 들어갈 칸의 개수
height = 20  # Board에 세로로 들어갈 칸의 개수
framerate = 30  # Bigger -> Slower

total_time = 60  # 타임 어택 시간
speed_change = 2  # 레벨별 블록 하강 속도 상승 정도

board_width = 800  # 전체 창의 가로 길이
board_height = 450  # 전체 창의 세로 길이
board_rate = 0.5625  # 가로세로비율

min_width = 400
min_height = 225
mid_width = 1200

# 기본 볼륨
music_volume = 5
effect_volume = 5

mino_matrix_x = 4  # mino는 4*4 배열이어서 이를 for문에 사용
mino_matrix_y = 4  # mino는 4*4 배열이어서 이를 for문에 사용
board_x = 10
board_y = 20

total_time = 60  # 타임 어택 시간

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)
pygame.time.set_timer(pygame.USEREVENT, framerate * 10)
pygame.display.set_caption("FG_TETRIS")

initialize = True  # Start Screen 에서 set_initial_values()로 초기화할지 여부를 boolean으로 저장


class ui_variables:
    # Fonts
    font_path = "assets/fonts/a옛날사진관3.ttf"
    font_path_b = "assets/fonts/a옛날사진관3.ttf"
    font_path_i = "assets/fonts/a옛날사진관3.ttf"

    h1 = pygame.font.Font(font_path, 50)
    h2 = pygame.font.Font(font_path, 30)
    h3 = pygame.font.Font(font_path, 25)
    h4 = pygame.font.Font(font_path, 20)
    h5 = pygame.font.Font(font_path, 13)
    h6 = pygame.font.Font(font_path, 10)

    h1_b = pygame.font.Font(font_path_b, 50)
    h2_b = pygame.font.Font(font_path_b, 30)

    h2_i = pygame.font.Font(font_path_i, 30)
    h5_i = pygame.font.Font(font_path_i, 13)

    # Sounds
    pygame.mixer.music.load("assets/sounds/BGM1.wav")  # 음악 불러옴
    pygame.mixer.music.set_volume(0.5)  # 이 부분도 필요 없음, set_volume에 추가해야 함
    intro_sound = pygame.mixer.Sound("assets/sounds/intro.wav")
    fall_sound = pygame.mixer.Sound("assets/sounds/SFX_Fall.wav")
    break_sound = pygame.mixer.Sound("assets/sounds/SFX_Break.wav")
    click_sound = pygame.mixer.Sound("assets/sounds/SFX_ButtonUp.wav")  # 여기부터
    move_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceMoveLR.wav")
    drop_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceHardDrop.wav")
    single_sound = pygame.mixer.Sound(
        "assets/sounds/SFX_SpecialLineClearSingle.wav")
    double_sound = pygame.mixer.Sound(
        "assets/sounds/SFX_SpecialLineClearDouble.wav")
    triple_sound = pygame.mixer.Sound(
        "assets/sounds/SFX_SpecialLineClearTriple.wav")  # 여기까지는 기존코드
    tetris_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialTetris.wav")
    LevelUp_sound = pygame.mixer.Sound("assets/sounds/SFX_LevelUp.wav")
    GameOver_sound = pygame.mixer.Sound("assets/sounds/SFX_GameOver.wav")

    # 레벨업 이미지
    LevelUp_vector = pygame.image.load('assets/vector/Level_Up.png')

    # # Combo graphic
    # combos = []
    # large_combos = []
    # combo_ring = pygame.image.load("assets/Combo/4combo ring.png")  # 4블록 동시제거 그래픽
    # combo_4ring = pygame.transform.smoothscale(combo_ring, (200, 100)) #이미지를 특정 크기로 불러옴, 200=가로크기, 100=세로크기#
    # for i in range(1, 11): #10가지의 콤보 이미지 존재. 각 숫자에 해당하는 이미지 불러옴
    #     combos.append(pygame.image.load("assets/Combo/" + str(i) + "combo.png"))
    #     large_combos.append(pygame.transform.smoothscale(combos[i - 1], (150, 200))) #콤보이미지를 특정 크기로 불러옴, 150=가로크기, 200=세로크기#

    # combos_sound = []
    # for i in range(1, 10): #1-9까지 콤보사운드 존재. 각 숫자에 해당하는 음악 불러옴
    #     combos_sound.append(pygame.mixer.Sound("assets/sounds/SFX_" + str(i + 2) + "Combo.wav"))

    # Background colors
    black = (10, 10, 10)  # rgb(10, 10, 10)
    black_pause = (0, 0, 0, 127)
    real_white = (255, 255, 255)  # rgb(255, 255, 255)
    white = (211, 211, 211)  # rgb(211, 211, 211) ##연회색
    grey_1 = (26, 26, 26)  # rgb(26, 26, 26)
    grey_2 = (35, 35, 35)  # rgb(35, 35, 35)
    grey_3 = (55, 55, 55)  # rgb(55, 55, 55)
    pinkpurple = (250, 165, 255)  # rgb(250, 165, 255) 핑크+보라#

    # Tetrimino colors
    cyan = (69, 206, 204)  # rgb(69, 206, 204) # I
    blue = (64, 111, 249)  # rgb(64, 111, 249) # J
    orange = (253, 189, 53)  # rgb(253, 189, 53) # L
    yellow = (246, 227, 90)  # rgb(246, 227, 90) # O
    green = (98, 190, 68)  # rgb(98, 190, 68) # S
    pink = (242, 64, 235)  # rgb(242, 64, 235) # T
    red = (225, 13, 27)  # rgb(225, 13, 27) # Z

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


# 각 이미지 주소
background_image = 'assets/images/background_image.png'  # 메뉴화면(첫 화면) 배경
gamebackground_image = 'assets/images/background_nyc.png'  # 게임 배경화면 : 기본값 뉴욕
pause_board_image = 'assets/vector/pause_board.png'

help_board_image = 'assets/vector/help_board.png'
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

resume_button_image = 'assets/vector/resume_button.png'
clicked_resume_button_image = 'assets/vector/clicked_resume_button.png'

help_button_image = 'assets/vector/help_button.png'
clicked_help_button_image = 'assets/vector/clicked_help_button.png'

single_button_image = 'assets/vector/easy_button.png'
clicked_single_button_image = 'assets/vector/clicked_easy_button.png'

hard_button_image = 'assets/vector/hard_button.png'
clicked_hard_button_image = 'assets/vector/clicked_hard_button.png'

pvp_button_image = 'assets/vector/multi_button.png'
clicked_pvp_button_image = 'assets/vector/clicked_multi_button.png'


hard_training_button_image = 'assets/vector/hard_tutorial_button.png'
clicked_hard_training_button_image = 'assets/vector/clicked_hard_tutorial_button.png'

multi_training_button_image = 'assets/vector/multi_tutorial_button.png'
clicked_multi_training_button_image = 'assets/vector/clicked_multi_tutorial_button.png'


gameover_board_image = 'assets/vector/gameover_board.png'

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
'''
hard_training_start_image = 'assets/images/hard_tutorial_menual.png'
multi_training_start_image = 'assets/images/multi_tutorial_menual.png'
setting_board_image = 'assets/vector/setting_board.png'
number_board = 'assets/vector/number_board.png'
mute_button_image = 'assets/vector/allmute_button.png'
clicked_mute_button_image = 'assets/vector/clicked_allmute_button.png'

background1_image = 'assets/images/background_hongkong.png'
background2_image = 'assets/images/background_nyc.png'
background3_image = 'assets/images/background_uk.png'

clicked_background1_image = 'assets/images/clicked_background_hongkong.png'
clicked_background2_image = 'assets/images/clicked_background_nyc.png'
clicked_background3_image = 'assets/images/clicked_background_uk.png'

mute_button_image = 'assets/vector/allmute_button.png'
default_button_image = 'assets/vector/default_button.png'
clicked_default_button_image = 'assets/vector/clicked_default_button.png'
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

backgroundmusic_select_image = 'assets/vector/backgroundmusic_select.png'
clicked_backgroundmusic_select_image = 'assets/vector/clicked_backgroundmusic_select.png'
sound_off_button_image = 'assets/vector/sound_off_button.png'
sound_on_button_image = 'assets/vector/sound_on_button.png'
check_button_image = 'assets/vector/checkbox_button.png'
clicked_check_button_image = 'assets/vector/clicked_checkbox_button.png'

pvp_win_image = 'assets/vector/pvp_win.png'
pvp_lose_image = 'assets/vector/pvp_lose.png'
leaderboard_vector = 'assets/vector/leaderboard_vector.png'
clicked_leaderboard_vector = 'assets/vector/clicked_leaderboard_vector.png'
multi_win_image = 'assets/vector/multi_win.png'
multi_lose_image = 'assets/vector/multi_lose.png'
multi_game_over = 'assets/vector/multi_game_over.png'

leaderboard_vector = 'assets/vector/leaderboard_vector.png'
clicked_leaderboard_vector = 'assets/vector/clicked_leaderboard_vector.png'
scoreboard_board_image = 'assets/vector/score_board.png'

multi_gameover_image = 'assets/vector/multi_game_over.png'
multi_win_image = 'assets/vector/multi_win.png'
multi_lose_image = 'assets/vector/multi_lose.png'

multi_key_reverse_image = 'assets/vector/key_reverse.png'
hard_speed_up_image = 'assets/vector/speed_up.png'
hard_flipped_image = 'assets/vector/flipped.png'

multi_1P_break_image = 'assets/images/multi_1p_break.png'
multi_2P_break_image = 'assets/images/multi_2p_break.png'
training_box_image = 'assets/vector/box.png'

line_message_multi_break_image = 'assets/vector/line_message_multi_tutorial_break.png'
line_message_multi_win_image = 'assets/vector/line_message_multi_tutorial_win.png'

training_completed_image = 'assets/images/training_completed.png'
training_incomplete_image = 'assets/images/training_incomplete.png'

# 트레이닝모드 중간 이벤트 발생 시 나오는 설명 이미지
hard_3line_image = 'assets/images/hard_3line.png'  # 하드트레이닝 3줄 제거시 등장
hard_10s_image = 'assets/images/hard_10s.png'  # 하드트레이닝 10초 경과시 등장
hard_line_message = 'assets/vector/line_message_hard_tutorial.png'  # 하드트레이닝 시작하자마자 메시지 등장


class button():  # 버튼객체
    def __init__(self, board_width, board_height, x_rate, y_rate, width_rate, height_rate, img=''):  # 버튼생성
        self.x = board_width * x_rate  # 버튼 x좌표 (버튼이미지의 정중앙)
        self.y = board_height * y_rate  # 버튼 y좌표 (버튼이미지의 정중앙)
        self.width = int(board_width * width_rate)  # 버튼 너비
        self.height = int(board_height * height_rate)  # 버튼 높이
        self.x_rate = x_rate  # board_width * x_rate = x좌표
        self.y_rate = y_rate  # board_height * y_rate = y좌표
        self.width_rate = width_rate  # board_width * width_rate = 버튼 너비
        self.height_rate = height_rate  # board_height * height_rate = 버튼 높이
        self.image = img  # 불러올 버튼 이미지

    def change(self, board_width, board_height):  # 버튼 위치, 크기 바꾸기
        self.x = board_width * self.x_rate  # x좌표
        self.y = board_height * self.y_rate  # y좌표
        self.width = int(board_width * self.width_rate)  # 너비
        self.height = int(board_height * self.height_rate)  # 높이

    def draw(self, win, outline=None):  # 버튼 보이게 만들기

        if outline:
            draw_image(screen, self.image, self.x,
                       self.y, self.width, self.height)

    # 마우스의 위치가 버튼이미지 위에 있는지 확인  (pos[0]은 마우스 x좌표, pos[1]은 마우스 y좌표)
    def isOver(self, pos):

        if pos[0] > self.x - (self.width / 2) and pos[0] < self.x + (self.width / 2):
            if pos[1] > self.y - (self.height / 2) and pos[1] < self.y + (self.height / 2):
                return True
        return False

    def isOver_2(self, pos):  # start 화면에서 single,pvp,help,setting을 위해서 y좌표 좁게 인식하도록

        if pos[0] > self.x - (self.width / 2) and pos[0] < self.x + (self.width / 2):
            # 243줄에서의 2을 4로 바꿔주면서 좁게 인식할수 있도록함. 더 좁게 인식하고 싶으면 숫자 늘려주기#
            if pos[1] > self.y - (self.height / 4) and pos[1] < self.y + (self.height / 4):
                return True
        return False
# 메뉴 버튼


select_mode_button = button(
    board_width, board_height, 0.2, 0.2, 0.22, 0.2, select_mode_button_image)
setting_button = button(board_width, board_height, 0.2,
                        0.8, 0.22, 0.2, setting_button_image)

quit_button = button(board_width, board_height, 0.8,
                     0.8, 0.22, 0.2, quit_button_image)
score_board_button = button(
    board_width, board_height, 0.8, 0.2, 0.22, 0.2, score_board_button_image)

single_button = button(board_width, board_height, 0.25,
                       0.35, 0.22, 0.2, single_button_image)
hard_button = button(board_width, board_height, 0.5,
                     0.35, 0.22, 0.2, hard_button_image)
pvp_button = button(board_width, board_height, 0.75,
                    0.35, 0.22, 0.2, pvp_button_image)
hard_training_button = button(
    board_width, board_height, 0.37, 0.65, 0.22, 0.2, hard_training_button_image)
multi_training_button = button(
    board_width, board_height, 0.63, 0.65, 0.22, 0.2, multi_training_button_image)
resume_button = button(board_width, board_height, 0.5,
                       0.23, 0.17, 0.2, resume_button_image)
menu_button2 = button(board_width, board_height, 0.5,
                      0.43, 0.17, 0.2, menu_button_image)
help_button = button(board_width, board_height, 0.5,
                     0.63, 0.17, 0.2, help_button_image)
training_help_button = button(board_width, board_height, 0.68,
                     0.6, 0.17, 0.2, help_button_image)

pause_quit_button = button(board_width, board_height,
                           0.5, 0.83, 0.17, 0.2, quit_button_image)
pause_setting_button = button(
    board_width, board_height, 0.5, 0.63, 0.17, 0.2, pause_setting_button_image)

leaderboard_icon = button(board_width, board_height,
                          0.77, 0.85, 0.15, 0.2, leaderboard_vector)
mute_button = button(board_width, board_height, 0.5,
                     0.20, 0.15, 0.2, mute_button_image)
default_button = button(board_width, board_height, 0.5,
                        0.27, 0.15, 0.2, default_button_image)


restart_button = button(board_width, board_height, 0.5,
                        0.23, 0.17, 0.2, restart_button_image)
back_button = button(board_width, board_height, 0.5,
                     0.85, 0.1, 0.12, back_button_image)
back_button2 = button(board_width, board_height, 0.2,
                      0.85, 0.1, 0.12, back_button_image)
ok_button = button(board_width, board_height, 0.5,
                   0.83, 0.15, 0.2, ok_button_image)

# 멀티모드 게임오버화면 버튼
multi_menu_button = button(board_width, board_height,
                           0.35, 0.8, 0.2, 0.2, menu_button_image)
multi_restart_button = button(
    board_width, board_height, 0.65, 0.8, 0.2, 0.2, restart_button_image)
# 트레이닝 게임오버 화면 버튼
training_restart_button = button(
    board_width, board_height, 0.35, 0.8, 0.2, 0.2, restart_button_image)
training_multi_start_button = button(
    board_width, board_height, 0.65, 0.8, 0.2, 0.2, pvp_button_image)
training_hard_start_button = button(
    board_width, board_height, 0.65, 0.8, 0.2, 0.2, hard_button_image)


effect_plus_button = button(
    board_width, board_height, 0.27, 0.73, 0.0625, 0.1111, plus_button_image)
effect_minus_button = button(
    board_width, board_height, 0.42, 0.73, 0.0625, 0.1111, minus_button_image)

sound_plus_button = button(board_width, board_height,
                           0.27, 0.53, 0.0625, 0.1111, plus_button_image)
sound_minus_button = button(
    board_width, board_height, 0.42, 0.53, 0.0625, 0.1111, minus_button_image)


mute_check_button = button(board_width, board_height,
                           0.2, 0.4, 0.0625, 0.1111, check_button_image)

background1_check_button = button(
    board_width, board_height, 0.5, 0.25, 0.1875, 0.1444, background1_image)  # hongkong
background2_check_button = button(
    board_width, board_height, 0.5, 0.45, 0.1875, 0.1444, clicked_background2_image)  # nyc (default background)
background3_check_button = button(
    board_width, board_height, 0.5, 0.65, 0.1875, 0.1444, background3_image)  # uk

volume_icon = button(board_width, board_height, 0.4,
                     0.5, 0.12, 0.23, volume_vector)
screen_icon = button(board_width, board_height, 0.6,
                     0.5, 0.12, 0.23, screen_vector)


#음소거 추가#
effect_sound_off_button = button(
    board_width, board_height, 0.55, 0.73, 0.08, 0.15, sound_off_button_image)
music_sound_off_button = button(
    board_width, board_height, 0.55, 0.53, 0.08, 0.15, sound_off_button_image)
effect_sound_on_button = button(
    board_width, board_height, 0.55, 0.73, 0.08, 0.15, sound_on_button_image)
music_sound_on_button = button(
    board_width, board_height, 0.55, 0.53, 0.08, 0.15, sound_on_button_image)

#BGM 선택 추가#
BGM1_sound_on_button = button(
    board_width, board_height, 0.67, 0.43, 0.08, 0.15, clicked_backgroundmusic_select_image)  # default bgm: BGM1
BGM2_sound_on_button = button(
    board_width, board_height, 0.67, 0.63, 0.08, 0.15, backgroundmusic_select_image)
BGM3_sound_on_button = button(
    board_width, board_height, 0.67, 0.83, 0.08, 0.15, backgroundmusic_select_image)

# 선택된 BGM
selected_bgm = "assets/sounds/BGM1.wav"


# 게임 중 버튼 생성하기위한 버튼객체 리스트 (버튼 전체)
'''button_list = [mute_button, default_button, single_button, pvp_button, help_button, quit_button, gravity_button, timeattack_button, resume_button, restart_button, setting_button, pause_quit_button, back_button,
        ok_button, menu_button, gameover_quit_button, effect_plus_button, effect_minus_button, sound_plus_button, sound_minus_button, level_plus_button,
        effect_sound_off_button, music_sound_off_button, effect_sound_on_button, music_sound_on_button, mute_check_button, smallsize_check_button, midiumsize_check_button, bigsize_check_button,
        setting_icon, leaderboard_icon, volume_icon, screen_icon, level_minus_button, combo_minus_button, combo_plus_button, speed_minus_button, speed_plus_button]
'''

button_list = [
    select_mode_button, setting_button, quit_button, score_board_button, single_button, hard_button, pvp_button,
    hard_training_button, multi_training_button, resume_button, menu_button2, help_button, pause_quit_button, pause_setting_button,
    leaderboard_icon, mute_button, default_button, restart_button, back_button, ok_button, effect_plus_button, effect_minus_button,
    sound_plus_button, sound_minus_button, mute_check_button, background1_check_button, background2_check_button, background3_check_button,
    volume_icon, screen_icon, effect_sound_off_button, music_sound_off_button, effect_sound_on_button, music_sound_on_button,
    BGM1_sound_on_button, BGM2_sound_on_button, BGM3_sound_on_button, multi_restart_button, multi_menu_button, back_button2, training_restart_button, training_multi_start_button, training_hard_start_button]


def set_volume():
    # set_volume의 argument는 0.0~1.0으로 이루어져야하기 때문에 소수로 만들어주기 위해 10으로 나눔#
    ui_variables.fall_sound.set_volume(effect_volume / 10)
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
    x = x - (width / 2)  # 해당 이미지의 가운데 x좌표, 가운데 좌표이기 때문에 2로 나눔
    y = y - (height / 2)  # 해당 이미지의 가운데 y좌표, 가운데 좌표이기 때문에 2로 나눔
    image = pygame.image.load(img_path)
    image = pygame.transform.smoothscale(image, (width, height))
    window.blit(image, (x, y))

# Draw block


def draw_block(x, y, color):
    # 사각형 내부 색 color로 지정
    pygame.draw.rect(
        screen,
        color,
        Rect(x, y, block_size, block_size)
    )
    # 사각형 테두리
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        Rect(x, y, block_size, block_size),
        1
    )


def draw_block_image(x, y, image):
    # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
    draw_image(screen, image, x, y, block_size, block_size)

# Draw game screen


def draw_board(next1, next2, hold, score, level, goal):
    # 크기 비율 고정, 전체 board 가로길이에서 원하는 비율을 곱해줌
    sidebar_width = int(board_width * 0.5312)
    # screen.fill(ui_variables.grey_1)

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        Rect(sidebar_width, 0, int(board_width * 0.2375), board_height)  # 크기 비율 고정
    )

    # Draw 2 next minos
    grid_n1 = tetrimino.mino_map[next1 - 1][0]
    grid_n2 = tetrimino.mino_map[next2 - 1][0]

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            dx1 = int(board_width * 0.025) + sidebar_width + \
                block_size * j  # 위치 비율 고정, 전체 board 가로 길이에서 원하는 비율을 곱해줌
            dy1 = int(board_height * 0.3743) + block_size * \
                i  # 위치 비율 고정, 전체 board 세로 길이에서 원하는 비율을 곱해줌#
            if grid_n1[i][j] != 0:
                draw_block_image(dx1, dy1, ui_variables.t_block[grid_n1[i][j]])

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            dx2 = int(board_width * 0.145) + sidebar_width + \
                block_size * j  # 위치 비율 고정, 전체 board 가로길이에서 원하는 비율을 곱해줌#
            dy2 = int(board_height * 0.3743) + block_size * \
                i  # 위치 비율 고정, 전체 board 세로길이에서 원하는 비율을 곱해줌#
            if grid_n2[i][j] != 0:
                draw_block_image(dx2, dy2, ui_variables.t_block[grid_n2[i][j]])

    ''''# Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for i in range(4):
            for j in range(4):
                dx = 220 + block_size * j
                dy = 50 + block_size * i
                if grid_h[i][j] != 0:
                    draw_block_image(
                        dx, dy, ui_variables.t_block[grid_h[i][j]])'''  # hold 블록 출력
    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]  # (배열이라-1) 기본 모양
    if hold_mino != -1:  # hold 존재X
        for i in range(mino_matrix_y):
            for j in range(mino_matrix_x):
                dx = int(board_width * 0.045) + sidebar_width + \
                    block_size * j  # 위치 비율 고정
                dy = int(board_height * 0.1336) + block_size * i  # 위치 비율 고정
                if grid_h[i][j] != 0:  # 해당 부분에 블록이 존재하면
                    draw_block_image(
                        dx, dy, ui_variables.t_block[grid_h[i][j]])  # hold 블록 출력

    # Set max score
    if score > 999999:
        score = 999999

    # Draw texts
    text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.real_white)
    text_next = ui_variables.h5.render("NEXT", 1, ui_variables.real_white)
    text_score = ui_variables.h5.render("SCORE", 1, ui_variables.real_white)
    score_value = ui_variables.h4.render(
        str(score), 1, ui_variables.real_white)
    text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.real_white)
    level_value = ui_variables.h4.render(
        str(level), 1, ui_variables.real_white)
    text_goal = ui_variables.h5.render("GOAL", 1, ui_variables.real_white)
    goal_value = ui_variables.h4.render(str(goal), 1, ui_variables.real_white)

    # Place texts
    screen.blit(text_hold, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.0374)))
    screen.blit(text_next, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.2780)))
    screen.blit(text_score, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.5187)))
    screen.blit(score_value, (int(board_width * 0.055) +
                sidebar_width, int(board_height * 0.5614)))
    screen.blit(text_level, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.6791)))
    screen.blit(level_value, (int(board_width * 0.055) +
                sidebar_width, int(board_height * 0.7219)))
    screen.blit(text_goal, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.8400)))
    screen.blit(goal_value, (int(board_width * 0.055) +
                sidebar_width, int(board_height * 0.8823)))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(board_width * 0.25) + block_size * \
                x  # 위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#
            dy = int(board_height * 0.055) + block_size * \
                y  # 위치비율 고정, board 세로길이에 원하는 비율을 곱해줌#
            draw_block_image(dx, dy, ui_variables.t_block[matrix[x][y + 1]])

# hard mode draw board


def draw_hardboard(next1, next2, hold, score, remaining_time, line):
  # 크기 비율 고정, 전체 board 가로길이에서 원하는 비율을 곱해줌
    sidebar_width = int(board_width * 0.5312)

    # screen.fill(ui_variables.grey_1)

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        Rect(sidebar_width, 0, int(board_width * 0.2375), board_height)  # 크기 비율 고정
    )

    # Draw 2 next minos
    grid_n1 = tetrimino.mino_map[next1 - 1][0]
    grid_n2 = tetrimino.mino_map[next2 - 1][0]

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            dx1 = int(board_width * 0.025) + sidebar_width + \
                block_size * j  # 위치 비율 고정, 전체 board 가로 길이에서 원하는 비율을 곱해줌
            dy1 = int(board_height * 0.3743) + block_size * \
                i  # 위치 비율 고정, 전체 board 세로 길이에서 원하는 비율을 곱해줌#
            if grid_n1[i][j] != 0:
                draw_block_image(dx1, dy1, ui_variables.t_block[grid_n1[i][j]])

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            dx2 = int(board_width * 0.145) + sidebar_width + \
                block_size * j  # 위치 비율 고정, 전체 board 가로길이에서 원하는 비율을 곱해줌#
            dy2 = int(board_height * 0.3743) + block_size * \
                i  # 위치 비율 고정, 전체 board 세로길이에서 원하는 비율을 곱해줌#
            if grid_n2[i][j] != 0:
                draw_block_image(dx2, dy2, ui_variables.t_block[grid_n2[i][j]])

    '''# Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for i in range(4):
            for j in range(4):
                dx = 220 + block_size * j
                dy = 50 + block_size * i
                if grid_h[i][j] != 0:
                    draw_block_image(
                        dx, dy, ui_variables.t_block[grid_h[i][j]])  # hold 블록 출력'''
    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]  # (배열이라-1) 기본 모양

    if hold_mino != -1:  # hold 존재X
        for i in range(mino_matrix_y):
            for j in range(mino_matrix_x):
                dx = int(board_width * 0.045) + sidebar_width + \
                    block_size * j  # 위치 비율 고정
                dy = int(board_height * 0.1336) + block_size * i  # 위치 비율 고정
                if grid_h[i][j] != 0:  # 해당 부분에 블록이 존재하면
                    draw_block_image(
                        dx, dy, ui_variables.t_block[grid_h[i][j]])  # hold 블록 출력

    # Set max score
    if score > 999999:
        score = 999999

    # Draw texts
    text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.real_white)
    text_next = ui_variables.h5.render("NEXT", 1, ui_variables.real_white)
    text_score = ui_variables.h5.render("SCORE", 1, ui_variables.real_white)
    score_value = ui_variables.h4.render(
        str(score), 1, ui_variables.real_white)
    text_remaining_time = ui_variables.h5.render(
        "TIME", 1, ui_variables.real_white)
    time_value = ui_variables.h4.render(
        str(remaining_time), 1, ui_variables.real_white)
    text_line = ui_variables.h5.render("LINE", 1, ui_variables.real_white)
    line_value = ui_variables.h4.render(
        str(line_count), 1, ui_variables.real_white)

    # Place texts
    screen.blit(text_hold, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.0374)))
    screen.blit(text_next, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.2780)))
    screen.blit(text_score, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.5187)))
    screen.blit(score_value, (int(board_width * 0.055) +
                sidebar_width, int(board_height * 0.5614)))
    screen.blit(text_remaining_time, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.6791)))
    screen.blit(time_value, (int(board_width * 0.055) +
                sidebar_width, int(board_height * 0.7219)))
    screen.blit(text_line, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.8395)))
    screen.blit(line_value, (int(board_width * 0.055) +
                sidebar_width, int(board_height * 0.8823)))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(board_width * 0.25) + block_size * \
                x  # 위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#
            dy = int(board_height * 0.055) + block_size * \
                y  # 위치비율 고정, board 세로길이에 원하는 비율을 곱해줌#
            draw_block_image(dx, dy, ui_variables.t_block[matrix[x][y + 1]])
            # draw_block_image(dx, dy, ui_variables.t_block[matrix[x][(height-1)-y+1]])

# hard mode draw board change


def draw_hardboard_change(next1, next2, hold, score, remaining_time, line):
  # 크기 비율 고정, 전체 board 가로길이에서 원하는 비율을 곱해줌
    sidebar_width = int(board_width * 0.5312)

    # screen.fill(ui_variables.grey_1)

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        Rect(sidebar_width, 0, int(board_width * 0.2375), board_height)  # 크기 비율 고정
    )

    # Draw 2 next minos
    grid_n1 = tetrimino.mino_map[next1 - 1][0]
    grid_n2 = tetrimino.mino_map[next2 - 1][0]

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            dx1 = int(board_width * 0.025) + sidebar_width + \
                block_size * j  # 위치 비율 고정, 전체 board 가로 길이에서 원하는 비율을 곱해줌
            dy1 = int(board_height * 0.3743) + block_size * \
                i  # 위치 비율 고정, 전체 board 세로 길이에서 원하는 비율을 곱해줌#
            if grid_n1[i][j] != 0:
                draw_block_image(dx1, dy1, ui_variables.t_block[grid_n1[i][j]])

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            dx2 = int(board_width * 0.145) + sidebar_width + \
                block_size * j  # 위치 비율 고정, 전체 board 가로길이에서 원하는 비율을 곱해줌#
            dy2 = int(board_height * 0.3743) + block_size * \
                i  # 위치 비율 고정, 전체 board 세로길이에서 원하는 비율을 곱해줌#
            if grid_n2[i][j] != 0:
                draw_block_image(dx2, dy2, ui_variables.t_block[grid_n2[i][j]])

    '''# Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for i in range(4):
            for j in range(4):
                dx = 220 + block_size * j
                dy = 50 + block_size * i
                if grid_h[i][j] != 0:
                    draw_block_image(
                        dx, dy, ui_variables.t_block[grid_h[i][j]])  # hold 블록 출력'''
    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]  # (배열이라-1) 기본 모양

    if hold_mino != -1:  # hold 존재X
        for i in range(mino_matrix_y):
            for j in range(mino_matrix_x):
                dx = int(board_width * 0.045) + sidebar_width + \
                    block_size * j  # 위치 비율 고정
                dy = int(board_height * 0.1336) + block_size * i  # 위치 비율 고정
                if grid_h[i][j] != 0:  # 해당 부분에 블록이 존재하면
                    draw_block_image(
                        dx, dy, ui_variables.t_block[grid_h[i][j]])  # hold 블록 출력

    # Set max score
    if score > 999999:
        score = 999999

    # Draw texts
    text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.real_white)
    text_next = ui_variables.h5.render("NEXT", 1, ui_variables.real_white)
    text_score = ui_variables.h5.render("SCORE", 1, ui_variables.real_white)
    score_value = ui_variables.h4.render(
        str(score), 1, ui_variables.real_white)
    text_remaining_time = ui_variables.h5.render(
        "TIME", 1, ui_variables.real_white)
    time_value = ui_variables.h4.render(
        str(remaining_time), 1, ui_variables.real_white)
    text_line = ui_variables.h5.render("LINE", 1, ui_variables.real_white)
    line_value = ui_variables.h4.render(
        str(line_count), 1, ui_variables.real_white)

    # Place texts
    screen.blit(text_hold, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.0374)))
    screen.blit(text_next, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.2780)))
    screen.blit(text_score, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.5187)))
    screen.blit(score_value, (int(board_width * 0.055) +
                sidebar_width, int(board_height * 0.5614)))
    screen.blit(text_remaining_time, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.6791)))
    screen.blit(time_value, (int(board_width * 0.055) +
                sidebar_width, int(board_height * 0.7219)))
    screen.blit(text_line, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.8395)))
    screen.blit(line_value, (int(board_width * 0.055) +
                sidebar_width, int(board_height * 0.8823)))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(board_width * 0.25) + block_size * \
                x  # 위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#
            dy = int(board_height * 0.055) + block_size * \
                y  # 위치비율 고정, board 세로길이에 원하는 비율을 곱해줌#
            # draw_block_image(dx, dy, ui_variables.t_block[matrix[x][y + 1]])
            draw_block_image(
                dx, dy, ui_variables.t_block[matrix[x][(height-1)-y+1]])


def draw_1Pboard(next, hold, current_key):
    # 위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#
    sidebar_width = int(board_width * 0.31)

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        Rect(sidebar_width, 0, int(board_width * 0.1875),
             board_height)  # 크기비율 고정, board 가로길이에 원하는 비율을 곱해줌#
    )

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]  # (배열이라-1) 다음 블록의 원래 모양

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            dx = int(board_width * 0.045) + sidebar_width + \
                block_size * j  # 위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#
            dy = int(board_height * 0.3743) + block_size * \
                i  # 위치비율 고정, board 세로길이에 원하는 비율을 곱해줌#
            if grid_n[i][j] != 0:
                draw_block_image(dx, dy, ui_variables.t_block[grid_n[i][j]])

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]  # (배열이라-1) 기본 모양

    if hold_mino != -1:  # 기본값이 -1. 즉 hold블록 존재할 떄
        for i in range(mino_matrix_y):
            for j in range(mino_matrix_x):
                dx = int(board_width * 0.045) + sidebar_width + \
                    block_size * j  # 위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#
                dy = int(board_height * 0.1336) + block_size * \
                    i  # 위치비율 고정, board 세로길이에 원하는 비율을 곱해줌#
                if grid_h[i][j] != 0:
                    draw_block_image(
                        dx, dy, ui_variables.t_block[grid_h[i][j]])  # hold 블록 그림

    # Draw texts
    # render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
    if textsize == False:
        text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h5.render("NEXT", 1, ui_variables.real_white)
        # text_score = ui_variables.h5.render(
        #     "SCORE", 1, ui_variables.real_white)
        # score_value = ui_variables.h4.render(
        #     str(score), 1, ui_variables.real_white)
        # text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.real_white)
        # level_value = ui_variables.h4.render(str(level), 1, ui_variables.real_white)
        text_reverse = ui_variables.h5.render(
            "REVERSE", 1, ui_variables.real_white)
        if current_key:
            reverse_value = ui_variables.h4.render(
                "O", 1, ui_variables.real_white)
        elif not current_key:
            reverse_value = ui_variables.h4.render(
                "X", 1, ui_variables.real_white)
        text_combo = ui_variables.h5.render("GOAL", 1, ui_variables.real_white)
        combo_value = ui_variables.h4.render(
            str(5 - combo_count), 1, ui_variables.real_white)
    if textsize == True:
        text_hold = ui_variables.h3.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h3.render("NEXT", 1, ui_variables.real_white)
        # text_score = ui_variables.h3.render(
        #     "SCORE", 1, ui_variables.real_white)
        # score_value = ui_variables.h2.render(
        #     str(score), 1, ui_variables.real_white)
        # text_level = ui_variables.h3.render("LEVEL", 1, ui_variables.real_white)
        # level_value = ui_variables.h2.render(str(level), 1, ui_variables.real_white)
        text_reverse = ui_variables.h3.render(
            "REVERSE", 1, ui_variables.real_white)
        if current_key:
            reverse_value = ui_variables.h2.render(
                "O", 1, ui_variables.real_white)
        elif not current_key:
            reverse_value = ui_variables.h2.render(
                "X", 1, ui_variables.real_white)
        text_combo = ui_variables.h3.render("GOAL", 1, ui_variables.real_white)
        combo_value = ui_variables.h2.render(
            str(5 - combo_count), 1, ui_variables.real_white)
    if debug:
        # speed를 알려주는 framerate(기본값 30. 빨라질 수록 숫자 작아짐)
        speed_value = ui_variables.h5.render(
            "SPEED : "+str(framerate), 1, ui_variables.real_white)
        screen.blit(speed_value, (int(board_width * 0.045) + sidebar_width,
                    int(board_height * 0.015)))  # 각각 전체 board 가로길이, 세로길이에 원하는 비율을 곱해줌
    screen.blit(text_hold, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.0374)))
    screen.blit(text_next, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.2780)))
    # screen.blit(text_score, (int(board_width * 0.045) +
    #             sidebar_width, int(board_height * 0.5187)))
    # screen.blit(score_value, (int(board_width * 0.055) +
    #             sidebar_width, int(board_height * 0.5614)))
    screen.blit(text_reverse, (int(board_width*0.045) +
                sidebar_width, int(board_height*0.6791)))
    screen.blit(reverse_value, (int(board_width*0.055) +
                sidebar_width, int(board_height*0.7219)))
    screen.blit(text_combo, (int(board_width*0.045) +
                sidebar_width, int(board_height*0.8395)))
    screen.blit(combo_value, (int(board_width*0.055) +
                sidebar_width, int(board_height*0.8823)))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(board_width * 0.05) + block_size * \
                x  # 위치 비율 고정, board의 가로길이에 원하는 비율을 곱해줌
            dy = int(board_height * 0.055) + block_size * \
                y  # 위치 비율 고정, board의 세로길이에 원하는 비율을 곱해줌
            draw_block_image(dx, dy, ui_variables.t_block[matrix[x][y + 1]])


def draw_2Pboard(next, hold, current_key_2P):
    # 위치 비율 고정, , board의 가로길이에 원하는 비율을 곱해줌
    sidebar_width = int(board_width * 0.82)

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        # 크기 비율 고정, , board의 가로길이에 원하는 비율을 곱해줌, Rect(x축, y축, 가로길이, 세로길이)#
        Rect(sidebar_width, 0, int(board_width * 0.1875), board_height)
    )

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]

    for i in range(mino_matrix_y):  # 16개의 그리드 칸에서 true인 값만 뽑아서 draw.rect
        for j in range(mino_matrix_x):
            dx = int(board_width * 0.05) + sidebar_width + \
                block_size * j  # 위치 비율 고정, board의 가로길이에 원하는 비율을 곱해줌
            dy = int(board_height * 0.3743) + block_size * \
                i  # 위치 비율 고정, board의 세로길이에 원하는 비율을 곱해줌
            if grid_n[i][j] != 0:
                draw_block_image(dx, dy, ui_variables.t_block[grid_n[i][j]])

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino_2P != -1:  # 기본값이 -1. 즉 hold블록 존재할 떄
        for i in range(mino_matrix_y):
            for j in range(mino_matrix_x):
                dx = int(board_width * 0.045) + sidebar_width + \
                    block_size * j  # 위치 비율 고정, board의 가로길이에 원하는 비율을 곱해줌
                dy = int(board_height * 0.1336) + block_size * \
                    i  # 위치 비율 고정, board의 세로길이에 원하는 비율을 곱해줌
                if grid_h[i][j] != 0:
                    draw_block_image(
                        dx, dy, ui_variables.t_block[grid_h[i][j]])

    # render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래 코드의 숫자 1=안티에일리어싱 적용에 대한 코드
    if textsize == False:
        text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h5.render("NEXT", 1, ui_variables.real_white)
        # text_score = ui_variables.h5.render(
        #     "SCORE", 1, ui_variables.real_white)
        # score_value = ui_variables.h4.render(
        #     str(score_2P), 1, ui_variables.real_white)
        # text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.real_white)
        # level_value = ui_variables.h4.render(str(level), 1, ui_variables.real_white)
        text_reverse = ui_variables.h5.render(
            "REVERSE", 1, ui_variables.real_white)
        if current_key_2P:
            reverse_value = ui_variables.h4.render(
                "O", 1, ui_variables.real_white)
        elif not current_key_2P:
            reverse_value = ui_variables.h4.render(
                "X", 1, ui_variables.real_white)
        text_combo = ui_variables.h5.render("GOAL", 1, ui_variables.real_white)
        combo_value = ui_variables.h4.render(
            str(5 - combo_count_2P), 1, ui_variables.real_white)
    if textsize == True:
        text_hold = ui_variables.h4.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h4.render("NEXT", 1, ui_variables.real_white)
        # text_score = ui_variables.h4.render(
        #     "SCORE", 1, ui_variables.real_white)
        # score_value = ui_variables.h3.render(
        #     str(score_2P), 1, ui_variables.real_white)
        # text_level = ui_variables.h4.render("LEVEL", 1, ui_variables.real_white)
        # level_value = ui_variables.h3.render(str(level), 1, ui_variables.real_white)
        text_reverse = ui_variables.h4.render(
            "REVERSE", 1, ui_variables.real_white)
        if current_key_2P:
            reverse_value = ui_variables.h3.render(
                "O", 1, ui_variables.real_white)
        elif not current_key_2P:
            reverse_value = ui_variables.h3.render(
                "X", 1, ui_variables.real_white)
        text_combo = ui_variables.h4.render("GOAL", 1, ui_variables.real_white)
        combo_value = ui_variables.h3.render(
            str(5 - combo_count_2P), 1, ui_variables.real_white)
    if debug:
        # speed를 알려주는 framerate(기본값 30. 빨라질 수록 숫자 작아짐)
        speed_value = ui_variables.h5.render(
            "SPEED : "+str(framerate_2P), 1, ui_variables.real_white)
        screen.blit(speed_value, (int(board_width * 0.045) + sidebar_width,
                    int(board_height * 0.015)))  # 각각 전체 board의 가로길이, 세로길이에 대해 원하는 비율을 곱해줌
    screen.blit(text_hold, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.0374)))
    screen.blit(text_next, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.2780)))
    # screen.blit(text_score, (int(board_width * 0.045) +
    #             sidebar_width, int(board_height * 0.5187)))
    # screen.blit(score_value, (int(board_width * 0.055) +
    #             sidebar_width, int(board_height * 0.5614)))
    screen.blit(text_reverse, (int(board_width*0.045) +
                sidebar_width, int(board_height*0.6791)))
    screen.blit(reverse_value, (int(board_width*0.055) +
                sidebar_width, int(board_height*0.7219)))
    screen.blit(text_combo, (int(board_width*0.045) +
                sidebar_width, int(board_height*0.8395)))
    screen.blit(combo_value, (int(board_width*0.055) +
                sidebar_width, int(board_height*0.8823)))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(board_width * 0.54) + block_size * x  # 위치비율 고정
            dy = int(board_height * 0.055) + block_size * y  # 위치비율 고정
            draw_block_image(dx, dy, ui_variables.t_block[matrix_2P[x][y + 1]])


def draw_multiboard(next_1P, hold_1P, next_2P, hold_2P, current_key, current_key_2P):
    screen.fill(ui_variables.real_white)
    draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
               0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
    draw_1Pboard(next_1P, hold_1P, current_key)
    draw_2Pboard(next_2P, hold_2P, current_key_2P)


# Draw a tetrimino
def draw_mino(x, y, mino, r, matrix):  # mino는 모양, r은 회전된 모양 중 하나
    grid = tetrimino.mino_map[mino - 1][r]  # grid : 출력할 테트리스

    tx, ty = x, y
    # 테트리스가 바닥에 존재하면 true -> not이니까 바닥에 없는 상태
    while not is_bottom(tx, ty, mino, r, matrix):
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
                # 그 블록위치에 0, 8 아님(즉 블록 존재 함)
                elif matrix[x + j][y + i + 1] != 0 and matrix[x + j][y + i + 1] != 8:
                    return True

    return False


# Returns true if mino is at the left edge
def is_leftedge(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - 1][r]  # grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j - 1) < 0:  # 맨 왼쪽에 위치함
                    return True
                elif matrix[x + j - 1][y + i] != 0:  # 그 위치의 왼쪽에 이미 무엇인가 존재함
                    return True

    return False

# Returns true if mino is at the right edge


def is_rightedge(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - 1][r]  # grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j + 1) >= board_x:  # 맨 오른쪽에 위치
                    return True
                elif matrix[x + j + 1][y + i] != 0:  # 그 위치의 오른쪽에 이미 무엇인가 존재함
                    return True

    return False


def is_turnable_r(x, y, mino, r, matrix):
    if r != 3:  # 회전모양 총 0, 1, 2, 3번째 총 4가지 있음
        grid = tetrimino.mino_map[mino - 1][r + 1]  # 3이 아니면 그 다음 모양
    else:
        grid = tetrimino.mino_map[mino - 1][0]  # 3이면 0번째 모양으로

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                # 테트리스 matrix크기 벗어나면 못돌림
                if (x + j) < 0 or (x + j) >= board_x or (y + i) < 0 or (y + i) > board_y:
                    return False
                elif matrix[x + j][y + i] != 0:  # 해당 자리에 이미 블록이 있으면 못돌림
                    return False
    return True

# Returns true if turning left is possible


def is_turnable_l(x, y, mino, r, matrix):
    if r != 0:  # 회전모양 총 0, 1, 2, 3번째 총 4가지 있음
        grid = tetrimino.mino_map[mino - 1][r - 1]  # 0이 아니면 그 다음 모양
    else:
        grid = tetrimino.mino_map[mino - 1][3]  # 0이면 3번째 모양으로

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                # 테트리스 matrix크기 벗어나면 못돌림
                if (x + j) < 0 or (x + j) >= board_x or (y + i) < 0 or (y + i) > board_y:
                    return False
                elif matrix[x + j][y + i] != 0:  # 해당 자리에 이미 블록이 있으면 못돌림
                    return False

    return True

# Returns true if new block is drawable


def is_stackable(mino, matrix):
    grid = tetrimino.mino_map[mino - 1][0]  # grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0 and matrix[3 + j][i] != 0:
                return False

    return True


'''
# Draw a tetrimino
def draw_mino(x, y, mino, r, matrix):  # mino는 모양, r은 회전된 모양 중 하나
    grid = tetrimino.mino_map[mino - 1][r]  # grid : 출력할 테트리스
    tx, ty = x, y
    # 테트리스가 바닥에 존재하면 true -> not이니까 바닥에 없는 상태
    while not is_bottom(tx, ty, mino, r, matrix):
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
                # 그 블록위치에 0, 8 아님(즉 블록 존재 함)
                elif matrix[x + j][y + i + 1] != 0 and matrix[x + j][y + i + 1] != 8:
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
                # 테트리스 matrix크기 벗어나면 못돌림
                if (x + j) < 0 or (x + j) >= board_x or (y + i) < 0 or (y + i) > board_y :
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
                # 테트리스 matrix크기 벗어나면 못돌림
                if (x + j) < 0 or (x + j) >= board_x or (y + i) < 0 or (y + i) > board_y:
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


def multi_reverse_key(rev, player):
    # 하드드롭-왼쪽회전, 소프트드롭-오른쪽회전, 오른쪽이동-왼쪽이동 방향키 전환
    keys_1P = {'hardDrop': K_e, 'softDrop': K_s, 'turnRight': K_w,
               'turnLeft': K_q, 'moveRight': K_d, 'moveLeft': K_a}
    keys_1P_reverse = {'hardDrop': K_q, 'softDrop': K_w, 'turnRight': K_s,
                       'turnLeft': K_e, 'moveRight': K_a, 'moveLeft': K_d}
    keys_2P = {'hardDrop': K_SPACE, 'softDrop': K_DOWN, 'turnRight': K_UP,
               'turnLeft': K_m, 'moveRight': K_RIGHT, 'moveLeft': K_LEFT}
    keys_2P_reverse = {'hardDrop': K_m, 'softDrop': K_UP, 'turnRight': K_DOWN,
                       'turnLeft': K_SPACE, 'moveRight': K_LEFT, 'moveLeft': K_RIGHT}

    if rev == False:
        if player == 1:
            return keys_1P
        elif player == 2:
            return keys_2P
    elif rev == True:
        if player == 1:
            return keys_1P_reverse
        elif player == 2:
            return keys_2P_reverse


def set_initial_values():
    global training_event_happened, pause_training, training_event, combo_count, combo_count_2P, line_count, score, level, goal, score_2P, level_2P, goal_2P, bottom_count, bottom_count_2P, hard_drop, hard_drop_2P, attack_point, attack_point_2P, dx, dy, dx_2P, dy_2P, rotation, rotation_2P, mino, mino_2P, next_mino1, next_mino2, next_mino1_2P, hold, hold_2P, hold_mino, hold_mino_2P, framerate, framerate_2P, matrix, matrix_2P, Change_RATE, blink, start, pause, done, game_over, leader_board, setting, volume_setting, screen_setting, pvp, help, gravity_mode, debug, d, e, b, u, g, start_ticks, textsize, CHANNELS, swidth, name_location, name, previous_time, current_time, pause_time, lines, leaders, leaders_hard, game_status, framerate_blockmove, framerate_2P_blockmove, game_speed, game_speed_2P, select_mode, hard, hard_training, multi_training, training_status, hard_time_setting, winner, key1, key2, key_reverse, key_reverse_2P, current_key, current_key_2P, hard_training_info, multi_training_info, game_over_training, help_status, remaining_time

    framerate = 30  # Bigger -> Slower  기본 블록 하강 속도, 2도 할만 함, 0 또는 음수 이상이어야 함
    framerate_blockmove = framerate * 3  # 블록 이동 시 속도
    game_speed = framerate * 20  # 게임 기본 속도
    framerate_2P = 30  # 2P
    framerate_2P_blockmove = framerate_2P * 3  # 블록 이동 시 속도
    game_speed_2P = framerate_2P * 20  # 2P 게임 기본 속도

    help_status = False
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
    hard = False  # 하드모드 변수 추가
    hard_training = False  # 하드 트레이닝 변수 추가
    hard_training_info = False  # 하드 트레이닝 설명 화면

    multi_training = False  # 멀티 트레이닝 변수 추가
    multi_training_info = False  # 하드 트레이닝 설명 화면

    training_status = False  # 여러 기능 설명 창 띄우기
    pause_training = False  # 트레이닝의 pause 변수 추가
    game_over_training = False  # 트레이닝 모드 게임오버 화면

    help = False
    select_mode = False
    gravity_mode = False  # 이 코드가 없으면 중력모드 게임을 했다가 Restart해서 일반모드로 갈때 중력모드로 게임이 진행됨#
    debug = False
    d = False
    e = False
    b = False
    u = False
    g = False
    hard_time_setting = False  # 하드모드 시작하였을 때 타임 세팅을 시작하여 경과 시간을 계산하기 위해 추가한 변수
    remaining_time = 60  # 하드모드 남은 시간
    winner = 0  # multi mode에서 1P가 이기면 1, 2P가 이기면 2 (기본값은 0)
    start_ticks = pygame.time.get_ticks()
    textsize = False
    # 트레이닝에서 발생한 이벤트 상태 저장용 변수 (hard_10sec, hard_3line, hard_full, multi_1P_break, multi_2P_break, multi_5break, multi_full, no_event)
    training_event = ''
    # 트레이닝에서 반복해서 발생하는 이벤트 발생 첫 회에서만 설명 띄울 수 있게, 발생 여부를 저장하는 딕셔너리
    training_event_happened = {'hard_3line': False, 'hard_10sec': False,
                               'multi_1P_break': False, 'multi_2P_break': False}

    # 게임 음악 속도 조절 관련 변수
    CHANNELS = 1
    swidth = 2
    Change_RATE = 2

    line_count = 0
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
    combo_count = 0
    combo_count_2P = 0
    key1 = {'hardDrop': K_e, 'softDrop': K_s, 'turnRight': K_w,
            'turnLeft': K_q, 'moveRight': K_d, 'moveLeft': K_a}
    key2 = {'hardDrop': K_SPACE, 'softDrop': K_DOWN, 'turnRight': K_UP,
            'turnLeft': K_m, 'moveRight': K_RIGHT, 'moveLeft': K_LEFT}
    key_reverse = False   # 상대가 몇 줄이든 줄(들)을 깼는지 체크 (조건 충족 체크)
    key_reverse_2P = False
    current_key = False    # 최근 키가 반전키였는지 정상키였는지 체크
    current_key_2P = False

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

    # easy mode 스코어보드 leaders 배열에 저장
    with open('leaderboard.txt') as f:
        lines = f.readlines()
    lines = [line.rstrip('\n') for line in open(
        'leaderboard.txt')]  # leaderboard.txt 한줄씩 읽어옴

    leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
    for i in lines:
        leaders[i.split(' ')[0]] = int(i.split(' ')[1])
    leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)

    # hard mode 스코어보드 leaders_hard 배열에 저장
    with open('leaderboard_hard.txt') as h:
        lines = h.readlines()
    lines = [line.rstrip('\n') for line in open(
        'leaderboard_hard.txt')]  # leaderboard.txt 한줄씩 읽어옴

    leaders_hard = {'AAA': 0, 'BBB': 0, 'CCC': 0}
    for i in lines:
        leaders_hard[i.split(' ')[0]] = int(i.split(' ')[1])
    leaders_hard = sorted(leaders_hard.items(),
                          key=operator.itemgetter(1), reverse=True)

    matrix = [[0 for y in range(height + 1)]
              for x in range(width)]  # Board matrix
    matrix_2P = [[0 for y in range(height + 1)]
                 for x in range(width)]  # Board matrix

    pygame.mixer.init()
    ui_variables.click_sound.set_volume(effect_volume / 10)
    ui_variables.intro_sound.set_volume(music_volume / 10)
    ui_variables.break_sound.set_volume(
        effect_volume / 10)  # 소리 설정 부분도 set_volume 함수에 넣으면 됨

    game_status = ''
    pygame.mixer.music.load(selected_bgm)


set_initial_values()
pygame.time.set_timer(pygame.USEREVENT, 10)


###########################################################
# Loop Start
###########################################################

while not done:
    # Pause screen
    if pause:
        pygame.mixer.music.pause()
        if start:
            screen.fill(ui_variables.real_white)
            draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                       0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
            draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
            # 화면 회색으로 약간 불투명하게
            pause_surface = screen.convert_alpha()  # 투명 가능하도록
            pause_surface.fill((0, 0, 0, 0))  # 투명한 검정색으로 덮기
            pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(
                board_width), int(board_height)])  # (screen, 색깔, 위치 x, y좌표, 너비, 높이)
            screen.blit(pause_surface, (0, 0))

        if hard:
            screen.fill(ui_variables.real_white)
            draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                       0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
            draw_hardboard(next_mino1, next_mino2, hold_mino,
                           score, remaining_time, line_count)

            # 화면 회색으로 약간 불투명하게
            pause_surface = screen.convert_alpha()  # 투명 가능하도록
            pause_surface.fill((0, 0, 0, 0))  # 투명한 검정색으로 덮기
            pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(
                board_width), int(board_height)])  # (screen, 색깔, 위치 x, y좌표, 너비, 높이)
            screen.blit(pause_surface, (0, 0))

        if pvp:
            draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                            hold_mino_2P, current_key, current_key_2P)
            # 화면 회색으로 약간 불투명하게
            pause_surface = screen.convert_alpha()  # 투명 가능하도록
            pause_surface.fill((0, 0, 0, 0))  # 투명한 검정색으로 덮기
            pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(
                board_width), int(board_height)])  # (screen, 색깔, 위치 x, y좌표, 너비, 높이)
            screen.blit(pause_surface, (0, 0))

        if hard_training:
            screen.fill(ui_variables.real_white)

            draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                       0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
            draw_hardboard(next_mino1, next_mino2, hold_mino,
                           score, remaining_time, line_count)

            # 화면 회색으로 약간 불투명하게
            pause_surface = screen.convert_alpha()  # 투명 가능하도록
            pause_surface.fill((0, 0, 0, 0))  # 투명한 검정색으로 덮기
            pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(
                board_width), int(board_height)])  # (screen, 색깔, 위치 x, y좌표, 너비, 높이)
            screen.blit(pause_surface, (0, 0))

        if multi_training:
            draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P,
                            current_key, current_key_2P)
            # 화면 회색으로 약간 불투명하게
            pause_surface = screen.convert_alpha()  # 투명 가능하도록
            pause_surface.fill((0, 0, 0, 0))  # 투명한 검정색으로 덮기
            pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(
                board_width), int(board_height)])  # (screen, 색깔, 위치 x, y좌표, 너비, 높이)
            screen.blit(pause_surface, (0, 0))

        if help_status == True:
            pause_surface = screen.convert_alpha()  # 투명 가능하도록
            pause_surface.fill((0, 0, 0, 0))  # 투명한 검정색으로 덮기
            pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(
                board_width), int(board_height)])  # (screen, 색깔, 위치 x, y좌표, 너비, 높이)

            draw_image(screen, help_board_image, board_width * 0.5, board_height * 0.5,
                       int(board_width * 0.8), int(board_height * 0.9))  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
            back_button2.draw(screen, (0, 0, 0))

        if help_status == False:
            draw_image(screen, pause_board_image, board_width * 0.5, board_height * 0.5,
                       int(board_height * 1), board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
            resume_button.draw(screen, (0, 0, 0))  # rgb(0,0,0) = 검정색

            menu_button2.draw(screen, (0, 0, 0))
            help_button.draw(screen, (0, 0, 0))
            pause_quit_button.draw(screen, (0, 0, 0))

        pygame.display.update()

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
                    pygame.mixer.music.unpause()
                    pause = False
                    ui_variables.click_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, 1)  # 0.001초

            elif event.type == pygame.MOUSEMOTION:
                if back_button2.isOver(pos):
                    back_button2.image = clicked_back_button_image
                else:
                    back_button2.image = back_button_image
                pygame.display.update()
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

                if pause_quit_button.isOver_2(pos):
                    pause_quit_button.image = clicked_quit_button_image
                else:
                    pause_quit_button.image = quit_button_image
                pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button2.isOver(pos):
                    ui_variables.click_sound.play()
                    help_status = False
                    pause = True

                if pause_quit_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    done = True

                if help_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    help_status = True
                    #help = True

                if menu_button2.isOver_2(pos):
                    ui_variables.click_sound.play()
                    pause = False
                    start = False
                    if pvp:
                        pvp = False
                    if hard:
                        hard = False

                    if hard_training:
                        hard_training = False

                    if multi_training:
                        multi_training = False

                if resume_button.isOver_2(pos):
                    pygame.mixer.music.unpause()
                    pause = False
                    ui_variables.click_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, 1)  # 0.001초
            # 리사이징
            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)  # 블록 크기 고정
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)
                pygame.display.update()

    # training mode 중간 멈추는 screen
    elif pause_training:
        # ui_variables.intro_sound.stop()
        pygame.mixer.music.pause()

        # training_event가 하드의 3줄깨기 일 때,
        if training_event == 'hard_3line':
            draw_image(screen, training_box_image, board_width * 0.6,
                       board_height * 0.9, int(board_height * 0.2), int(board_height * 0.2))
            draw_image(screen, hard_3line_image, board_width * 0.3, board_height * 0.4,
                       int(board_height * 0.7), int(board_height * 0.55))
            training_event_happened['hard_3line'] = True

        # training_event가 하드의 10초 지남 일 때,
        elif training_event == 'hard_10sec':
            draw_image(screen, training_box_image, board_width * 0.6,
                       board_height * 0.7, int(board_height * 0.2), int(board_height * 0.2))
            draw_image(screen, hard_10s_image, board_width * 0.3, board_height * 0.4,
                       int(board_height * 0.7), int(board_height * 0.55))
            training_event_happened['hard_10sec'] = True

        # training_event가 멀티의 1P가 한 줄 이상 깸 일 때,
        elif training_event == 'multi_1P_break':
            draw_image(screen, training_box_image, board_width * 0.9,
                       board_height * 0.75, int(board_height * 0.2), int(board_height * 0.18))
            draw_image(screen, multi_1P_break_image, board_width * 0.65,
                       board_height * 0.4, int(board_height * 0.7), int(board_height * 0.55))
            training_event_happened['multi_1P_break'] = True

        # training_event가 멀티의 2P가 한 줄 이상 깸 일 때,
        elif training_event == 'multi_2P_break':
            draw_image(screen, training_box_image, board_width * 0.39,
                       board_height * 0.75, int(board_height * 0.2), int(board_height * 0.18))
            draw_image(screen, multi_2P_break_image, board_width * 0.2,
                       board_height * 0.4, int(board_height * 0.7), int(board_height * 0.55))
            training_event_happened['multi_2P_break'] = True

        # draw_image(screen, pause_board_image, board_width * 0.5, board_height * 0.5,
        #            int(board_height * 1), board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                pygame.display.update()
            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation, matrix)
                if event.key == K_RETURN:
                    pause_training = False
                    ui_variables.click_sound.play()
                    # ui_variables.intro_sound.play()
                    pygame.mixer.music.unpause()
                    pygame.time.set_timer(pygame.USEREVENT, 1)
            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate + 0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)  # 블록 크기비율 고정
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)

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
                        pygame.time.set_timer(pygame.USEREVENT, game_speed)

                # Draw a mino
                draw_mino(dx, dy, mino, rotation, matrix)
                draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                           0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                draw_board(next_mino1, next_mino2,
                           hold_mino, score, level, goal)

                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation, matrix)

                # Move mino down
                if not is_bottom(dx, dy, mino, rotation, matrix):
                    dy += 1

                # Create new mino
                else:
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        score += 10 * level
                        draw_mino(dx, dy, mino, rotation, matrix)
                        screen.fill(ui_variables.real_white)
                        draw_image(screen, gamebackground_image, board_width *
                                   0.5, board_height * 0.5, board_width, board_height)
                        draw_board(next_mino1, next_mino2,
                                   hold_mino, score, level, goal)
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
                            ui_variables.GameOver_sound.play()
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
                    # blit(이미지, 위치)
                    screen.blit(ui_variables.LevelUp_vector,
                                (board_width * 0.28, board_height * 0.1))
                    pygame.display.update()
                    pygame.time.delay(400)  # 0.4초
                    framerate = int(framerate * 0.8)

            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation, matrix)
                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    pause = True
                # Hard drop
                elif event.key == K_SPACE:
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation, matrix):
                        dy += 1
                    hard_drop = True
                    pygame.time.set_timer(pygame.USEREVENT, framerate)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_board(next_mino1, next_mino2,
                               hold_mino, score, level, goal)
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
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_board(next_mino1, next_mino2,
                               hold_mino, score, level, goal)
                # Turn right
                elif event.key == K_UP or event.key == K_x:
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
                    draw_board(next_mino1, next_mino2,
                               hold_mino, score, level, goal)
                # Turn left
                elif event.key == K_z or event.key == K_LCTRL:
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
                    draw_board(next_mino1, next_mino2,
                               hold_mino, score, level, goal)
                # Move left
                elif event.key == K_LEFT:
                    if not is_leftedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_board(next_mino1, next_mino2,
                               hold_mino, score, level, goal)
                # Move right
                elif event.key == K_RIGHT:
                    if not is_rightedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_board(next_mino1, next_mino2,
                               hold_mino, score, level, goal)

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)

        pygame.display.update()

    elif hard:
        if hard_time_setting == False:  # 타임 세팅이 안 되어 있으면
            start_ticks = pygame.time.get_ticks()  # 현재 시간을 타임어택 모드 시작 시간이라고 설정하고
            hard_time_setting = True  # 타임 세팅이 완료되었다고 바꾼다.

        elapsed_time = (pygame.time.get_ticks() -
                        start_ticks) / 1000  # 경과 시간 계산
        remaining_time = int(total_time - elapsed_time)  # 남은 시간

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            # 3줄마다 위아래 전환, 몫이 홀수이면 위로 전환, 0 또는 짝수이면 아래로
            change = line_count // 3  # 깬 줄//3 == 몫

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                # Set speed
                if not game_over:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_DOWN]:
                        # 프레임 시간만큼 빠르게 소프트드롭
                        pygame.time.set_timer(pygame.USEREVENT, framerate)
                    else:
                        pygame.time.set_timer(pygame.USEREVENT, game_speed)

                # Draw a mino
                draw_mino(dx, dy, mino, rotation, matrix)
                screen.fill(ui_variables.real_white)
                draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                           0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                # change가 홀수이면 위아래전환, 아니면 원래대로
                if change % 2 == 1:
                    draw_hardboard_change(
                        next_mino1, next_mino2, hold_mino, score, remaining_time, line_count)
                else:
                    draw_hardboard(next_mino1, next_mino2, hold_mino,
                                   score, remaining_time, line_count)
                    pygame.display.update()

                current_time = pygame.time.get_ticks()
                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation, matrix)

                # Move mino down
                if not is_bottom(dx, dy, mino, rotation, matrix):
                    dy += 1

                else:
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        draw_mino(dx, dy, mino, rotation, matrix)
                        screen.fill(ui_variables.real_white)
                        draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                                   0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                        # change가 홀수이면 위아래전환, 아니면 원래대로
                        if change % 2 == 1:
                            draw_hardboard_change(
                                next_mino1, next_mino2, hold_mino, score, remaining_time, line_count)
                        else:
                            draw_hardboard(
                                next_mino1, next_mino2, hold_mino, score, remaining_time, line_count)
                            pygame.display.update()

                        if is_stackable(next_mino1, matrix):
                            mino = next_mino1
                            next_mino1 = next_mino2
                            next_mino2 = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                        else:
                            hard = False
                            game_status = 'hard'
                            game_over = True
                            ui_variables.GameOver_sound.play()
                            pygame.time.set_timer(
                                pygame.USEREVENT, 1)  # 0.001초
                    else:
                        bottom_count += 1

                # Erase line
                erase_count = 0
                matrix_contents = []

                for j in range(board_y+1):
                    is_full = True
                    for i in range(board_x):
                        if matrix[i][j] == 0 or matrix[i][j] == 9:  # 빈 공간이거나, 장애물블록
                            is_full = False
                    if is_full:  # 한 줄 꽉 찼을 때
                        erase_count += 1
                        line_count += 1
                        # 화면이 뒤집히는 순간 (line_count가 3의 배수)
                        if line_count % 3 == 0 and line_count > 0:
                            # 화면 위아래 뒤집힌 알림 띄우기
                            draw_image(screen, hard_flipped_image, board_width * 0.4,
                                       board_height * 0.2, int(board_width*0.3), int(board_height*0.1))
                        pygame.display.update()
                        pygame.time.delay(400)
                        k = j

                        for i in range(board_x):

                            # 현재 클리어된 줄에 있는 mino 종류들 저장
                            matrix_contents.append(matrix[i][j])

                        while k > 0:
                            for i in range(board_x):
                                # 남아있는 블록 한 줄씩 내리기(덮어쓰기)
                                matrix[i][k] = matrix[i][k - 1]
                            k -= 1

                if erase_count >= 1:
                    # 점수 계산
                    if erase_count == 1:
                        ui_variables.break_sound.play()
                        ui_variables.single_sound.play()
                        score += 50 * level * erase_count
                    elif erase_count == 2:
                        ui_variables.break_sound.play()
                        ui_variables.double_sound.play()
                        ui_variables.double_sound.play()
                        score += 150 * level * erase_count
                    elif erase_count == 3:
                        ui_variables.break_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        score += 350 * level * erase_count
                    elif erase_count == 4:
                        ui_variables.break_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        score += 1000 * level * erase_count
                        screen.blit(ui_variables.combo_4ring,
                                    (250, 160))  # blit(이미지, 위치)

                # 10초마다 속도 빨라지게
                if (remaining_time % 10 == 0) and (remaining_time != 60):
                    ui_variables.LevelUp_sound.play()
                    draw_image(screen, hard_speed_up_image, board_width * 0.4,
                               board_height * 0.2, int(board_width*0.3), int(board_height*0.1))
                    framerate = int(framerate - speed_change)
                    # Change_RATE += 1
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
                    draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                               0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    # change가 홀수이면 위아래전환, 아니면 원래대로
                    if change % 2 == 1:
                        draw_hardboard_change(
                            next_mino1, next_mino2, hold_mino, score, remaining_time, line_count)
                    else:
                        draw_hardboard(next_mino1, next_mino2, hold_mino,
                                       score, remaining_time, line_count)
                elif event.key == K_j:
                    framerate = int(framerate-speed_change)
                    print(framerate)

                # Hold
                elif event.key == K_RSHIFT:  # keyboard 변경하기
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
                    draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                               0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    # change가 홀수이면 위아래전환, 아니면 원래대로
                    if change % 2 == 1:
                        draw_hardboard_change(
                            next_mino1, next_mino2, hold_mino, score, remaining_time, line_count)
                    else:
                        draw_hardboard(next_mino1, next_mino2, hold_mino,
                                       score, remaining_time, line_count)

                # dx, dy는 각각 좌표위치 이동에 해당하며, rotation은 mino.py의 테트리스 블록 회전에 해당함
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
                    draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                               0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    # change가 홀수이면 위아래전환, 아니면 원래대로
                    if change % 2 == 1:
                        draw_hardboard_change(
                            next_mino1, next_mino2, hold_mino, score, remaining_time, line_count)
                    else:
                        draw_hardboard(next_mino1, next_mino2, hold_mino,
                                       score, remaining_time, line_count)

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
                    draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                               0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    # change가 홀수이면 위아래전환, 아니면 원래대로
                    if change % 2 == 1:
                        draw_hardboard_change(
                            next_mino1, next_mino2, hold_mino, score, remaining_time, line_count)
                    else:
                        draw_hardboard(next_mino1, next_mino2, hold_mino,
                                       score, remaining_time, line_count)

                # Move left
                elif event.key == K_LEFT:
                    if not is_leftedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                               0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    # change가 홀수이면 위아래전환, 아니면 원래대로
                    if change % 2 == 1:
                        draw_hardboard_change(
                            next_mino1, next_mino2, hold_mino, score, remaining_time, line_count)
                    else:
                        draw_hardboard(next_mino1, next_mino2, hold_mino,
                                       score, remaining_time, line_count)

                # Move right
                elif event.key == K_RIGHT:
                    if not is_rightedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                               0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    # change가 홀수이면 위아래전환, 아니면 원래대로
                    if change % 2 == 1:
                        draw_hardboard_change(
                            next_mino1, next_mino2, hold_mino, score, remaining_time, line_count)
                    else:
                        draw_hardboard(next_mino1, next_mino2, hold_mino,
                                       score, remaining_time, line_count)

                # debug mode block change
                elif debug:
                    if event.key == K_1:
                        ui_variables.click_sound.play()
                        mino = 1  # 빨
                    if event.key == K_2:
                        ui_variables.click_sound.play()
                        mino = 2  # 빨
                    if event.key == K_3:
                        ui_variables.click_sound.play()
                        mino = 3  # 빨
                    if event.key == K_4:
                        ui_variables.click_sound.play()
                        mino = 4  # 빨
                    if event.key == K_5:
                        ui_variables.click_sound.play()
                        mino = 5  # 빨
                    if event.key == K_6:
                        ui_variables.click_sound.play()
                        mino = 6  # 빨
                    if event.key == K_7:
                        ui_variables.click_sound.play()
                        mino = 7  # 빨

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)

        if total_time - elapsed_time < 0:  # 60초가 지났으면
            hard = False
            game_status = 'hard'
            game_over = True
            ui_variables.GameOver_sound.play()
            pygame.time.set_timer(pygame.USEREVENT, 1)

        pygame.display.update()

    elif pvp:

        for event in pygame.event.get():
            if event.type == QUIT:
                done = True

            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, game_speed)  # 기본 게임속도 

                # Draw a mino
                draw_mino(dx, dy, mino, rotation, matrix)
                draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                hold_mino_2P, current_key, current_key_2P)

                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation, matrix)
                    erase_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)

                if combo_count == 5:  # 5줄을 먼저 깨면 게임 종료
                    winner = 1
                    game_status = 'pvp'
                    pvp = False
                    game_over = True
                    ui_variables.GameOver_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, 1)

                if combo_count_2P == 5:  # 5줄을 먼저 깨면 게임 종료
                    winner = 2
                    game_status = 'pvp'
                    pvp = False
                    game_over = True
                    ui_variables.GameOver_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                ### 1P ###
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
                            next_mino1 = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                            score += 10 * level
                        else:  # 더이상 쌓을 수 없으면 게임오버
                            winner = 2
                            game_status = 'pvp'
                            pvp = False
                            game_over = True
                            ui_variables.GameOver_sound.play()
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count += 1

                ### 2P ###
                # Move mino down
                if not is_bottom(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                    dy_2P += 1

                # Create new mino
                else:

                    if hard_drop_2P or bottom_count_2P == 6:
                        hard_drop_2P = False
                        bottom_count_2P = 0
                        draw_mino(dx_2P, dy_2P, mino_2P,
                                  rotation_2P, matrix_2P)

                        if is_stackable(next_mino1_2P, matrix_2P):
                            mino_2P = next_mino1_2P
                            next_mino1_2P = randint(1, 7)
                            dx_2P, dy_2P = 3, 0
                            rotation_2P = 0
                            hold_2P = False
                            score_2P += 10 * level_2P
                        else:  # 더이상 쌓을 수 없으면 게임오버
                            winner = 1
                            game_status = 'pvp'
                            pvp = False
                            game_over = True
                            ui_variables.GameOver_sound.play()
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count_2P += 1

                # Erase line
                # 콤보 카운트
                # erase_count = 0
                # erase_count_2P = 0
                # attack_line = 0
                # attack_line_2P = 0

                # 한 줄이 차면 그 위의 블럭들 한 줄씩 아래로 내리기. (1P)
                for j in range(board_y + 1):
                    is_full = True  # 한 줄이 가득 찼는지 확인하기 위한 변수
                    for i in range(board_x):
                        if matrix[i][j] == 0:  # 빈 곳인 경우
                            is_full = False  # 클리어 되지 못함
                    if is_full:
                        # erase_count += 1
                        combo_count += 1
                        key_reverse_2P = True  # 상대방 키 반전조건 성립 (몇 줄을 깨든)
                        draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                        hold_mino_2P, current_key, current_key_2P)
                        # 2P 보드에 key reverse 이미지 표시
                        draw_image(screen, multi_key_reverse_image, board_width * 0.8,
                                   board_height * 0.2, int(board_width * 0.3), int(board_height * 0.12))
                        pygame.display.update()
                        pygame.time.delay(400)
                        ui_variables.break_sound.play()
                        k = j

                        while k > 0:  # y좌표가 matrix 안에 있는 동안
                            for i in range(board_x):  # 해당 줄의 x좌표들 모두
                                matrix[i][k] = matrix[i][k - 1]  # 한줄씩 밑으로 내림
                            k -= 1

                # 한 줄이 차면 그 위의 블럭들 한 줄씩 아래로 내리기. (2P)
                for j in range(board_y + 1):
                    is_full = True
                    for i in range(board_x):
                        if matrix_2P[i][j] == 0:  # 빈 곳인 경우
                            is_full = False  # 클리어 되지 못함
                    if is_full:
                        # erase_count_2P += 1
                        combo_count_2P += 1
                        key_reverse = True  # 상대방 키 반전조건 성립 (몇 줄을 깨든)
                        draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                        hold_mino_2P, current_key, current_key_2P)
                        # 1P 보드에 key reverse 이미지 표시
                        draw_image(screen, multi_key_reverse_image, board_width * 0.2,
                                   board_height * 0.2, int(board_width * 0.28), int(board_height * 0.1))
                        pygame.display.update()
                        pygame.time.delay(400)
                        ui_variables.break_sound.play()
                        k = j
                        while k > 0:  # y좌표가 matrix 안에 있는 동안
                            for i in range(board_x):  # 해당 줄의 x좌표들 모두
                                # 한줄씩 밑으로 내림
                                matrix_2P[i][k] = matrix_2P[i][k - 1]
                            k -= 1

                if key_reverse:   # 키 반전 조건(상대가 몇 줄이든 깸)이 성립됐다면
                    # 방향키 반전 (최근 방향키가 어떤 것이었든 반대로)
                    current_key = not current_key
                    key1 = multi_reverse_key(current_key, 1)
                    key_reverse = False  # 다시 키 반전 조건은 False로 (default)
                if key_reverse_2P:
                    current_key_2P = not current_key_2P
                    key2 = multi_reverse_key(current_key_2P, 2)
                    key_reverse_2P = False

            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation, matrix)
                erase_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)

                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    pause = True

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
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
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
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)

                    # dx, dy는 각각 좌표위치 이동에 해당하며, rotation은 mino.py의 테트리스 블록 회전에 해당함
                    # Hard drop
                # 왼쪽창#
                elif event.key == key1['hardDrop']:
                    ui_variables.fall_sound.play()
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation, matrix):
                        dy += 1
                    hard_drop = True
                    pygame.time.set_timer(pygame.USEREVENT, framerate)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                elif event.key == key2['hardDrop']:  # 오른쪽창#
                    ui_variables.fall_sound.play()
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        dy_2P += 1
                    hard_drop_2P = True
                    pygame.time.set_timer(pygame.USEREVENT, framerate_2P)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)

                # Turn right
                elif event.key == key1['turnRight']:  # 왼쪽창#
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
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                elif event.key == key2['turnRight']:  # 오른쪽창#
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
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)

                # Turn left
                elif event.key == key1['turnLeft']:
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
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                elif event.key == key2['turnLeft']:  # 오른쪽창#
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
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)

                # Move left (1P)
                # key = pygame.key.get_pressed()
                elif event.key == key1['moveLeft']:
                    if not is_leftedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(
                            pygame.KEYUP, framerate_blockmove)
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                # Move right (1P)
                elif event.key == key1['moveRight']:
                    if not is_rightedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(
                            pygame.KEYUP, framerate_blockmove)
                        dx += 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)

                # Move left(2P)
                elif event.key == key2['moveLeft']:
                    if not is_leftedge(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(
                            pygame.KEYUP, framerate_2P_blockmove)
                        dx_2P -= 1
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                # Move right(2P)
                elif event.key == key2['moveRight']:
                    if not is_rightedge(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(
                            pygame.KEYUP, framerate_2P_blockmove)
                        dx_2P += 1
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)

                # Soft drop (1P)
                elif event.key == key1['softDrop']:
                    if not is_bottom(dx, dy, mino, rotation, matrix):
                        dy = dy + 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P,
                                    current_key, current_key_2P)
                # Soft drop (2P)
                elif event.key == key2['softDrop']:
                    if not is_bottom(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        dy_2P = dy_2P + 1
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P,
                                    current_key, current_key_2P)

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate - 0.1) < (board_height / board_width) < (
                        board_rate + 0.05)):  # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width * board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)  # 블록 크기비율 고정
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)

        pygame.display.update()

    elif multi_training:

        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                # Set speed
                pygame.time.set_timer(pygame.USEREVENT, game_speed)

                # Draw a mino
                draw_mino(dx, dy, mino, rotation, matrix)
                draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                hold_mino_2P, current_key, current_key_2P)
                # 안내 문구 이미지 띄우기 "1줄 (이상) 깨기" - 한 플레이어도 한 줄도 안 깼을 때
                if (combo_count == 0 and combo_count_2P == 0):
                    draw_image(screen, line_message_multi_break_image, board_width * 0.5,
                               board_height * 0.2, board_width * 0.5, board_height * 0.1)

                # 안내 문구 이미지 띄우기 "5줄 깨야 이김" - 어떤 플레이어든 한  줄 이상 깬 후로
                if (combo_count_2P >= 1 or combo_count_2P >= 1):
                    draw_image(screen, line_message_multi_win_image, board_width * 0.5,
                               board_height * 0.2, board_width * 0.5, board_height * 0.1)
                pygame.display.update()

                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation, matrix)
                    erase_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)

                if combo_count == 5:  # 5줄을 먼저 깨면 게임 종료
                    winner = 1
                    # 트레이닝 모드는 게임 종료 전에 pause_training 상태로 넘어가 설명 띄우기
                    # training_event = 'multi_5break'
                    # pause_training = True

                    training_event = 'multi_game_over'
                    multi_training = False
                    game_over_training = True
                    ui_variables.GameOver_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, 1)

                if combo_count_2P == 5:  # 5줄을 먼저 깨면 게임 종료
                    winner = 2
                    # 트레이닝 모드는 게임 종료 전에 pause_training 상태로 넘어가 설명 띄우기
                    # training_event = 'multi_5break'
                    # pause_training = True

                    training_event = 'multi_game_over'
                    multi_training = False
                    game_over_training = True
                    ui_variables.GameOver_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                ### 1P ###
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
                            next_mino1 = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                            score += 10 * level
                        else:  # 더이상 쌓을 수 없으면 게임오버
                            training_event = 'multi_game_over'
                            multi_training = False
                            game_over_training = True

                            winner = 2
                            ui_variables.GameOver_sound.play()
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count += 1

                ### 2P ###
                # Move mino down
                if not is_bottom(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                    dy_2P += 1

                # Create new mino
                else:

                    if hard_drop_2P or bottom_count_2P == 6:
                        hard_drop_2P = False
                        bottom_count_2P = 0
                        draw_mino(dx_2P, dy_2P, mino_2P,
                                  rotation_2P, matrix_2P)

                        if is_stackable(next_mino1_2P, matrix_2P):
                            mino_2P = next_mino1_2P
                            next_mino1_2P = randint(1, 7)
                            dx_2P, dy_2P = 3, 0
                            rotation_2P = 0
                            hold_2P = False
                            score_2P += 10 * level_2P
                        else:  # 더이상 쌓을 수 없으면 게임오버
                            training_event = 'multi_game_over'
                            multi_training = False
                            game_over_training = True

                            winner = 1
                            ui_variables.GameOver_sound.play()
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count_2P += 1

                # Erase line
                # 콤보 카운트
                # erase_count = 0
                # erase_count_2P = 0
                # attack_line = 0
                # attack_line_2P = 0

                # 한 줄이 차면 그 위의 블럭들 한 줄씩 아래로 내리기. (1P)
                for j in range(board_y + 1):
                    is_full = True  # 한 줄이 가득 찼는지 확인하기 위한 변수
                    for i in range(board_x):
                        if matrix[i][j] == 0:  # 빈 곳인 경우
                            is_full = False  # 클리어 되지 못함
                    if is_full:
                        # erase_count += 1
                        combo_count += 1
                        key_reverse_2P = True  # 상대방 키 반전조건 성립 (몇 줄을 깨든)
                        draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                        hold_mino_2P, current_key, current_key_2P)
                        # 2P 보드에 key reverse 이미지 표시
                        draw_image(screen, multi_key_reverse_image, board_width * 0.77,
                                   board_height * 0.2, int(board_width * 0.28), int(board_height * 0.1))
                        pygame.display.update()
                        ui_variables.break_sound.play()
                        k = j

                        while k > 0:  # y좌표가 matrix 안에 있는 동안
                            for i in range(board_x):  # 해당 줄의 x좌표들 모두
                                matrix[i][k] = matrix[i][k - 1]  # 한줄씩 밑으로 내림
                            k -= 1

                # 한 줄이 차면 그 위의 블럭들 한 줄씩 아래로 내리기. (2P)
                for j in range(board_y + 1):
                    is_full = True
                    for i in range(board_x):
                        if matrix_2P[i][j] == 0:  # 빈 곳인 경우
                            is_full = False  # 클리어 되지 못함
                    if is_full:
                        # erase_count_2P += 1
                        combo_count_2P += 1
                        key_reverse = True  # 상대방 키 반전조건 성립 (몇 줄을 깨든)
                        draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                        hold_mino_2P, current_key, current_key_2P)
                        # 1P 보드에 key reverse 이미지 표시
                        draw_image(screen, multi_key_reverse_image, board_width * 0.2,
                                   board_height * 0.2, int(board_width * 0.28), int(board_height * 0.1))
                        pygame.display.update()
                        ui_variables.break_sound.play()
                        k = j
                        while k > 0:  # y좌표가 matrix 안에 있는 동안
                            for i in range(board_x):  # 해당 줄의 x좌표들 모두
                                # 한줄씩 밑으로 내림
                                matrix_2P[i][k] = matrix_2P[i][k - 1]
                            k -= 1

                if key_reverse:   # 1P의 키 반전 조건(2P가 몇 줄이든 깸)이 성립됐다면
                    # 방향키 반전 (최근 방향키가 어떤 것이었든 반대로)
                    current_key = not current_key
                    key1 = multi_reverse_key(current_key, 1)
                    key_reverse = False  # 다시 키 반전 조건은 False로 (default)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                    pygame.display.update()
                    if not training_event_happened['multi_2P_break']:
                        # 트레이닝 모드에서 2P가 줄을 깬 경우로 설명
                        training_event = 'multi_2P_break'
                        pause_training = True

                if key_reverse_2P:   # 2P의 키 반전 조건(1P가 몇 줄이든 깸)이 성립됐다면
                    current_key_2P = not current_key_2P
                    key2 = multi_reverse_key(current_key_2P, 2)
                    key_reverse_2P = False

                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                    pygame.display.update()
                    if not training_event_happened['multi_1P_break']:
                        # 트레이닝 모드에서 1P가 줄을 깬 경우로 설명
                        training_event = 'multi_1P_break'
                        pause_training = True

            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation, matrix)
                erase_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)

                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    pause = True

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
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
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
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)

                # dx, dy는 각각 좌표위치 이동에 해당하며, rotation은 mino.py의 테트리스 블록 회전에 해당함
                # Hard drop
                # 왼쪽창#
                elif event.key == key1['hardDrop']:
                    ui_variables.fall_sound.play()
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation, matrix):
                        dy += 1
                    hard_drop = True
                    pygame.time.set_timer(pygame.USEREVENT, framerate)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                elif event.key == key2['hardDrop']:  # 오른쪽창#
                    ui_variables.fall_sound.play()
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        dy_2P += 1
                    hard_drop_2P = True
                    pygame.time.set_timer(pygame.USEREVENT, framerate_2P)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)

                # Turn right
                elif event.key == key1['turnRight']:  # 왼쪽창#
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
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                elif event.key == key2['turnRight']:  # 오른쪽창#
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
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)

                # Turn left
                elif event.key == key1['turnLeft']:
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
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                elif event.key == key2['turnLeft']:  # 오른쪽창#
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
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)

                # Move left (1P)
                # key = pygame.key.get_pressed()
                elif event.key == key1['moveLeft']:
                    if not is_leftedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(
                            pygame.KEYUP, framerate_blockmove)
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                # Move right (1P)
                elif event.key == key1['moveRight']:
                    if not is_rightedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(
                            pygame.KEYUP, framerate_blockmove)
                        dx += 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)

                # Move left(2P)
                elif event.key == key2['moveLeft']:
                    if not is_leftedge(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(
                            pygame.KEYUP, framerate_2P_blockmove)
                        dx_2P -= 1
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                # Move right(2P)
                elif event.key == key2['moveRight']:
                    if not is_rightedge(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(
                            pygame.KEYUP, framerate_2P_blockmove)
                        dx_2P += 1
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                
                # Soft drop (1P)
                elif event.key == key1['softDrop']:
                    if not is_bottom(dx, dy, mino, rotation, matrix):
                        dy = dy + 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P,
                                    current_key, current_key_2P)
                # Soft drop (2P)
                elif event.key == key2['softDrop']:
                    if not is_bottom(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        dy_2P = dy_2P + 1
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P,
                                    current_key, current_key_2P)

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate - 0.1) < (board_height / board_width) < (
                        board_rate + 0.05)):  # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width * board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)  # 블록 크기비율 고정
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)

        pygame.display.update()

    elif hard_training:

        if hard_time_setting == False:  # 타임 세팅이 안 되어 있으면
            start_ticks = pygame.time.get_ticks()  # 현재 시간을 타임어택 모드 시작 시간이라고 설정하고
            hard_time_setting = True  # 타임 세팅이 완료되었다고 바꾼다.

        elapsed_time = (pygame.time.get_ticks() -
                        start_ticks) / 1000  # 경과 시간 계산
        remaining_time = int(total_time - elapsed_time)  # 남은 시간

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            # 3줄마다 위아래 전환, 몫이 홀수이면 위로 전환, 0 또는 짝수이면 아래로
            change = line_count // 3  # 깬 줄//3 == 몫

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                # Set speed
                if not game_over:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_DOWN]:
                        # 프레임 시간만큼 빠르게 소프트드롭
                        pygame.time.set_timer(pygame.USEREVENT, framerate)
                    else:
                        pygame.time.set_timer(pygame.USEREVENT, game_speed)

                # Draw a mino
                draw_mino(dx, dy, mino, rotation, matrix)
                screen.fill(ui_variables.real_white)
                draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                           0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                # change가 홀수이면 위아래전환, 아니면 원래대로
                if change % 2 == 1:
                    draw_hardboard_change(
                        next_mino1, next_mino2, hold_mino, score, remaining_time, line_count)
                else:
                    draw_hardboard(next_mino1, next_mino2, hold_mino,
                                   score, remaining_time, line_count)
                pygame.display.update()

                current_time = pygame.time.get_ticks()
                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation, matrix)

                # Move mino down
                if not is_bottom(dx, dy, mino, rotation, matrix):
                    dy += 1

                else:
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        draw_mino(dx, dy, mino, rotation, matrix)
                        screen.fill(ui_variables.real_white)
                        draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                                   0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                        # change가 홀수이면 위아래전환, 아니면 원래대로
                        if change % 2 == 1:
                            draw_hardboard_change(
                                next_mino1, next_mino2, hold_mino, score, remaining_time, line_count)
                        else:
                            draw_hardboard(
                                next_mino1, next_mino2, hold_mino, score, remaining_time, line_count)
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
                            training_event = 'hard_game_over'
                            hard_training = False
                            game_over_training = True
                            pygame.time.set_timer(
                                pygame.USEREVENT, 1)  # 0.001초
                    else:
                        bottom_count += 1

                # Erase line
                erase_count = 0
                matrix_contents = []

                for j in range(board_y+1):
                    is_full = True
                    for i in range(board_x):
                        if matrix[i][j] == 0 or matrix[i][j] == 9:  # 빈 공간이거나, 장애물블록
                            is_full = False
                    if is_full:  # 한 줄 꽉 찼을 때
                        erase_count += 1
                        line_count += 1
                        # 화면이 뒤집히는 순간 (line_count가 3의 배수)
                        if line_count % 3 == 0 and line_count > 0:
                            # 화면 위아래 뒤집힌 알림 띄우기
                            draw_image(screen, hard_flipped_image, board_width * 0.4,
                                       board_height * 0.2, int(board_width*0.3), int(board_height*0.1))
                        pygame.display.update()
                        pygame.time.delay(400)
                        k = j

                        for i in range(board_x):

                            # 현재 클리어된 줄에 있는 mino 종류들 저장
                            matrix_contents.append(matrix[i][j])

                        while k > 0:
                            for i in range(board_x):
                                # 남아있는 블록 한 줄씩 내리기(덮어쓰기)
                                matrix[i][k] = matrix[i][k - 1]
                            k -= 1

                if erase_count >= 1:
                    # 점수 계산
                    if erase_count == 1:
                        ui_variables.break_sound.play()
                        ui_variables.single_sound.play()
                        score += 50 * level * erase_count
                    elif erase_count == 2:
                        ui_variables.break_sound.play()
                        ui_variables.double_sound.play()
                        ui_variables.double_sound.play()
                        score += 150 * level * erase_count
                    elif erase_count == 3:
                        ui_variables.break_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        score += 350 * level * erase_count
                    elif erase_count == 4:
                        ui_variables.break_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        score += 1000 * level * erase_count

                # 10초마다 속도 빨라지게
                if (remaining_time % 10 == 0) and (remaining_time != 60):
                    ui_variables.LevelUp_sound.play()
                    draw_image(screen, hard_speed_up_image, board_width * 0.4,
                               board_height * 0.2, int(board_width*0.3), int(board_height*0.1))
                    framerate = int(framerate - speed_change)
                    # Change_RATE += 1
                    # set_music_playing_speed(CHANNELS, swidth, Change_RATE)

                # 3줄 깨면 설명 나오게 pause_training로 연결
                # if (line_count >= 3 and training_event != 'no_event'):
                if (line_count >= 3 and not training_event_happened['hard_3line']):
                    pause_training = True
                    training_event = 'hard_3line'

                # 10초 지나면 설명 나오게 pause_training로 연결
                if (remaining_time == 50):
                    pause_training = True
                    training_event = 'hard_10sec'

                # 시작하자마자 팝업 알림 띄우기
                if (0 < elapsed_time < 2):
                    # 시작하자마자 팝업 알림 띄우기 (먼저, 3줄을 깨보세요)
                    draw_image(screen, hard_line_message, board_width * 0.4,
                               board_height * 0.2, int(board_width*0.6), int(board_height*0.1))
                    # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    pygame.time.set_timer(pygame.USEREVENT, 300)

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
                    draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                               0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    # change가 홀수이면 위아래전환, 아니면 원래대로
                    if change % 2 == 1:
                        draw_hardboard_change(
                            next_mino1, next_mino2, hold_mino, score, remaining_time, line_count)
                    else:
                        draw_hardboard(next_mino1, next_mino2, hold_mino,
                                       score, remaining_time, line_count)

                    pygame.display.update()
                elif event.key == K_j:
                    framerate = int(framerate-speed_change)
                    print(framerate)

                # Hold
                elif event.key == K_RSHIFT:  # keyboard 변경하기
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
                    draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                               0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    # change가 홀수이면 위아래전환, 아니면 원래대로
                    if change % 2 == 1:
                        draw_hardboard_change(
                            next_mino1, next_mino2, hold_mino, score, remaining_time, line_count)
                    else:
                        draw_hardboard(next_mino1, next_mino2, hold_mino,
                                       score, remaining_time, line_count)

                # dx, dy는 각각 좌표위치 이동에 해당하며, rotation은 mino.py의 테트리스 블록 회전에 해당함
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
                    draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                               0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    # change가 홀수이면 위아래전환, 아니면 원래대로
                    if change % 2 == 1:
                        draw_hardboard_change(
                            next_mino1, next_mino2, hold_mino, score, remaining_time, line_count)
                    else:
                        draw_hardboard(next_mino1, next_mino2, hold_mino,
                                       score, remaining_time, line_count)

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
                    draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                               0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    # change가 홀수이면 위아래전환, 아니면 원래대로
                    if change % 2 == 1:
                        draw_hardboard_change(
                            next_mino1, next_mino2, hold_mino, score, remaining_time, line_count)
                    else:
                        draw_hardboard(next_mino1, next_mino2, hold_mino,
                                       score, remaining_time, line_count)

                # Move left
                elif event.key == K_LEFT:
                    if not is_leftedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                               0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    # change가 홀수이면 위아래전환, 아니면 원래대로
                    if change % 2 == 1:
                        draw_hardboard_change(
                            next_mino1, next_mino2, hold_mino, score, remaining_time, line_count)
                    else:
                        draw_hardboard(next_mino1, next_mino2, hold_mino,
                                       score, remaining_time, line_count)

                # Move right
                elif event.key == K_RIGHT:
                    if not is_rightedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                               0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    # change가 홀수이면 위아래전환, 아니면 원래대로
                    if change % 2 == 1:
                        draw_hardboard_change(
                            next_mino1, next_mino2, hold_mino, score, remaining_time, line_count)
                    else:
                        draw_hardboard(next_mino1, next_mino2, hold_mino,
                                       score, remaining_time, line_count)

                # debug mode block change
                elif debug:
                    if event.key == K_1:
                        ui_variables.click_sound.play()
                        mino = 1  # 빨
                    if event.key == K_2:
                        ui_variables.click_sound.play()
                        mino = 2  # 빨
                    if event.key == K_3:
                        ui_variables.click_sound.play()
                        mino = 3  # 빨
                    if event.key == K_4:
                        ui_variables.click_sound.play()
                        mino = 4  # 빨
                    if event.key == K_5:
                        ui_variables.click_sound.play()
                        mino = 5  # 빨
                    if event.key == K_6:
                        ui_variables.click_sound.play()
                        mino = 6  # 빨
                    if event.key == K_7:
                        ui_variables.click_sound.play()
                        mino = 7  # 빨

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)

        if total_time - elapsed_time < 0:  # 60초가 지났으면
            ui_variables.GameOver_sound.play()
            training_event = 'hard_game_over'
            hard_training = False
            game_over_training = True
            pygame.time.set_timer(pygame.USEREVENT, 1)

        pygame.display.update()

    # new game over screen
    elif game_over:

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.mixer.music.stop()

                pygame.time.set_timer(pygame.USEREVENT, 300)  # 0.3초

                if game_status == 'pvp':
                    # 기존 화면 약간 어둡게 처리
                    draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                               0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P,
                                    current_key, current_key_2P)
                    pause_surface = screen.convert_alpha()  # 투명 가능하도록
                    pause_surface.fill((0, 0, 0, 0))  # 투명한 검정색으로 덮기
                    pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(
                        board_width), int(board_height)])  # (screen, 색깔, 위치 x, y좌표, 너비, 높이)
                    screen.blit(pause_surface, (0, 0))
                    #

                    draw_image(screen, multi_gameover_image, board_width * 0.5, board_height * 0.2,
                               int(board_height * 0.7), int(board_height * 0.2))  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    if winner == 1:  # 1P가 이기면
                        draw_image(screen, multi_win_image, board_width * 0.2, board_height * 0.5,
                                   int(board_height * 0.3), int(board_height * 0.25))  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                        draw_image(screen, multi_lose_image, board_width * 0.8, board_height * 0.5,
                                   int(board_height * 0.3), int(board_height * 0.25))  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    elif winner == 2:  # 2P가 이기면
                        draw_image(screen, multi_win_image, board_width * 0.8, board_height * 0.5,
                                   int(board_height * 0.3), int(board_height * 0.25))  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                        draw_image(screen, multi_lose_image, board_width * 0.2, board_height * 0.5,
                                   int(board_height * 0.3), int(board_height * 0.25))  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)

                    multi_menu_button.draw(screen, (0, 0, 0))
                    multi_restart_button.draw(screen, (0, 0, 0))

                elif game_status != 'pvp':
                    draw_image(screen, gameover_board_image, board_width * 0.5, board_height * 0.5,
                               int(board_height * 1), board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    menu_button2.draw(screen, (0, 0, 0))  # rgb(0,0,0) = 검정색
                    restart_button.draw(screen, (0, 0, 0))
                    ok_button.draw(screen, (0, 0, 0))

                    # render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
                    name_1 = ui_variables.h1_b.render(
                        chr(name[0]), 1, ui_variables.white)
                    name_2 = ui_variables.h1_b.render(
                        chr(name[1]), 1, ui_variables.white)
                    name_3 = ui_variables.h1_b.render(
                        chr(name[2]), 1, ui_variables.white)

                    underbar_1 = ui_variables.h1_b.render(
                        "_", 1, ui_variables.white)
                    underbar_2 = ui_variables.h1_b.render(
                        "_", 1, ui_variables.white)
                    underbar_3 = ui_variables.h1_b.render(
                        "_", 1, ui_variables.white)

                    # blit(요소, 위치), 각각 전체 board의 가로길이, 세로길이에다가 원하는 비율을 곱해줌
                    screen.blit(name_1, (int(board_width * 0.434),
                                int(board_height * 0.55)))
                    screen.blit(name_2, (int(board_width * 0.494),
                                int(board_height * 0.55)))  # blit(요소, 위치)
                    screen.blit(name_3, (int(board_width * 0.545),
                                int(board_height * 0.55)))  # blit(요소, 위치)

                    if blink:
                        blink = False
                    else:
                        if name_location == 0:
                            # 위치 비율 고정
                            screen.blit(
                                underbar_1, ((int(board_width * 0.437), int(board_height * 0.56))))
                        elif name_location == 1:
                            # 위치 비율 고정
                            screen.blit(
                                underbar_2, ((int(board_width * 0.497), int(board_height * 0.56))))
                        elif name_location == 2:
                            # 위치 비율 고정
                            screen.blit(
                                underbar_3, ((int(board_width * 0.557), int(board_height * 0.56))))
                        blink = True

                pygame.display.update()

            elif event.type == KEYDOWN and game_status != 'pvp':  # 멀티모드 아닐 때만 스코어 저장

                if event.key == K_RETURN:
                    ui_variables.click_sound.play()
                    if game_status == 'start':  # easy mode일 경우
                        outfile = open('leaderboard.txt', 'a')
                        outfile.write(
                            chr(name[0]) + chr(name[1]) + chr(name[2]) + ' ' + str(score) + '\n')
                        outfile.close()
                    elif game_status == 'hard':  # hard mode일 경우
                        outfile = open('leaderboard_hard.txt', 'a')
                        outfile.write(
                            chr(name[0]) + chr(name[1]) + chr(name[2]) + ' ' + str(score) + '\n')
                        outfile.close()

                    game_over = False
                    pygame.time.set_timer(pygame.USEREVENT, 1)  # 0.001초

                # name은 3글자로 name_locationd은 0~2, name[name_location]은 영어 아스키코드로 65~90.
                elif event.key == K_RIGHT:
                    if name_location != 2:
                        name_location += 1
                    else:
                        name_location = 0
                    pygame.time.set_timer(pygame.USEREVENT, 1)  # 0.001초
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

            elif event.type == pygame.MOUSEMOTION:
                if menu_button2.isOver_2(pos):
                    menu_button2.image = clicked_menu_button_image
                else:
                    menu_button2.image = menu_button_image

                if restart_button.isOver_2(pos):
                    restart_button.image = clicked_restart_button_image
                else:
                    restart_button.image = restart_button_image

                if ok_button.isOver_2(pos):
                    ok_button.image = clicked_ok_button_image
                else:
                    ok_button.image = ok_button_image

                # 멀티모드 게임오버 화면 버튼
                if multi_menu_button.isOver_2(pos):
                    multi_menu_button.image = clicked_menu_button_image
                else:
                    multi_menu_button.image = menu_button_image

                if multi_restart_button.isOver_2(pos):
                    multi_restart_button.image = clicked_restart_button_image
                else:
                    multi_restart_button.image = restart_button_image

                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_status != 'pvp':
                    if ok_button.isOver(pos):
                        ui_variables.click_sound.play()
                        if game_status == 'start':  # easy mode 일 경우
                            outfile = open('leaderboard.txt', 'a')
                            outfile.write(
                                chr(name[0]) + chr(name[1]) + chr(name[2]) + ' ' + str(score) + '\n')
                            outfile.close()
                        elif game_status == 'hard':  # hard mode 일 경우
                            outfile = open('leaderboard_hard.txt', 'a')
                            outfile.write(
                                chr(name[0]) + chr(name[1]) + chr(name[2]) + ' ' + str(score) + '\n')
                            outfile.close()
                        game_over = False
                        pygame.time.set_timer(pygame.USEREVENT, 1)

                    if menu_button2.isOver(pos):
                        ui_variables.click_sound.play()
                        game_over = False

                    if restart_button.isOver_2(pos):
                        if game_status == 'start':
                            set_initial_values()
                            ui_variables.intro_sound.stop()
                            start = True
                            pygame.mixer.music.play(-1)  # play(-1) = 노래 반복재생
                        if game_status == 'pvp':
                            set_initial_values()
                            ui_variables.intro_sound.stop()
                            pvp = True
                            pygame.mixer.music.play(-1)
                        if game_status == 'hard':
                            set_initial_values()
                            ui_variables.intro_sound.stop()
                            hard = True
                            pygame.mixer.music.play(-1)
                        ui_variables.click_sound.play()
                        game_over = False
                        pause = False

                    if resume_button.isOver_2(pos):
                        pause = False
                        ui_variables.click_sound.play()
                        pygame.time.set_timer(pygame.USEREVENT, 1)  # 0.001초

                # 멀티모드 게임오버 화면 버튼
                if game_status == 'pvp':
                    if multi_menu_button.isOver_2(pos):
                        ui_variables.click_sound.play()
                        game_over = False
                    if multi_restart_button.isOver_2(pos):
                        set_initial_values()
                        pvp = True
                        pygame.mixer.music.play(-1)

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate + 0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)  # 블록 크기비율 고정
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)

    # new game over screen
    elif game_over_training:

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.mixer.music.stop()

                pygame.time.set_timer(pygame.USEREVENT, 300)  # 0.3초

                if training_event == 'multi_game_over':
                    # 이벤트 두개 모두 실행되었는지 확인
                    if training_event_happened['multi_1P_break'] == True and training_event_happened['multi_2P_break'] == True:
                        draw_image(screen, training_completed_image, board_width * 0.5, board_height * 0.5,
                                   int(board_height * 1.3), (board_height))  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    else:
                        draw_image(screen, training_incomplete_image, board_width * 0.5, board_height * 0.5,
                                   int(board_height * 1.3), (board_height))  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    training_multi_start_button.draw(screen, (0, 0, 0))
                    training_restart_button.draw(screen, (0, 0, 0))
                pygame.display.update()

                if training_event == 'hard_game_over':
                    # 이벤트 두개 모두 실행되었는지 확인
                    if training_event_happened['hard_3line'] == True and training_event_happened['hard_10sec'] == True:
                        draw_image(screen, training_completed_image, board_width * 0.5, board_height * 0.5,
                                   int(board_height * 1.3), (board_height))  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    else:
                        draw_image(screen, training_incomplete_image, board_width * 0.5, board_height * 0.5,
                                   int(board_height * 1.3), (board_height))  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    training_hard_start_button.draw(screen, (0, 0, 0))
                    training_restart_button.draw(screen, (0, 0, 0))
                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if training_multi_start_button.isOver_2(pos):
                    training_multi_start_button.image = clicked_pvp_button_image
                else:
                    training_multi_start_button.image = pvp_button_image

                if training_restart_button.isOver_2(pos):
                    training_restart_button.image = clicked_restart_button_image
                else:
                    training_restart_button.image = restart_button_image

                if training_hard_start_button.isOver_2(pos):
                    training_hard_start_button.image = clicked_hard_button_image
                else:
                    training_hard_start_button.image = hard_button_image
                pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if training_event == 'multi_game_over':
                    if training_restart_button.isOver_2(pos):
                        ui_variables.click_sound.play()
                        set_initial_values()
                        multi_training_info = True
                        training_status = True
                        pygame.mixer.music.play(-1)
                    if training_multi_start_button.isOver_2(pos):
                        ui_variables.click_sound.play()
                        set_initial_values()
                        game_over_training = False
                        pvp = True
                        pygame.mixer.music.play(-1)

                if training_event == 'hard_game_over':
                    if training_hard_start_button.isOver_2(pos):
                        ui_variables.click_sound.play()
                        set_initial_values()
                        game_over_training = False
                        hard = True
                        pygame.mixer.music.play(-1)

                    if training_restart_button.isOver_2(pos):
                        ui_variables.click_sound.play()
                        set_initial_values()
                        hard_training_info = True
                        training_status = True
                        pygame.mixer.music.play(-1)
                        game_over = False
                        hard_training = False

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate + 0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)  # 블록 크기비율 고정
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)

    elif select_mode:
        screen.fill(ui_variables.real_white)
        draw_image(screen, background_image, board_width * 0.5, board_height *
                   0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
        pause_surface = screen.convert_alpha()  # 투명 가능하도록
        pause_surface.fill((0, 0, 0, 0))  # 투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(
            board_width), int(board_height)])  # (screen, 색깔, 위치 x, y좌표, 너비, 높이)
        screen.blit(pause_surface, (0, 0))

        single_button.draw(screen, (0, 0, 0))
        pvp_button.draw(screen, (0, 0, 0))
        hard_button.draw(screen, (0, 0, 0))
        hard_training_button.draw(screen, (0, 0, 0))
        multi_training_button.draw(screen, (0, 0, 0))
        back_button.draw(screen, (0, 0, 0))

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

                if hard_training_button.isOver_2(pos):
                    hard_training_button.image = clicked_hard_training_button_image
                else:
                    hard_training_button.image = hard_training_button_image

                if multi_training_button.isOver_2(pos):
                    multi_training_button.image = clicked_multi_training_button_image
                else:
                    multi_training_button.image = multi_training_button_image

                if back_button.isOver(pos):
                    back_button.image = clicked_back_button_image
                else:
                    back_button.image = back_button_image

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if single_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    previous_time = pygame.time.get_ticks()
                    ui_variables.intro_sound.stop()
                    pygame.mixer.music.play(-1)
                    start = True
                    initialize = True
                    select_mode = False

                    # pygame.mixer.music.play(-1) #play(-1) = 노래 반복재생
                    # ui_variables.intro_sound.stop()
                if pvp_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    ui_variables.intro_sound.stop()
                    pygame.mixer.music.play(-1)
                    pvp = True
                    initialize = True
                    select_mode = False
                if hard_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    ui_variables.intro_sound.stop()
                    pygame.mixer.music.play(-1)
                    hard = True
                    initialize = True
                    select_mode = False
                if hard_training_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    hard_training_info = True
                    training_status = True
                    ui_variables.intro_sound.stop()
                    pygame.mixer.music.play(-1)
                    initialize = True
                    select_mode = False
                if multi_training_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    multi_training_info = True
                    training_status = True
                    ui_variables.intro_sound.stop()
                    pygame.mixer.music.play(-1)
                    initialize = True
                    select_mode = False
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    select_mode = False
                    initialize = False

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate - 0.1) < (board_height / board_width) < (board_rate + 0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width * board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)  # 블록 크기 고정
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)

    elif leader_board:
        screen.fill(ui_variables.real_white)
        draw_image(screen, background_image, board_width * 0.5, board_height *
                   0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
        pause_surface = screen.convert_alpha()  # 투명 가능하도록
        pause_surface.fill((0, 0, 0, 0))  # 투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(
            board_width), int(board_height)])  # (screen, 색깔, 위치 x, y좌표, 너비, 높이)
        screen.blit(pause_surface, (0, 0))

        draw_image(screen, scoreboard_board_image, board_width * 0.5, board_height * 0.5,
                   int(board_height * 1.3), board_height)

        easy_mode_text = ui_variables.h2_b.render(
            "EASY MODE:", 1, ui_variables.yellow)
        hard_mode_text = ui_variables.h2_b.render(
            "HARD MODE:", 1, ui_variables.yellow)
        screen.blit(easy_mode_text, (board_width * 0.2, board_height * 0.2))
        screen.blit(hard_mode_text, (board_width * 0.55, board_height * 0.2))

        back_button.draw(screen, (0, 0, 0))

        # render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
        # easy mode
        leader_1 = ui_variables.h2_b.render(
            '1st ' + leaders[0][0] + ' ' + str(leaders[0][1]), 1, ui_variables.white)
        leader_2 = ui_variables.h2_b.render(
            '2nd ' + leaders[1][0] + ' ' + str(leaders[1][1]), 1, ui_variables.white)
        leader_3 = ui_variables.h2_b.render(
            '3rd ' + leaders[2][0] + ' ' + str(leaders[2][1]), 1, ui_variables.white)
        screen.blit(leader_1, (board_width * 0.2,
                    board_height * 0.35))  # 위치 비율 고정
        screen.blit(leader_2, (board_width * 0.2,
                    board_height * 0.5))  # 위치 비율 고정
        screen.blit(leader_3, (board_width * 0.2,
                    board_height * 0.65))  # 위치 비율 고정

        # hard mode
        leader_1 = ui_variables.h2_b.render(
            '1st ' + leaders_hard[0][0] + ' ' + str(leaders_hard[0][1]), 1, ui_variables.white)
        leader_2 = ui_variables.h2_b.render(
            '2nd ' + leaders_hard[1][0] + ' ' + str(leaders_hard[1][1]), 1, ui_variables.white)
        leader_3 = ui_variables.h2_b.render(
            '3rd ' + leaders_hard[2][0] + ' ' + str(leaders_hard[2][1]), 1, ui_variables.white)
        screen.blit(leader_1, (board_width * 0.55,
                    board_height * 0.35))  # 위치 비율 고정
        screen.blit(leader_2, (board_width * 0.55,
                    board_height * 0.5))  # 위치 비율 고정
        screen.blit(leader_3, (board_width * 0.55,
                    board_height * 0.65))  # 위치 비율 고정

        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver_2(pos):
                    back_button.image = clicked_back_button_image
                else:
                    back_button.image = back_button_image

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    leader_board = False
            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)

    # 트레이닝 모드 시작 시 나오는 설명 화면
    elif training_status:
        if hard_training_info:
            screen.fill(ui_variables.real_white)

            draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                       0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
            draw_hardboard(next_mino1, next_mino2, hold_mino,
                           score, remaining_time, line_count)

            # 화면 회색으로 약간 불투명하게
            pause_surface = screen.convert_alpha()  # 투명 가능하도록
            pause_surface.fill((0, 0, 0, 0))  # 투명한 검정색으로 덮기
            pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(
                board_width), int(board_height)])  # (screen, 색깔, 위치 x, y좌표, 너비, 높이)
            screen.blit(pause_surface, (0, 0))

            draw_image(screen, hard_training_start_image, board_width * 0.5, board_height *
                       0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)

        if multi_training_info:
            draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P,
                            current_key, current_key_2P)
            # 화면 회색으로 약간 불투명하게
            pause_surface = screen.convert_alpha()  # 투명 가능하도록
            pause_surface.fill((0, 0, 0, 0))  # 투명한 검정색으로 덮기
            pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(
                board_width), int(board_height)])  # (screen, 색깔, 위치 x, y좌표, 너비, 높이)
            screen.blit(pause_surface, (0, 0))

            draw_image(screen, multi_training_start_image, board_width * 0.5, board_height *
                       0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)

        if help_status == True:
            # pause_surface = screen.convert_alpha()  # 투명 가능하도록
            # pause_surface.fill((0, 0, 0, 0))  # 투명한 검정색으로 덮기
            # pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(
            #     board_width), int(board_height)])  # (screen, 색깔, 위치 x, y좌표, 너비, 높이)

            draw_image(screen, help_board_image, board_width * 0.5, board_height * 0.5,
                       int(board_width * 0.8), int(board_height * 0.9))  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
            back_button2.draw(screen, (0, 0, 0))
        
        # if help_status == False:

        
        # training_help_button.draw(screen, (0,0,0))
        
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True

            # 설명 화면에서 enter만 누르면 게임 시작
            elif event.type == KEYDOWN:
                if hard_training_info:
                    if event.key == K_RETURN:
                        ui_variables.click_sound.play()
                        training_status = False
                        hard_training = True
                if multi_training_info:
                    if event.key == K_RETURN:
                        ui_variables.click_sound.play()
                        training_status = False
                        multi_training = True
            

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate + 0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)  # 블록 크기비율 고정
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)

    elif screen_setting:
        screen.fill(ui_variables.pinkpurple)
        draw_image(screen, background_image, board_width * 0.5, board_height *
                   0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
        select_mode_button.draw(screen, (0, 0, 0))
        setting_button.draw(screen, (0, 0, 0))
        score_board_button.draw(screen, (0, 0, 0))
        quit_button.draw(screen, (0, 0, 0))
        # 배경 약간 어둡게
        leaderboard_icon.draw(screen, (0, 0, 0))
        pause_surface = screen.convert_alpha()  # 투명 가능하도록
        pause_surface.fill((0, 0, 0, 0))  # 투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(
            board_width), int(board_height)])  # (screen, 색깔, 위치 x, y좌표, 너비, 높이)

        screen.blit(pause_surface, (0, 0))

        draw_image(screen, setting_board_image, board_width * 0.5, board_height * 0.5,
                   int(board_height * 1.3), board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)

        background1_check_button.draw(screen, (0, 0, 0))
        background2_check_button.draw(screen, (0, 0, 0))
        background3_check_button.draw(screen, (0, 0, 0))
        back_button.draw(screen, (0, 0, 0))

        Background1_text = ui_variables.h5.render(
            'HongKong', 1, ui_variables.white)
        Background2_text = ui_variables.h5.render(
            'NewYork', 1, ui_variables.white)
        Background3_text = ui_variables.h5.render(
            'London', 1, ui_variables.white)
        screen.blit(Background1_text, (board_width * 0.47,
                    board_height * 0.33))  # 위치 비율 고정
        screen.blit(Background2_text, (board_width * 0.47,
                    board_height * 0.52))  # 위치 비율 고정
        screen.blit(Background3_text, (board_width * 0.47,
                    board_height * 0.73))  # 위치 비율 고정

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)  # 0.3초로 설정
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
                if background1_check_button.isOver(pos):
                    gamebackground_image = 'assets/images/background_hongkong.png'
                    # 클릭한 이미지에만 체크 표시
                    background2_check_button.image = background2_image
                    background3_check_button.image = background3_image
                    background1_check_button.image = clicked_background1_image

                if background2_check_button.isOver(pos):
                    gamebackground_image = 'assets/images/background_nyc.png'
                    # 클릭한 이미지에만 체크 표시
                    background1_check_button.image = background1_image
                    background3_check_button.image = background3_image
                    background2_check_button.image = clicked_background2_image

                if background3_check_button.isOver(pos):
                    gamebackground_image = 'assets/images/background_uk.png'
                    # 클릭한 이미지에만 체크 표시
                    background1_check_button.image = background1_image
                    background2_check_button.image = background2_image
                    background3_check_button.image = clicked_background3_image
                pygame.display.update()

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate - 0.1) < (board_height / board_width) < (board_rate + 0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width * board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)  # 블록 크기 고정
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)

    elif volume_setting:
        # 배경 약간 어둡게
        leaderboard_icon.draw(screen, (0, 0, 0))  # rgb(0,0,0) = 검정색#
        pause_surface = screen.convert_alpha()  # 투명 가능하도록
        pause_surface.fill((0, 0, 0, 0))  # 투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(
            board_width), int(board_height)])  # (screen, 색깔, 위치 x, y좌표, 너비, 높이)
        screen.blit(pause_surface, (0, 0))  # 위치 비율 고정

        # draw_image(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        draw_image(screen, setting_board_image, board_width * 0.5,
                   board_height * 0.5, int(board_height * 1.3), board_height)
        draw_image(screen, number_board, board_width * 0.35, board_height *
                   0.53, int(board_width * 0.09), int(board_height * 0.1444))
        draw_image(screen, number_board, board_width * 0.35, board_height *
                   0.73, int(board_width * 0.09), int(board_height * 0.1444))
        mute_button.draw(screen, (0, 0, 0))  # rgb(0,0,0) = 검정색#

        effect_plus_button.draw(screen, (0, 0, 0))
        effect_minus_button.draw(screen, (0, 0, 0))
        sound_plus_button.draw(screen, (0, 0, 0))
        sound_minus_button.draw(screen, (0, 0, 0))
        #음소거 추가#
        effect_sound_on_button.draw(screen, (0, 0, 0))
        music_sound_on_button.draw(screen, (0, 0, 0))

        # BGM 선택 버튼 3개
        BGM1_sound_on_button.draw(screen, (0, 0, 0))
        BGM2_sound_on_button.draw(screen, (0, 0, 0))
        BGM3_sound_on_button.draw(screen, (0, 0, 0))
        back_button.draw(screen, (0, 0, 0))

        # render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
        music_volume_text = ui_variables.h5.render(
            'Music Volume', 1, ui_variables.white)
        effect_volume_text = ui_variables.h5.render(
            'Effect Volume', 1, ui_variables.white)
        screen.blit(music_volume_text, (board_width *
                    0.3, board_height * 0.4))  # 위치 비율 고정
        screen.blit(effect_volume_text, (board_width *
                    0.3, board_height * 0.6))  # 위치 비율 고정

        music_volume_text = ui_variables.h5.render(
            'Music On/Off', 1, ui_variables.white)
        effect_volume_text = ui_variables.h5.render(
            'Effect On/Off', 1, ui_variables.white)
        screen.blit(music_volume_text, (board_width *
                    0.5, board_height * 0.4))  # 위치 비율 고정
        screen.blit(effect_volume_text, (board_width *
                    0.5, board_height * 0.6))  # 위치 비율 고정

        music_volume_size_text = ui_variables.h4.render(
            str(music_volume), 1, ui_variables.grey_1)
        effect_volume_size_text = ui_variables.h4.render(
            str(effect_volume), 1, ui_variables.grey_1)
        screen.blit(music_volume_size_text, (board_width *
                    0.33, board_height * 0.5))  # 위치 비율 고정
        screen.blit(effect_volume_size_text, (board_width *
                    0.33, board_height * 0.7))  # 위치 비율 고정

        BGM1_text = ui_variables.h5.render('BGM1', 1, ui_variables.white)
        BGM2_text = ui_variables.h5.render('BGM2', 1, ui_variables.white)
        BGM3_text = ui_variables.h5.render('BGM3', 1, ui_variables.white)

        screen.blit(BGM1_text, (board_width * 0.65,
                    board_height * 0.3))  # 위치 비율 고정
        screen.blit(BGM2_text, (board_width * 0.65,
                    board_height * 0.5))  # 위치 비율 고정
        screen.blit(BGM3_text, (board_width * 0.65,
                    board_height * 0.7))  # 위치 비율 고정

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)  # 0.3초로 설정

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

                if mute_button.image == mute_button_image:
                    if mute_button.isOver(pos):
                        mute_button.image = clicked_mute_button_image
                    else:
                        mute_button.image = mute_button_image
                if mute_button.image == clicked_mute_button_image:
                    if mute_button.isOver(pos):
                        mute_button.image = clicked_mute_button_image
                    else:
                        mute_button.image = mute_button_image

                if mute_button.image == default_button_image:
                    if mute_button.isOver(pos):
                        mute_button.image = clicked_default_button_image
                    else:
                        mute_button.image = default_button_image
                if mute_button.image == clicked_default_button_image:
                    if mute_button.isOver(pos):
                        mute_button.image = clicked_default_button_image
                    else:
                        mute_button.image = default_button_image

                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    pygame.mixer.music.stop()
                    ui_variables.intro_sound.play()
                    volume_setting = False
                if sound_plus_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if music_volume >= 10:  # 음량 최대크기
                        music_volume = 10
                    else:
                        music_sound_on_button.image = sound_on_button_image
                        music_volume += 1
                if sound_minus_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if music_volume <= 0:  # 음량 최소크기
                        music_volume = 0
                        music_sound_on_button.image = sound_off_button_image
                    else:
                        if music_volume == 1:
                            music_sound_on_button.image = sound_off_button_image
                            music_volume -= 1
                        else:
                            music_sound_on_button.image = sound_on_button_image
                            music_volume -= 1
                if effect_plus_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if effect_volume >= 10:  # 음량 최대크기
                        effect_volume = 10
                    else:
                        effect_sound_on_button.image = sound_on_button_image
                        effect_volume += 1
                if effect_minus_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if effect_volume <= 0:  # 음량 최소크기
                        effect_volume = 0
                        effect_sound_on_button.image = sound_off_button_image
                    else:
                        if effect_volume == 1:
                            effect_sound_on_button.image = sound_off_button_image
                            effect_volume -= 1
                        else:
                            effect_sound_on_button.image = sound_on_button_image
                            effect_volume -= 1
                #BGM 선택 기능 추가#
                # BGM버튼을 누르면 인트로음악은 멈추고 해당 BGM재생됨 (Back버튼을 눌러 뒤로가기 전까지 계속 재생)
                if BGM1_sound_on_button.isOver(pos):
                    #ui_variables.intro_sound.("assets/sounds/BGM2.wav")#
                    # 클릭한 버튼만 체크 표시되도록
                    BGM2_sound_on_button.image = backgroundmusic_select_image
                    BGM3_sound_on_button.image = backgroundmusic_select_image
                    BGM1_sound_on_button.image = clicked_backgroundmusic_select_image
                    ui_variables.intro_sound.stop()
                    pygame.mixer.music.stop()
                    selected_bgm = "assets/sounds/BGM1.wav"
                    pygame.mixer.music.load(selected_bgm)
                    pygame.mixer.music.play()
                if BGM2_sound_on_button.isOver(pos):
                    #ui_variables.intro_sound.("assets/sounds/BGM2.wav")#
                    # 클릭한 버튼만 체크 표시되도록
                    BGM1_sound_on_button.image = backgroundmusic_select_image
                    BGM3_sound_on_button.image = backgroundmusic_select_image
                    BGM2_sound_on_button.image = clicked_backgroundmusic_select_image
                    ui_variables.intro_sound.stop()
                    pygame.mixer.music.stop()
                    selected_bgm = "assets/sounds/BGM2.wav"
                    pygame.mixer.music.load(selected_bgm)
                    pygame.mixer.music.play()
                if BGM3_sound_on_button.isOver(pos):
                    #ui_variables.intro_sound.("assets/sounds/BGM2.wav")#
                    # 클릭한 버튼만 체크 표시되도록
                    BGM1_sound_on_button.image = backgroundmusic_select_image
                    BGM2_sound_on_button.image = backgroundmusic_select_image
                    BGM3_sound_on_button.image = clicked_backgroundmusic_select_image
                    ui_variables.intro_sound.stop()
                    pygame.mixer.music.stop()
                    selected_bgm = "assets/sounds/BGM3.wav"
                    pygame.mixer.music.load(selected_bgm)
                    pygame.mixer.music.play()

                #음소거 추가#
                if music_sound_on_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if music_volume == 0:
                        music_volume = 5  # 중간 음량으로
                        music_sound_on_button.image = sound_on_button_image
                    else:
                        music_volume = 0
                        music_sound_off_button.draw(
                            screen, (0, 0, 0))  # rgb(0,0,0) = 검정색
                        music_sound_on_button.image = sound_off_button_image
                if effect_sound_on_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if effect_volume == 0:
                        effect_volume = 5  # 중간 음량으로
                        effect_sound_on_button.image = sound_on_button_image
                    else:
                        effect_volume = 0
                        effect_sound_off_button.draw(screen, (0, 0, 0))
                        effect_sound_on_button.image = sound_off_button_image
                if mute_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if (effect_volume == 0) and (music_volume == 0):
                        music_volume = 5  # 중간 음량으로
                        effect_volume = 5  # 중간 음량으로
                        mute_button.image = mute_button_image
                    else:
                        music_volume = 0  # 최소 음량으로
                        effect_volume = 0  # 최소 음량으로
                        # default_button.draw(screen, (0, 0, 0))
                        mute_button.image = default_button_image

                set_volume()

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate - 0.1) < (board_height / board_width) < (board_rate + 0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width * board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)  # 블록 크기 고정
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)

    elif setting:
        select_mode_button.draw(screen, (0, 0, 0))
        setting_button.draw(screen, (0, 0, 0))
        score_board_button.draw(screen, (0, 0, 0))
        quit_button.draw(screen, (0, 0, 0))
        # 배경 약간 어둡게
        leaderboard_icon.draw(screen, (0, 0, 0))
        pause_surface = screen.convert_alpha()  # 투명 가능하도록
        pause_surface.fill((0, 0, 0, 0))  # 투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(
            board_width), int(board_height)])  # (screen, 색깔, 위치 x, y좌표, 너비, 높이)
        screen.blit(pause_surface, (0, 0))

        draw_image(screen, setting_board_image, board_width * 0.5, board_height * 0.5,
                   int(board_height * 1.3), board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)

        screen_icon.draw(screen, (0, 0, 0))  # rgb(0,0,0) = 검정색
        volume_icon.draw(screen, (0, 0, 0))

        back_button.draw(screen, (0, 0, 0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)  # 0.3초로 설정
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
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)  # 블록 크기 고정
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)

    # Start screen
    else:
        # 초기화
        if initialize:
            set_initial_values()
        initialize = False

        # 인트로 사운드 플레이
        ui_variables.intro_sound.play()

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
                    initialize = True
                    # #pygame.mixer.music.play(-1) #play(-1) = 노래 반복재생
                    # #ui_variables.intro_sound.stop()
                if setting_button.isOver(pos):
                    ui_variables.click_sound.play()
                    setting = True
                if score_board_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    leader_board = True
                if quit_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    done = True

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate - 0.1) < (board_height / board_width) < (board_rate + 0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width * board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)  # 블록 크기 고정
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)

                '''
                if single_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    previous_time = pygame.time.get_ticks()
                    start = True
                    initialize = True
                    pygame.mixer.music.play(-1) #play(-1) = 노래 반복재생
                    ui_variables.intro_sound.stop()
                if pvp_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    pvp = True
                    initialize = True
                    pygame.mixer.music.play(-1)
                    ui_variables.intro_sound.stop()
                if gravity_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    start = True
                    gravity_mode = True
                    initialize = True
                    pygame.mixer.music.play(-1)
                    ui_variables.intro_sound.stop()
                if timeattack_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    start = True
                    time_attack = True
                    initialize = True
                    pygame.mixer.music.play(-1)
                    ui_variables.intro_sound.stop()
                if leaderboard_icon.isOver(pos):
                    ui_variables.click_sound.play()
                    leader_board = True
                if setting_icon.isOver(pos):
                    ui_variables.click_sound.play()
                    setting = True

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
        draw_image(screen, background_image, board_width * 0.5, board_height *
                   0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)

        # 버튼그리기
        select_mode_button.draw(screen, (0, 0, 0))
        setting_button.draw(screen, (0, 0, 0))
        score_board_button.draw(screen, (0, 0, 0))
        quit_button.draw(screen, (0, 0, 0))

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
