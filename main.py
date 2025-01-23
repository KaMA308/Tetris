import pygame
import copy
from random import choice


def main():
    pygame.init()

    w, h = 10, 20
    cell = 35

    size = width, height = 600, 800
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Tetris')

    play_zone = pygame.Surface((350, 700))
    play_zone.fill((18, 28, 89))

    field = [[0 for i in range(w)] for j in range(h)]
    print(field)

    shape_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                 [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                 [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                 [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                 [(0, 0), (0, -1), (0, 1), (-1, -1)],
                 [(0, 0), (0, -1), (0, 1), (1, -1)],
                 [(0, 0), (0, -1), (0, 1), (-1, 0)]]

    shapes = [[pygame.Rect(x + w // 2, y + 1, 1, 1) for x, y in sha_pos] for sha_pos in shape_pos]

    shape_rect = pygame.Rect(0, 0, cell - 2, cell - 2)
    shape = copy.deepcopy(choice(shapes))

    speed = 100
    count_speed = 0
    lim_speed = 1600

    net = [pygame.Rect(x * cell, y * cell, cell, cell) for x in range(w) for y in range(h)]

    clock = pygame.time.Clock()
    FPS = 60

    running = True
    while running:
        pos = 0
        screen.fill((43, 66, 158))
        screen.blit(play_zone, (50, 50))
        play_zone.fill((18, 28, 89))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pos = -1
                elif event.key == pygame.K_RIGHT:
                    pos = 1
                elif event.key == pygame.K_DOWN:
                    speed = 400

        shape_old = copy.deepcopy(shape)

        for i in range(4):
            shape[i].x += pos
            if shape[i].x < 0 or shape[i].x > w - 1:
                shape = copy.deepcopy(shape_old)
                break

        count_speed += speed

        if count_speed >= lim_speed:
            count_speed = 0
            for i in range(4):
                shape[i].y += 1
                if shape[i].y > h - 1 or field[shape[i].y][shape[i].x]:
                    for i in range(4):
                        field[shape_old[i].y][shape_old[i].x] = pygame.Color('White')
                    shape = copy.deepcopy(choice(shapes))
                    speed = 100
                    break

        for i in net:
            pygame.draw.rect(play_zone, (80, 80, 80), i, 1)

        for i in range(4):
            shape_rect.x = shape[i].x * cell
            shape_rect.y = shape[i].y * cell
            pygame.draw.rect(play_zone, (255, 255, 255), shape_rect)

        for y, raw in enumerate(field):
            for x, col in enumerate(raw):
                if col:
                    shape_rect.x, shape_rect.y = x * cell, y * cell
                    pygame.draw.rect(play_zone, col, shape_rect)
                    print(field)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
