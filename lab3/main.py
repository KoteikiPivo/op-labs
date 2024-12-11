import pygame
import random

pygame.init()

GAME_COLORS = [
    (205, 192, 180),
    (187, 173, 160)
]

TILE_COLORS = [
    (237, 229, 218),
    (238, 225, 201),
    (243, 178, 122),
    (246, 150, 101),
    (247, 124, 95),
    (247, 95, 59),
    (237, 207, 114),
    (237, 204, 97),
    (237, 200, 80),
    (237, 197, 63),
    (237, 177, 46)
]

FONT_COLORS = [
    (119, 110, 101),
    (10, 10, 10)
]

width = 200
height = 200
thickness = int((width + height) * 0.05)
font = pygame.font.SysFont("consolas", 60, bold=True)


class Tile:
    def __init__(self, row, col, power):
        self.row = row
        self.col = col
        self.power = power

    def get_color(self):
        return TILE_COLORS[self.power - 1]

    def draw_tile(self, surface):
        color = self.get_color()
        if (self.power < 3):
            font_color = FONT_COLORS[0]
        else:
            font_color = FONT_COLORS[1]
        pygame.draw.rect(
            surface, color,
            (self.row * width, self.col * height, width, height))
        text = font.render(str(2 ** self.power), 1, font_color)
        surface.blit(
            text, (
                self.row * width + (width / 2 - text.get_width() / 2),
                self.col * height + (height / 2 - text.get_height() / 2),
            )
        )


def move_tiles(surface, tiles, clock, direction):
    match direction:
        case "left":
            pass
        case "down":
            pass
        case "up":
            pass
        case "right":
            pass


def generate_tiles(tiles):
    first = random.choices(range(0, 3), k=2)
    tiles[first[0]][first[1]] = (Tile(first[0], first[1], 1))
    second = random.choices(range(0, 3), k=2)
    while second == first:
        second = random.choices(range(0, 3), k=2)
    tiles[second[0]][second[1]] = (Tile(second[0], second[1], 1))


def draw_grid(surface):
    for i in range(0, 5):
        pygame.draw.line(
            surface, GAME_COLORS[1],
            (0, i * height), (width * 4, i * height), thickness)

        for j in range(0, 5):
            pygame.draw.line(
                surface, GAME_COLORS[1],
                (j * width, 0), (j * width, height * 4), thickness)


def draw_all(surface, tiles):
    surface.fill(GAME_COLORS[0])

    for tile_rows in tiles:
        for tile in tile_rows:
            if tile is not None:
                tile.draw_tile(surface)

    draw_grid(surface)

    pygame.display.update()


def main():
    global width
    global height
    main_surface = pygame.display.set_mode(
        (800, 800), pygame.RESIZABLE)
    pygame.display.set_caption('2048')

    clock = pygame.time.Clock()

    # tiles = [[None] * 4, [None] * 4, [None] * 4, [None] * 4]
    tiles = [None] * 4
    for i in range(4):
        tiles[i] = [None] * 4

    generate_tiles(tiles)

    running = True
    while running:
        clock.tick(60)
        window_width = pygame.display.get_window_size()[0]
        window_height = pygame.display.get_window_size()[1]
        width = window_width // 4
        height = window_height // 4
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.VIDEORESIZE:
                window_width = pygame.display.get_window_size()[0]
                window_height = pygame.display.get_window_size()[1]

                if window_width < 400:
                    window_width = 400
                if window_height < 400:
                    window_height = 400
                if (window_width, window_height) != event.size:
                    main_surface = pygame.display.set_mode(
                        (window_width, window_height), pygame.RESIZABLE)

        draw_all(main_surface, tiles)

    pygame.quit()
    print(tiles)


if __name__ == "__main__":
    main()
