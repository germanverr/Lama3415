from src.player import Player  # Импортируйте класс Player
from src.deck import Deck  # Импортируйте класс Deck
from src.card import LlamaCard  # Импортируйте класс LlamaCard

class GameState:
    def __init__(
            self, players: list[Player], deck: Deck, top: LlamaCard, current_player: int = 0, is_loaded_from_json: bool = False
    ):
        self.players: list[Player] = players
        self.deck: Deck = deck
        self.top: LlamaCard = top
        self.__current_player: int = current_player
        self.is_loaded_from_json: bool = is_loaded_from_json

    @property
    def current_player_index(self):   #Возвращает индекс текущего игрока
        return self.__current_player

    def current_player(self) -> Player:  #Метод, возвращающий текущего игрока
        return self.players[self.__current_player]

    def __eq__(self, other): #Метод для сравнения двух объектов GameState. Он проверяет, равны ли списки игроков, колоды, верхняя карта и индекс текущего игрока
        if self.players != other.players:
            return False
        if self.deck != other.deck:
            return False
        if self.top != other.top:
            return False
        if self.__current_player != other.__current_player:
            return False
        return True

    def save(self) -> dict: #Метод, который возвращает состояние игры в виде словаря, что может быть полезно для сохранения игры
        return {
            "top": str(self.top),
            "deck": str(self.deck),
            "current_player_index": self.__current_player,
            "players": [p.save() for p in self.players],
        }

    @classmethod
    def load(cls, data: dict): #Класс-метод, который загружает состояние игры из словаря, создавая новый объект GameState
        players = [Player.load(d) for d in data["players"]]
        return cls(
            players=players,
            deck=Deck.load(data["deck"]),
            top=LlamaCard.load(data["top"]),
            current_player=int(data["current_player_index"]),
        )

    def next_player(self): #Метод, который переходит к следующему игроку
        """Ход переходит к следующему игроку."""
        n = len(self.players)
        self.__current_player = (self.__current_player + 1) % n

    def draw_card(self) -> LlamaCard: #Метод, позволяющий текущему игроку взять карту из колоды
        """Текущий игрок берет карту из колоды."""
        if not self.deck.cards:  # Проверяем, что в колоде есть карты
            print("Колода пуста, нельзя взять карту.")
            return None
        card = self.deck.draw_card()
        self.current_player().hand.add_card(card)
        return card

    def play_card(self, card: LlamaCard): #Метод, который позволяет текущему игроку сыграть карту
        """Карта card от текущего игрока переходит в top."""
        if card.can_play_on(self.top):  # Проверяем, можно ли сыграть карту
            self.current_player().hand.remove_card(card)
            self.top = card
        else:
            print(f"{card} нельзя сыграть на {self.top}.")

    def deal_cards(self, num_cards: int = 6): #Метод для раздачи карт игрокам
        """Раздача карт игрокам."""
        for _ in range(num_cards):
            for player in self.players:
                if self.deck.cards:  # Проверяем, что в колоде есть карты
                    player.hand.add_card(self.deck.draw_card())

    def start_game(self): #Метод для начала игры, который перемешивает колоду и раздает карты
        """Начало игры."""
        self.deck.shuffle()
        self.deal_cards()
        self.top = self.deck.draw_card()  # Перевернуть верхнюю карту
        print(f"Начальная карта: {self.top}")

    def end_round(self): #Метод, который обрабатывает конец раунда, подсчитывая очки игроков
        """Обработка конца раунда."""
        scores = {player.name: player.calculate_score() for player in self.players}
        print("Конец раунда. Подсчет очков:")
        for name, score in scores.items():
            print(f"{name}: {score} очков")
        # Здесь можно добавить логику для определения победителя
        for player in self.players:
            player.hand.clear()  # Очистка рук игроков

    def is_round_over(self) -> bool: #Метод, который проверяет, закончился ли раунд
        """Проверка, закончился ли раунд."""
        return any(len(player.hand.cards) == 0 for player in self.players)

    def player_action(self): #Метод, который обрабатывает действия текущего игрока, запрашивая у него выбор действия (играть, взять или выйти)
        """Обработка действий текущего игрока."""
        current = self.current_player()
        print(f"{current.name}: {current.hand}")

        while True:
            action = input(f"{current.name}, выберите действие (играть/взять/выйти): ").strip().lower()
            if action == "играть":
                card_value = input("Введите значение карты, которую хотите сыграть: ")
                try:
                    card = LlamaCard(int(card_value))  # Пробуем создать карту
                    if card in current.hand.cards:
                        self.play_card(card)
                        print(f"{current.name} играет {card}")
                        break
                    else:
                        print("Такой карты нет в руке.")
                except ValueError:
                    print("Недопустимое значение карты.")
            elif action == "взять":
                self.draw_card()
                print(f"{current.name} берет карту.")
                break
            elif action == "выйти":
                current.hand.clear()  # Убираем карты игрока
                print(f"{current.name} выходит из раунда.")
                break
            else:
                print("Неверное действие. Попробуйте снова.")

    def play_game(self): #Основной цикл игры, который управляет ходом игры.
        """Основной цикл игры."""
        self.start_game()
        while True:
            self.player_action()
            if self.is_round_over():
                self.end_round()
                break
            self.next_player()