import pygame
from src.card import LlamaCard
from src.resource import RESOURCE as RSC
from src.ui.event import CustomEvent

class ViewCard:
    WIDTH = RSC["card_width"]
    HEIGHT = RSC["card_height"]
    IMAGE_BACK = None
    SELECTED_COLOR = 'magenta' # Цвет выделения карты
    BORDERX = RSC["border_x"]
    BORDERY = RSC["border_y"]

    def __init__(self, card: LlamaCard, x: int = 0, y: int = 0, opened: bool = True):
        self.img_front = None
        self.card = card  # Вызовет сеттер, который загрузит изображение
        self.x = x
        self.y = y
        self.opened = opened
        self.selected = False
        self.chooseable = False

    @property
    def card(self) -> LlamaCard:
        return self.__card

    @card.setter
    def card(self, value: LlamaCard):
        if not isinstance(value, LlamaCard):
            raise TypeError(f'Expected LlamaCard, got {type(value)}')
        self.__card = value
        self.load_images()

    def load_images(self):
        # Загрузка изображений
        try:
            img = pygame.image.load(f"img/{self.card.value}.png")  # Путь к изображению
            self.img_front = pygame.transform.scale(img, (self.WIDTH, self.HEIGHT))
            if self.IMAGE_BACK is None:
                img_back = pygame.image.load("img/back.png")
                self.IMAGE_BACK = pygame.transform.scale(img_back, (self.WIDTH, self.HEIGHT))
        except pygame.error as e:
            print(f"Ошибка загрузки изображения: {e}")

    def __repr__(self):
        return f'{self.card} ({self.x}, {self.y})'

    def rect(self) -> pygame.Rect:
        # Метод для получения прямоугольника, представляющего карту
        return pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def redraw(self, display: pygame.Surface):
        # Метод для отрисовки карты на экране
        if self.selected:
            # Если карта выбрана, рисуем рамку выделения
            r = (
                self.x - self.BORDERX,
                self.y - self.BORDERY,
                self.WIDTH + 2 * self.BORDERX,
                self.HEIGHT + 2 * self.BORDERY
            )
            display.fill(self.SELECTED_COLOR, r) # Заполняем область выделения цветом

        img = self.img_front if self.opened else self.IMAGE_BACK # Выбираем изображение для отрисовки
        display.blit(img, (self.x, self.y)) # Отрисовываем изображение на экране

    def event_processing(self, event: pygame.event.Event):
        if event.type == CustomEvent.SELECT_INTERACTIVE_CARDS:
            data = event.user_data
            print(f'ViewCard.event_processing->{CustomEvent(event.type).name} user_data={data}')
            cards = data['cards']  # list[LlamaCard]
            if not cards:
                self.chooseable = False # Если нет доступных карт, сбрасываем флаг
                self.selected = False
            else:
                self.chooseable = self.card in cards # Проверяем, можно ли выбрать текущую карту
                self.selected = self.chooseable # Устанавливаем состояние выделения

        if event.type == pygame.MOUSEBUTTONDOWN and self.chooseable:
            if pygame.mouse.get_pressed()[0]: # Проверяем, нажата ли левая кнопка мыши
                x, y = pygame.mouse.get_pos() # Получаем текущие координаты мыши
                if self.rect().collidepoint(x, y):  # Проверяем, попадает ли курсор в область карты
                    print(f'Карта {self.card} выбрана!')

    def flip(self):
        # Метод для переворота карты
        self.opened = not self.opened

    def select(self):
        # Метод для выбора карты
        self.selected = not self.selected
        print(f'{self.selected=}')

