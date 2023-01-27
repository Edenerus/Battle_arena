from unit import BaseUnit


class BaseSingleton(type):
    """ Базовый класс"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    """ Поле боя"""
    STAMINA_PER_ROUND = 1
    player = BaseUnit
    enemy = BaseUnit
    game_is_running = False

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        """ Начало игры"""
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def next_turn(self):
        """ следующий раунд"""
        result = self._check_players_hp()
        if result:
            return result
        if self.game_is_running:
            self._stamina_regeneration()
            self.player.stamina = round(self.player.stamina, 1)
            self.enemy.stamina = round(self.enemy.stamina, 1)
            self.player.hit_points = round(self.player.hit_points, 1)
            self.enemy.hit_points = round(self.enemy.hit_points, 1)
            return self.enemy.hit(self.player)

    def _stamina_regeneration(self):
        """ Востановление стамины"""
        if self.player.stamina + self.STAMINA_PER_ROUND > self.player.unit_class.max_stamina:
            self.player.stamina = self.player.unit_class.max_stamina
        elif self.player.stamina < self.player.unit_class.max_stamina:
            self.player.stamina += self.STAMINA_PER_ROUND
        if self.enemy.stamina + self.STAMINA_PER_ROUND > self.enemy.unit_class.max_stamina:
            self.enemy.stamina = self.enemy.unit_class.max_stamina
        elif self.enemy.stamina < self.enemy.unit_class.max_stamina:
            self.enemy.stamina += self.STAMINA_PER_ROUND

    def _check_players_hp(self):
        """завершение боя"""
        if self.player.hit_points <= 0 and self.enemy.hit_points <= 0:
            self.battle_result = f'Ничья между {self.player.name} и {self.enemy.name}!'
        elif self.player.hit_points >= 0 >= self.enemy.hit_points:
            self.battle_result = f'{self.player.name} победил {self.enemy.name}'
        elif self.player.hit_points <= 0 <= self.enemy.hit_points:
            self.battle_result = f'{self.player.name} проиграл {self.enemy.name}'
        elif self.player.hit_points and self.enemy.hit_points >= 0:
            return None
        return self._end_game()

    def _end_game(self):
        """ Конец игры"""
        self._instances = {}
        result = self.battle_result
        self.game_is_running = False
        return result

    def player_hit(self):
        """ Атака игрока и след. ход"""
        result = self.player.hit(self.enemy)
        turn_result = self.next_turn()
        return f"{result}\n{turn_result}"

    def player_use_skill(self):
        """ Использование спец. умения"""
        result = self.player.use_skill(self.enemy)
        turn_result = self.next_turn()
        return f"{result}\n{turn_result}"
