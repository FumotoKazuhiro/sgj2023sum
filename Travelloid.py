# ゲームタイトル
# <Travelloid>
# 作：麓一博

import pygame
from pygame.locals import *
import random
import time

# event time
ev_time = 15
start_time = 0
elapsed_time = 0

GAMEOVER_STATE = False

# ゲーム画面のサイズ
WIDTH = 640
HEIGHT = 480

# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GLAY = (192, 192, 192)

# パドルのサイズと速度
PADDLE_WIDTH = 80
PADDLE_HEIGHT = 10
PADDLE_SPEED = 6

# ボールのサイズと速度
BALL_RADIUS = 8
BALL_SPEED = 3

# ブロックの設定
BLOCK_WIDTH = 60
BLOCK_HEIGHT = 20
BLOCK_ROWS = 5
BLOCK_COLS = 9
BLOCK_COLORS = [GREEN, BLUE, RED, RED, BLUE]

# テキストの設定
text_content = "Travelloid 15sec"
font_size = 36
font_color = (255, 255, 255)  # 白色
fade_speed = 2  # フェードアウトの速度（大きいほど早い）

# ランダム移動の設定
# 二次元配列のサイズ
rows = BLOCK_ROWS * BLOCK_COLS
cols = 2
# 二次元配列を生成
matrix = [[random.choice([-2, 2]) for _ in range(cols)] for _ in range(rows)]

# ブロック回転の数値
rotation_angle = 0
rotation_speed = 2  # 回転速度（度数法）

# 初期化
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ブロック崩し[旅情編]")
clock = pygame.time.Clock()

# フェードアウト用のカウンタ
fade_counter = 0

# フォントの設定
font = pygame.font.Font(None, 40)

# タイマーの描画位置と内容
timer_position = (WIDTH // 2, 14)
timer_content = ""

# 点数の描画位置と内容
score_position = (WIDTH, 14)
score_content = ""
score = 0

# タイトルテキストの描画
text_surface = font.render(text_content, True, font_color)
text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# ブロック画像の読みこみ
blockbit = pygame.image.load("block_way.png")

# 背景画像の読み込み
image1 = pygame.image.load("bg0001.png").convert()
image2 = pygame.image.load("bg0002.png").convert()
image3 = pygame.image.load("bg0003.png").convert()
image4 = pygame.image.load("bg0004.png").convert()
image5 = pygame.image.load("bg0005.png").convert()

gameover_img = pygame.image.load("GAMEOVER.png").convert()

# 背景画像リスト
background_images = [image1, image2, image3, image4, image5]
current_image = 0

# アニメーション速度（画像の切り替え間隔）
animation_speed = 2  # フレームごとに切り替える

# FPS（フレームレート）
FPS = 60

# パドルの初期位置
paddle_x = (WIDTH - PADDLE_WIDTH) // 2
paddle_y = HEIGHT - PADDLE_HEIGHT - 10

# ボールの初期位置と速度
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = random.choice([-1, 1]) * BALL_SPEED
ball_dy = -BALL_SPEED

# ボールの状態
ball_active = False  # ボールが発射されたかどうかを管理するフラグ

# ブロックの初期配置
blocks = []
for row in range(BLOCK_ROWS):
    for col in range(BLOCK_COLS):
        block_x = 1 + col * (BLOCK_WIDTH + 2)
        block_y = 30 + row * (BLOCK_HEIGHT + 2)
        blocks.append(pygame.Rect(block_x, block_y, BLOCK_WIDTH, BLOCK_HEIGHT))

# ゲームループ
running = True
while running:
    
    #screen.blit(background_image, (0, 0))
    #screen.fill(BLACK)
    
    # 画像の切り替え
    if pygame.time.get_ticks() % (FPS * animation_speed) == 0:
        current_image = (current_image + 1) % len(background_images)

    # 画面の描画
    screen.blit(background_images[current_image], (0, 0))

    # イベント処理
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                ball_active = True
                start_time = time.time()
            if event.key == K_ESCAPE and GAMEOVER_STATE:
                running = False

    # パドルの移動
    keys = pygame.key.get_pressed()
    if keys[K_LEFT] and paddle_x > 0:
        paddle_x -= PADDLE_SPEED
    if keys[K_RIGHT] and paddle_x < WIDTH - PADDLE_WIDTH:
        paddle_x += PADDLE_SPEED
    
    if not ball_active:
        # ボールをパドルの上に固定
        ball_x = paddle_x + PADDLE_WIDTH // 2
        ball_y = paddle_y - BALL_RADIUS
    else:
        elapsed_time = time.time() - start_time
        #if elapsed_time == ev_time: print(elapsed_time)
        # ボールの移動
        ball_x += ball_dx
        ball_y += ball_dy
        
        # ボールの反射（壁との衝突判定）
        if ball_x < 0 or ball_x > WIDTH - BALL_RADIUS:
            ball_dx *= -1
        if ball_y < 0:
            ball_dy *= -1
        
        # ボールの反射（パドルとの衝突判定）
        ball_rect = pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        paddle_rect = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        if ball_rect.colliderect(paddle_rect):
            ball_dy *= -1
        
        # ボールの反射（ブロックとの衝突判定）
        for block in blocks:
            if ball_rect.colliderect(block):
                blocks.remove(block)
                ball_dy *= -1
                score += 1
                break
        
        # ゲームオーバー判定
        if ball_y > HEIGHT or int(elapsed_time) == 48:
            #print('YOUR SCORE', score)
            # ゲームオーバーの状態を変更
            GAMEOVER_STATE = True
            # ゲームオーバー画面を表示
            screen.blit(gameover_img, (0, 0))
            # スコアを表示
            screen.blit(score_render, score_rect)
            # 一回だけアップデートをかけて・・・
            pygame.display.update()
            #running = False

    # テキストをフェードアウトさせる
    alpha = max(255 - fade_counter * fade_speed, 0)
    text_surface.set_alpha(alpha)
    fade_counter += 1

    # テキストを描画
    screen.blit(text_surface, text_rect)

    # タイマーを描画
    if elapsed_time <= ev_time:
        timer_content = str(int(elapsed_time))
    else:
        timer_content = "journey mode! " + str(int(elapsed_time))
    timer_render = font.render(timer_content, True, WHITE)
    if int(elapsed_time) >= 38:
        timer_render = font.render(timer_content, True, YELLOW)
    if int(elapsed_time) >= 43:
        timer_render = font.render(timer_content, True, RED)
    timer_rect = timer_render.get_rect(center=timer_position)
    screen.blit(timer_render, timer_rect)

    # スコアを描画
    score_content = str(score)
    score_render = font.render(score_content, True, WHITE)
    score_rect = score_render.get_rect()
    score_rect.midright = (score_position[0], score_position[1])
    screen.blit(score_render, score_rect)

    # オブジェクトを描画
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), BALL_RADIUS)

    for block in blocks:
        if elapsed_time <= ev_time:
            pygame.draw.rect(screen, BLOCK_COLORS[blocks.index(block) // BLOCK_COLS], block)
        else:
            # block.move_ip(1,1)
            block_xc = block.center[0]
            block_yc = block.center[1]
            block.w = BLOCK_WIDTH // 2
            # ブロックの反射（壁との衝突判定）
            if block_xc < 0 or block_xc > WIDTH - BLOCK_WIDTH // 2:
                matrix[blocks.index(block)][0] *= -1
            if block_yc < 0 or block_yc > HEIGHT - BLOCK_HEIGHT // 4:
                matrix[blocks.index(block)][1] *= -1
            block.move_ip(matrix[blocks.index(block)][0], matrix[blocks.index(block)][1])
            screen.blit(blockbit, block)
            #pygame.draw.rect(screen, GLAY, block)
    
    if GAMEOVER_STATE == False:
        pygame.display.update()
    #pygame.display.flip()
    clock.tick(FPS)

# ゲーム終了
pygame.quit()
