import pygame
import random
import math

pygame.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('comicsans', 25)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)

    SIDE_PAD = 100
    TOP_PAD = 150 

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algo Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    controls = draw_info.FONT.render("R - Reset|SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 45))

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 75))

    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, 
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst


def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True

    return lst


def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    return lst


def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"

    pygame.quit()


if __name__ == "__main__":
    main()










# import pygame
# import random
# import math

# pygame.init()

# # Drawing Information class to handle the display and graphics
# class DrawInformation:
#     BLACK = 0, 0, 0
#     WHITE = 255, 255, 255
#     GREEN = 0, 255, 0
#     RED = 255, 0, 0
#     BACKGROUND_COLOR = WHITE

#     FONT = pygame.font.SysFont('comicsans', 30)
#     LARGE_FONT = pygame.font.SysFont('comicsans', 40)

#     SIDE_PAD = 100
#     TOP_PAD = 150 

#     def __init__(self, width, height, lst):
#         self.width = width
#         self.height = height
#         self.window = pygame.display.set_mode((width, height))
#         pygame.display.set_caption("Sorting Algorithm Visualization")
#         self.set_list(lst)

#     def set_list(self, lst):
#         self.lst = lst
#         self.min_val = min(lst)
#         self.max_val = max(lst)

#         # Calculate the size and position of each block
#         self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
#         self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
#         self.start_x = self.SIDE_PAD // 2

# # Function to draw the current sorting status
# def draw(draw_info, algo_name, ascending):
#     draw_info.window.fill(draw_info.BACKGROUND_COLOR)

#     # Draw title and controls
#     title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
#     draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

#     controls = draw_info.FONT.render("R - Reset | SPACE - Sort | A - Ascend | D - Descend", 1, draw_info.BLACK)
#     draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 45))

#     draw_list(draw_info)
#     pygame.display.update()

# # Function to draw the list of bars representing numbers
# def draw_list(draw_info):
#     lst = draw_info.lst

#     for i, val in enumerate(lst):
#         x = draw_info.start_x + i * draw_info.block_width
#         y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

#         color = draw_info.BLACK
#         pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

# # Generate a random starting list for sorting
# def generate_starting_list(n, min_val, max_val):
#     return [random.randint(min_val, max_val) for _ in range(n)]

# # Bubble sort without generator, sorts list in place
# def bubble_sort(lst, ascending=True):
#     n = len(lst)
#     for i in range(n - 1):
#         for j in range(n - 1 - i):
#             if (lst[j] > lst[j + 1] and ascending) or (lst[j] < lst[j + 1] and not ascending):
#                 lst[j], lst[j + 1] = lst[j + 1], lst[j]

# # Insertion sort without generator, sorts list in place
# def insertion_sort(lst, ascending=True):
#     for i in range(1, len(lst)):
#         current = lst[i]
#         j = i - 1
#         while j >= 0 and ((lst[j] > current and ascending) or (lst[j] < current and not ascending)):
#             lst[j + 1] = lst[j]
#             j -= 1
#         lst[j + 1] = current

# # Main function to handle the game loop and events
# def main():
#     run = True
#     clock = pygame.time.Clock()

#     n = 50  # Number of elements
#     min_val = 0  # Minimum value for the list
#     max_val = 100  # Maximum value for the list

#     lst = generate_starting_list(n, min_val, max_val)
#     draw_info = DrawInformation(800, 600, lst)
#     sorting = False  # Flag for sorting
#     ascending = True  # Flag for ascending/descending order

#     sorting_algorithm = bubble_sort
#     sorting_algo_name = "Bubble Sort"

#     while run:
#         clock.tick(60)  # Run at 60 frames per second

#         # Draw the current state
#         draw(draw_info, sorting_algo_name, ascending)

#         # Event handling
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False

#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_r:
#                     lst = generate_starting_list(n, min_val, max_val)  # Reset the list
#                     draw_info.set_list(lst)
#                 elif event.key == pygame.K_SPACE:
#                     sorting_algorithm(lst, ascending)  # Perform sorting when SPACE is pressed
#                     draw_info.set_list(lst)
#                 elif event.key == pygame.K_a:
#                     ascending = True  # Set to ascending order
#                 elif event.key == pygame.K_d:
#                     ascending = False  # Set to descending order
#                 elif event.key == pygame.K_i:
#                     sorting_algorithm = insertion_sort
#                     sorting_algo_name = "Insertion Sort"
#                 elif event.key == pygame.K_b:
#                     sorting_algorithm = bubble_sort
#                     sorting_algo_name = "Bubble Sort"

#     pygame.quit()

# if __name__ == "__main__":
#     main()
