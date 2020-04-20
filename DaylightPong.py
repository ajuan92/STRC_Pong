# Developer : Hamdy Abou El Anein
from multiprocessing import Process, Pipe, Queue

import PongConst as PConst
import random
import pygame
import sys
import time as tm
from pygame import *
from easygui import *
from queue import Queue


WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
ball_pos = [0, 0]
ball_vel = [0, 0]
paddle1_vel = 0
paddle2_vel = 0
l_score = 0
r_score = 0


def ball_init(right):
    global ball_pos, ball_vel
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    horz = random.randrange(2, 4)
    vert = random.randrange(1, 3)

    if right == False:
        horz = -horz

    ball_vel = [horz, -vert]


def init():
    # these are floats
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, l_score, r_score
    global score1, score2  # these are ints
    paddle1_pos = [HALF_PAD_WIDTH - 1, HEIGHT // 2]
    paddle2_pos = [WIDTH + 1 - HALF_PAD_WIDTH, HEIGHT // 2]
    l_score = 0
    r_score = 0
    if random.randrange(0, 2) == 0:
        ball_init(True)
    else:
        ball_init(False)


def draw(canvas):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score

    canvas.fill(BLACK)
    pygame.draw.line(canvas, WHITE, [WIDTH // 2, 0], [WIDTH // 2, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(
        canvas, WHITE, [WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1
    )
    pygame.draw.circle(canvas, WHITE, [WIDTH // 2, HEIGHT // 2], 70, 1)

    if paddle1_pos[1] > HALF_PAD_HEIGHT and paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HALF_PAD_HEIGHT and paddle1_vel > 0:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel < 0:
        paddle1_pos[1] += paddle1_vel

    if paddle2_pos[1] > HALF_PAD_HEIGHT and paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HALF_PAD_HEIGHT and paddle2_vel > 0:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle2_vel < 0:
        paddle2_pos[1] += paddle2_vel

    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])

    pygame.draw.circle(canvas, ORANGE, ball_pos, 20, 0)
    pygame.draw.polygon(
        canvas,
        GREEN,
        [
            [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT],
            [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT],
            [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT],
            [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT],
        ],
        0,
    )
    pygame.draw.polygon(
        canvas,
        GREEN,
        [
            [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT],
            [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT],
            [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT],
            [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT],
        ],
        0,
    )

    if int(ball_pos[1]) <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    if int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]

    if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(ball_pos[1]) in range(
        paddle1_pos[1] - HALF_PAD_HEIGHT, paddle1_pos[1] + HALF_PAD_HEIGHT, 1
    ):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
        r_score += 1
        ball_init(True)

    if int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(
        ball_pos[1]
    ) in range(paddle2_pos[1] - HALF_PAD_HEIGHT, paddle2_pos[1] + HALF_PAD_HEIGHT, 1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
        l_score += 1
        ball_init(False)

    myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
    label1 = myfont1.render("Score " + str(l_score), 1, (255, 255, 0))
    canvas.blit(label1, (50, 20))

    myfont2 = pygame.font.SysFont("Comic Sans MS", 20)
    label2 = myfont2.render("Score " + str(r_score), 1, (255, 255, 0))
    canvas.blit(label2, (470, 20))


def keydown(event, Pipe_Data):
    global paddle1_vel, paddle2_vel

    if event.key == K_UP:
        if PConst.ID_CURRENT_PLAYER == PConst.PLAYER_1_ID:
            paddle1_vel = -8
            Pipe_Data[PConst.PALETA1_TYPE] = event.type
            Pipe_Data[PConst.PALETA1_KEY] = event.key
        else:
            paddle2_vel = -8
            Pipe_Data[PConst.PALETA2_TYPE] = event.type
            Pipe_Data[PConst.PALETA2_KEY] = event.key
    elif event.key == K_DOWN:
        if PConst.ID_CURRENT_PLAYER == PConst.PLAYER_1_ID:
            paddle1_vel = 8
            Pipe_Data[PConst.PALETA1_TYPE] = event.type
            Pipe_Data[PConst.PALETA1_KEY] = event.key
        else:
            paddle2_vel = 8
            Pipe_Data[PConst.PALETA2_TYPE] = event.type
            Pipe_Data[PConst.PALETA2_KEY] = event.key


def keyup(event, Pipe_Data):
    global paddle1_vel, paddle2_vel

    if event.key in (K_UP, K_DOWN):
        if PConst.ID_CURRENT_PLAYER == PConst.PLAYER_1_ID:
            paddle1_vel = 0
            Pipe_Data[PConst.PALETA1_TYPE] = event.type
            Pipe_Data[PConst.PALETA1_KEY] = event.key
        else:
            paddle2_vel = 0
            Pipe_Data[PConst.PALETA2_TYPE] = event.type
            Pipe_Data[PConst.PALETA2_KEY] = event.key


def Remotkeydown(Pipe_Data):
    global paddle1_vel, paddle2_vel

    if PConst.ID_OTHE_PLAYER == PConst.PLAYER_2_ID:
        if Pipe_Data[PConst.PALETA2_KEY] == K_UP:
            paddle2_vel = -8
        elif Pipe_Data[PConst.PALETA2_KEY] == K_DOWN:
            paddle2_vel = 8
    else:
        if Pipe_Data[PConst.PALETA1_KEY] == K_UP:
            paddle1_vel = -8
        elif Pipe_Data[PConst.PALETA1_KEY] == K_DOWN:
            paddle1_vel = 8


def Remotkeyup(Pipe_Data):
    global paddle1_vel, paddle2_vel

    if PConst.ID_OTHE_PLAYER == PConst.PLAYER_2_ID:
        if Pipe_Data[PConst.PALETA2_KEY] in (K_UP, K_DOWN):
            paddle2_vel = 0
    else:
        if Pipe_Data[PConst.PALETA1_KEY] in (K_UP, K_DOWN):
            paddle1_vel = 0


def PongGameMain(Pipe_Data):

    print("Waiting Other Player")
    print("Start_Game")
    Count = 0

    while Pipe_Data[PConst.ESTADO_CONECCION] != 1 or Count >= 50000:
        #print("Waiting Other Player")
        tm.sleep(0.010)
        Count = Count + 1

    pygame.init()
    fps = pygame.time.Clock()

    window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    pygame.display.set_caption("Daylight Pong")

    init()

    while True:

        draw(window)

        if PConst.ID_OTHE_PLAYER == PConst.PLAYER_2_ID:
            if Pipe_Data[PConst.PALETA2_TYPE] == KEYDOWN:
                Remotkeydown(Pipe_Data)
            elif Pipe_Data[PConst.PALETA2_TYPE] == KEYUP:
                Remotkeyup(Pipe_Data)
        else:
            if Pipe_Data[PConst.PALETA1_TYPE] == KEYDOWN:
                Remotkeydown(Pipe_Data)
            elif Pipe_Data[PConst.PALETA1_TYPE] == KEYUP:
                Remotkeyup(Pipe_Data)

        for event in pygame.event.get():

            if event.type == KEYDOWN:
                keydown(event, Pipe_Data)
            elif event.type == KEYUP:
                keyup(event, Pipe_Data)
            elif event.type == QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
        pygame.display.update()
        fps.tick(60)


if __name__ == "__main__":
    PongGameMain()
