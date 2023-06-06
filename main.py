import pygame
from tkinter import messagebox, Tk
import sys
from collections import deque
pygame.init()

size = (width, height) = 1280, 960 # розмір екрану
colscount, rows = 64, 48 # Кількість колонок та рядків

window = pygame.display.set_mode(size) # додаємо Pygame до нашого вікна
pygame.display.set_caption("Алгоритм Дейкстри. Зроблено для УжНУ (с) Nick Lobanov") # Визначаємо назву вікна

w = width // colscount # Встановлюємо ширину кожної клітинки
h = height // rows # Встановлюємо висоту кожної клітинки

grid = [] # Матриця для збереження клітинок
queue, visited = deque(), [] # Створюємо змінні для черги (Клітинок, які потрібно перевірити) та массив перевіренних клітинок 
path = [] # Массив найкоротшого шляху

    
class Cell:
    def __init__(self, i, j):
        self.x, self.y = i, j # Визначаємо координати клітинки
        self.f, self.g, self.h = 0, 0, 0 # Змінні, для оцінки "ваги" цієї клітинки
        self.neighbors = [] # Массив сусідніх клітинок
        self.prev = None # Попередня клітинка
        self.wall = False # Чи э ця клітинка стіною
        self.visited = False # Чи переглянув алгоритм цю клітинку

    # Відображає клітинку на екрані.
    # @param window window
    # @param color
    def show(self, window, color):
        if self.wall == True: # Якщо клітинка - стіна - замальовуємо її чорним кольором
            color = (0, 0, 0)
        pygame.draw.rect(window, color, (self.x * w, self.y * h, w - 1, h - 1))
            
    
    # Додає сусідні клітинки
    def add_neighbors(self, grid):
        if self.x < colscount - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])

# Додає стінку в позиції pos
# @param int[] pos координати клітинки
# @param boolean state True, якщо потрібно встановити стінку. False - щоб видалити її
def clickWall(pos, state):
    i = pos[0] // w
    j = pos[1] // h
    grid[i][j].wall = state

# Заповнюємо grid нашими клітинками
for i in range(colscount):
    arr = []
    for j in range(rows):
        arr.append(Cell(i, j))
    grid.append(arr)
for i in range(colscount):
    for j in range(rows):
        grid[i][j].add_neighbors(grid)
start = grid[0][0] # початкова точка, з якої буде виконуватись пошук
end = grid[colscount - colscount // 3][rows - colscount // 4] # Кінцева точка, до якої потрібно дійти

# Стартова та кінцеві точки не можуть бути стінами
start.wall = False 
end.wall = False

queue.append(start)
start.visited = True # Визначаємо цю клітинку переглянутою за замовчуванням.

# Запуск візуального інтерфейсу для "малювання" та знаходження найкоротшого шляху
def main():
    finished = False
    noflag = True
    startflag = False # Програма почала роботу пошуку найкоротшого шляху
    while True:
        for event in pygame.event.get(): # Зчитуємо усі події (Клік мишки або закриття програми)
            if event.type == pygame.QUIT: # При закритті програми потрібно припинити роботу нашої програми
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN: # Клік лівої кнопки мишки для встановлення чи видалення стінки
                if event.button in (1, 3):
                    clickWall(pygame.mouse.get_pos(), event.button == 1)
            elif event.type == pygame.MOUSEMOTION: # Якщо зажали кнопку мишки встановлюємо або видаляємо стінку в залежності від кліку
                if event.buttons[0] or event.buttons[2]: 
                    clickWall(pygame.mouse.get_pos(), event.buttons[0])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    startflag = True       

        if startflag: # Скрипт шукає найкоротший шлях
            if len(queue) > 0: # Виконується лише за умовою, що є клітинки, які ми ще не перевірили
                current = queue.popleft() # Перевіряємо найближчу клітинку та видаляємо її з масиву
                if current == end: # Якщо клітинка - кінцева точка, припиняємо пошук
                    temp = current # Записуємо клітинку у тимчасову змінну
                    while temp.prev: # Повертаємось назад, поки не дійдемо до початкової точки
                        path.append(temp.prev) # Додаємо усі клітинки до массиву найкоротшого шляху
                        temp = temp.prev
                    finished = True # Після перевірки усіх клітинок позначаємо скрипт завершеним
                if finished == False: # Якщо алгоритм не завершив пошук - перевіряємо сусідні клітинки
                    for i in current.neighbors:
                        if not i.visited and not i.wall: # Ми не перевіряємо уже перевірені клітинки, а також, не перевіряємо стіни
                            i.visited = True # Позначаємо клітинку перевіреною
                            i.prev = current # Додаємо клітинку у масив попередніх клітинок
                            queue.append(i) # Додаємо сусідні клітинки у чергу для перевірки
            else:
                if not finished:
                    Tk().wm_withdraw()
                    messagebox.showinfo("Помилка", "Неможливо знайти шлях до точки")
                    pygame.quit()
                    
        window.fill((0, 20, 20))
        for i in range(colscount):
            for j in range(rows):
                cell = grid[i][j]
                cell.show(window, (36, 72, 131)) # Заповнюємо кожну клітинку синім кольором
                if cell in path:
                    cell.show(window, (46, 204, 113))
                    cell.show(window, (192, 57, 43))
                elif cell.visited:
                    cell.show(window, (39, 174, 96))
                if cell in queue and not finished:
                    cell.show(window, (44, 62, 80))
                    cell.show(window, (39, 174, 96))
                if cell == start:
                    cell.show(window, (0, 255, 200))
                if cell == end:
                    cell.show(window, (0, 120, 255))
                
        pygame.display.flip()     


main() # Викликаємо функцію main для запуску програми