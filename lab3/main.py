import pygame

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

width = 200
height = 200
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
        pygame.draw.rect(
            surface, color,
            (self.row * width, self.col * height, width, height))
        text = font.render(str(2 ** self.power), 1, (255, 255, 255))
        surface.blit(
            text, (
                self.row * width + (width / 2 - text.get_width() / 2),
                self.col * height + (height / 2 - text.get_height() / 2),
            )
        )


def draw_grid(surface):
    thickness = int((width + height) * 0.05)
    for i in range(0, 5):
        pygame.draw.line(
            surface, GAME_COLORS[1],
            (0, i * height), (width * 4, i * height), thickness)

        for j in range(0, 5):
            pygame.draw.line(
                surface, GAME_COLORS[1],
                (j * width, 0), (j * width, width * 4), thickness)


def draw_all(surface, tiles):
    surface.fill(GAME_COLORS[0])

    for tile_row in tiles:
        for tile in tile_row:
            tile.draw_tile(surface)

    draw_grid(surface)

    pygame.display.update()


def main():
    main_surface = pygame.display.set_mode(
        (width * 4, height * 4), pygame.RESIZABLE)
    pygame.display.set_caption('2048')

    clock = pygame.time.Clock()

    tiles = [[], [Tile(0, 0, 4), Tile(1, 1, 9), Tile(1, 2, 10)]]
    print(tiles[1][1])

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        draw_all(main_surface, tiles)

    pygame.quit()


if __name__ == "__main__":
    main()
