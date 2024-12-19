import pygame
import random
from itertools import groupby, product
from tkinter import messagebox

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

diagonals = []
for _, coords in groupby(
        sorted(product(range(4), repeat=2), key=sum),
        key=sum):
    diagonals.append([i for i in [*coords]])

diagonals = diagonals[1::2]


class Tile:
    def __init__(self, power):
        self.power = power

    def get_color(self):
        return TILE_COLORS[self.power - 1]


def merge_tiles(tile1, tile2):
    tile1.power += 1
    return None


def move_tiles(surface, tiles, direction):
    moved = False
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
                            moved = True
                            break
                        else:
                            break
                    if merge is False and shift != 0:
                        tiles[i][j - shift] = tiles[i][j]
                        tiles[i][j] = None
                        moved = True
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
                            moved = True
                            break
                        else:
                            break
                    if merge is False and shift != 0:
                        tiles[i + shift][j] = tiles[i][j]
                        tiles[i][j] = None
                        moved = True
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
                            moved = True
                            break
                        else:
                            break
                    if merge is False and shift != 0:
                        tiles[i - shift][j] = tiles[i][j]
                        tiles[i][j] = None
                        moved = True
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
                            moved = True
                            break
                        else:
                            break
                    if merge is False and shift != 0:
                        tiles[i][j + shift] = tiles[i][j]
                        tiles[i][j] = None
                        moved = True
    return moved


def generate_tile(tiles):
    empty = []
    for i, inner in enumerate(tiles):
        for j, element in enumerate(inner):
            if tiles[i][j] is None:
                empty.append([i, j])
    gen = random.choice(empty)
    tiles[gen[0]][gen[1]] = Tile(1)
    if len(empty) <= 1:
        return True
    else:
        return False


def draw_tiles(surface, tiles):
    row = 0
    for tile_row in tiles:
        col = 0
        for tile in tile_row:
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


def check_same(tile1, tile2):
    return tile1.power == tile2.power


def game_over_check(tiles):
    game_over = True
    for diag in diagonals:
        for coord in diag:
            if coord[0] != 0:
                game_over = not check_same(
                    tiles[coord[0]][coord[1]], tiles[coord[0] - 1][coord[1]])
            if coord[0] != 3 and game_over:
                game_over = not check_same(
                    tiles[coord[0]][coord[1]], tiles[coord[0] + 1][coord[1]])
            if coord[1] != 0 and game_over:
                game_over = not check_same(
                    tiles[coord[0]][coord[1]], tiles[coord[0]][coord[1] - 1])
            if coord[1] != 3 and game_over:
                game_over = not check_same(
                    tiles[coord[0]][coord[1]], tiles[coord[0]][coord[1] + 1])
            if game_over is False:
                break
        if game_over is False:
            break
    return game_over


def game_win_check(tiles):
    for tile_row in tiles:
        for tile in tile_row:
            if tile is not None and tile.power == 11:
                return True
    return False


def restart_game(tiles):
    tiles = [None] * 4
    for i in range(4):
        tiles[i] = [None] * 4
    generate_tile(tiles)
    generate_tile(tiles)
    pygame.event.clear()
    return tiles


def main():
    global width
    global height
    main_surface = pygame.display.set_mode(
        (800, 800), pygame.RESIZABLE)
    pygame.display.set_caption('2048')
    icon = pygame.image.load('lab3/icon.jpg')
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()

    # Lose
    # tiles = [[Tile(1), Tile(2), Tile(3), Tile(4)], [Tile(5), Tile(6), Tile(8), Tile(9)],
    #         [Tile(1), Tile(2), Tile(3), Tile(4)], [Tile(5), Tile(6), Tile(1), Tile(1)]]

    # Win
    # tiles = [[Tile(1), Tile(2), Tile(3), Tile(4)], [Tile(5), Tile(6), Tile(10), Tile(10)],
    #         [Tile(1), Tile(2), Tile(3), Tile(4)], [Tile(5), Tile(6), Tile(1), Tile(1)]]

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

            elif event.type == pygame.KEYDOWN:
                if event.key in {pygame.K_LEFT, pygame.K_h, pygame.K_a}:
                    if move_tiles(main_surface, tiles, "left"):
                        tiles_full = generate_tile(tiles)
                elif event.key in {pygame.K_DOWN, pygame.K_j, pygame.K_s}:
                    if move_tiles(main_surface, tiles, "down"):
                        tiles_full = generate_tile(tiles)
                elif event.key in {pygame.K_UP, pygame.K_k, pygame.K_w}:
                    if move_tiles(main_surface, tiles, "up"):
                        tiles_full = generate_tile(tiles)
                elif event.key in {pygame.K_RIGHT, pygame.K_l, pygame.K_d}:
                    if move_tiles(main_surface, tiles, "right"):
                        tiles_full = generate_tile(tiles)
                elif event.key == pygame.K_r:
                    replay = messagebox.askyesno(
                        "Restart game", "Do you wish to restart the game?")
                    if replay is True:
                        tiles = restart_game(tiles)
                        tiles_full = False

        draw_all(main_surface, tiles)

        if tiles_full is True:
            if game_over_check(tiles):
                replay = messagebox.askyesno(
                    "You lost!", "Do you wish to play again?")
                if replay is False:
                    pygame.quit()
                else:
                    tiles = restart_game(tiles)
                    tiles_full = False

        if game_win_check(tiles) is True:
            replay = messagebox.askyesno(
                "You won!", "Do you wish to play again?")
            if replay is False:
                pygame.quit()
            else:
                tiles = restart_game(tiles)
                tiles_full = False

    pygame.quit()


if __name__ == "__main__":
    main()

