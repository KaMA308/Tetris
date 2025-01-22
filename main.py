import pygame


def main():
    pygame.init()

    w, h = 10, 20
    cell = 35

    size = width, height = 600, 800
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Tetris')

    play_zone = pygame.Surface((350, 700))
    play_zone.fill((18, 28, 89))



    shape_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                 [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                 [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                 [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                 [(0, 0), (0, -1), (0, 1), (-1, -1)],
                 [(0, 0), (0, -1), (0, 1), (1, -1)],
                 [(0, 0), (0, -1), (0, 1), (-1, 0)]]

    shapes = [[pygame.Rect(x + w // 2, y + 1, 1, 1) for x, y in sha_pos] for sha_pos in shape_pos]
    shape_rect = pygame.Rect(0, 0, cell - 2, cell - 2)
    shape = shapes[0]

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

        for i in range(4):
            shape[i].x += pos

        for i in net:
            pygame.draw.rect(play_zone, (80, 80, 80), i, 1)

        for i in range(4):
            shape_rect.x = shape[i].x * cell
            shape_rect.y = shape[i].y * cell
            pygame.draw.rect(play_zone, (255, 255, 255), shape_rect)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
