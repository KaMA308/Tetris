import pygame


def main():
    pygame.init()

    w, h = 10, 20
    tile = 35

    size = width, height = 600, 800
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Tetris')

    play_zone = pygame.Surface((350, 700))
    play_zone.fill((18, 28, 89))

    clock = pygame.time.Clock()
    FPS = 60

    net = [pygame.Rect(x * tile, y * tile, tile, tile) for x in range(w) for y in range(h)]

    running = True
    while running:
        screen.fill((43, 66, 158))
        screen.blit(play_zone, (50, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for i in net:
            pygame.draw.rect(play_zone, (40, 40, 40), i, 1)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
