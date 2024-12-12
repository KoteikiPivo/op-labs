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
    def __init__(self, power):
        self.power = power

    def get_color(self):
        return TILE_COLORS[self.power - 1]


def draw_tiles(surface, tiles):
    row = 0
    for tile_rows in tiles:
        col = 0
        for tile in tile_rows:
            if tile is None:
                col += 1
                continue
            color = tile.get_color()
            if (tile.power < 3):
                font_color = FONT_COLORS[0]
            else:
                font_color = FONT_COLORS[1]
            pygame.draw.rect(
                surface, color,
                (col * width, row * height, width, height))
            text = font.render(str(2 ** tile.power), 1, font_color)
            surface.blit(
                text, (
                    col * width + (width / 2 - text.get_width() / 2),
                    row * height + (height / 2 - text.get_height() / 2),
                )
            )
            col += 1
        row += 1


def merge_tiles(tile1, tile2):
    tile1.power += 1
    return None


def move_tiles(surface, tiles, direction):
    match direction:
        case "left":
            for i in range(4):
                for j in range(4):
                    if tiles[i][j] is None:
                        continue
                    shift = 0
                    merge = False
                    while (shift < j):
                        if tiles[i][j - shift - 1] is None:
                            shift += 1
                            continue
                        elif (tiles[i][j - shift - 1].power
                              == tiles[i][j].power):
                            tiles[i][j] = merge_tiles(
                                tiles[i][j - shift - 1], tiles[i][j])
                            merge = True
                            break
                        else:
                            break
                    if merge is False and shift != 0:
                        tiles[i][j - shift] = tiles[i][j]
                        tiles[i][j] = None
        case "down":
            for j in range(3, -1, -1):
                for i in range(3, -1, -1):
                    if tiles[i][j] is None:
                        continue
                    shift = 0
                    merge = False
                    while (shift < 3 - i):
                        if tiles[i + shift + 1][j] is None:
                            shift += 1
                            continue
                        elif (tiles[i + shift + 1][j].power
                              == tiles[i][j].power):
                            tiles[i][j] = merge_tiles(
                                tiles[i + shift + 1][j], tiles[i][j])
                            merge = True
                            break
                        else:
                            break
                    if merge is False and shift != 0:
                        tiles[i + shift][j] = tiles[i][j]
                        tiles[i][j] = None
        case "up":
            for j in range(4):
                for i in range(4):
                    if tiles[i][j] is None:
                        continue
                    shift = 0
                    merge = False
                    while (shift < i):
                        if tiles[i - shift - 1][j] is None:
                            shift += 1
                            continue
                        elif (tiles[i - shift - 1][j].power
                              == tiles[i][j].power):
                            tiles[i][j] = merge_tiles(
                                tiles[i - shift - 1][j], tiles[i][j])
                            merge = True
                            break
                        else:
                            break
                    if merge is False and shift != 0:
                        tiles[i - shift][j] = tiles[i][j]
                        tiles[i][j] = None
        case "right":
            for i in range(3, -1, -1):
                for j in range(3, -1, -1):
                    if tiles[i][j] is None:
                        continue
                    shift = 0
                    merge = False
                    while (shift < 3 - j):
                        if tiles[i][j + shift + 1] is None:
                            shift += 1
                            continue
                        elif (tiles[i][j + shift + 1].power
                              == tiles[i][j].power):
                            tiles[i][j] = merge_tiles(
                                tiles[i][j + shift + 1], tiles[i][j])
                            merge = True
                            break
                        else:
                            break
                    if merge is False and shift != 0:
                        tiles[i][j + shift] = tiles[i][j]
                        tiles[i][j] = None


def generate_tile(tiles):
    empty = []
    for i, inner in enumerate(tiles):
        for j, element in enumerate(inner):
            if tiles[i][j] is None:
                empty.append([i, j])
    if empty != []:
        gen = random.choice(empty)
        tiles[gen[0]][gen[1]] = Tile(1)
        return True
    else:
        return False


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

    draw_tiles(surface, tiles)
    draw_grid(surface)

    pygame.display.update()


def prevent_small_window(event, surface):
    window_width = pygame.display.get_window_size()[0]
    window_height = pygame.display.get_window_size()[1]

    if window_width < 400:
        window_width = 400
    if window_height < 400:
        window_height = 400
    if (window_width, window_height) != event.size:
        surface = pygame.display.set_mode(
            (window_width, window_height), pygame.RESIZABLE)
    return surface


def game_over_check(tiles):
    for i in range(4):
        for j in range(4):
            pass


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

    generate_tile(tiles)
    generate_tile(tiles)

    tiles_full = False
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
                main_surface = prevent_small_window(event, main_surface)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_tiles(main_surface, tiles, "left")
                    tiles_full = generate_tile(tiles)
                elif event.key == pygame.K_DOWN:
                    move_tiles(main_surface, tiles, "down")
                    tiles_full = generate_tile(tiles)
                elif event.key == pygame.K_UP:
                    move_tiles(main_surface, tiles, "up")
                    tiles_full = generate_tile(tiles)
                elif event.key == pygame.K_RIGHT:
                    move_tiles(main_surface, tiles, "right")
                    tiles_full = generate_tile(tiles)

        if tiles_full is True:
            game_over_check(tiles)

        draw_all(main_surface, tiles)

    pygame.quit()
    print(tiles)


if __name__ == "__main__":
    main()
