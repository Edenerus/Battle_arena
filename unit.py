from __future__ import annotations
from abc import ABC, abstractmethod
from random import randint
from typing import Optional

from classes import UnitClass
from equipment import Equipment, Weapon, Armor


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """

    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hit_points = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = Equipment().get_weapon("ладошки")
        self.armor = Equipment().get_armor('футболка')
        self._is_skill_used = False

    @property
    def health_points(self):
        """ Уровень hp"""
        return round(self.hit_points, 1)

    @property
    def stamina_points(self):
        """ Уровень stamina"""
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon):
        """присваиваем нашему герою новое оружие"""
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        """одеваем новую броню"""
        self.armor = armor
        return f"{self.name} экипирован броней {self.weapon.name}"

    def _count_damage(self, target: BaseUnit) -> int:
        """ Расчет урона"""
        self.stamina -= self.weapon.stamina_per_hit * self.unit_class.stamina
        damage = self.weapon.damage * self.unit_class.attack
        if target.stamina > target.armor.stamina_per_turn * target.unit_class.stamina:
            target.stamina -= target.armor.stamina_per_turn * target.unit_class.stamina
            damage = damage - target.armor.defence * target.unit_class.armor
        else:
            pass
        damage = target.get_damage(damage)
        return damage

    def get_damage(self, damage: int) -> Optional[int]:
        """Получение урона"""
        if damage > 0:
            self.hit_points -= damage
            self.hit_points = self.hit_points
            return round(damage, 1)
        return None

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """этот метод переопределен ниже"""
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        метод использования умения.
        """
        if self._is_skill_used:
            return "Навык уже использован"
        self._is_skill_used = True
        return self.unit_class.skill.use(user=self, target=target)


class PlayerUnit(BaseUnit):
    """ Класс Игрока"""

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар игрока:
        """
        if self.stamina >= self.weapon.stamina_per_hit * self.unit_class.stamina:
            damage = self._count_damage(target)
            if damage:
                return f"{self.name} используя " \
                       f"{self.weapon.name} пробивает " \
                       f"{target.armor.name} соперника и наносит " \
                       f"{damage} урона."
            return f"{self.name} используя " \
                   f"{self.weapon.name} наносит удар, но " \
                   f"{target.armor.name} " \
                   f"cоперника его останавливает."
        return f"{self.name} попытался использовать " \
               f"{self.weapon.name}, но у него не хватило выносливости."


class EnemyUnit(BaseUnit):
    """Класс Соперника"""

    def hit(self, target: BaseUnit) -> str:
        """функция удар соперника"""
        if randint(0, 100) < 10 and \
                self.stamina >= self.unit_class.skill.stamina and not \
                self._is_skill_used:
            return self.use_skill(target)
        if self.stamina >= self.weapon.stamina_per_hit * self.unit_class.stamina:
            damage = self._count_damage(target)
            if damage:
                return f"{self.name} используя " \
                       f"{self.weapon.name} пробивает " \
                       f"{target.armor.name} и наносит Вам " \
                       f"{damage} урона."
            return f"{self.name} используя " \
                   f"{self.weapon.name} наносит удар, но Ваш(а) " \
                   f"{target.armor.name} его останавливает."
        return f"{self.name} попытался использовать " \
               f"{self.weapon.name}, но у него не хватило выносливости."
