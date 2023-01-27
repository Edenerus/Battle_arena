from flask import Flask, render_template, request, redirect, url_for
from equipment import Equipment
from classes import unit_classes
from base import Arena
from unit import PlayerUnit, EnemyUnit, BaseUnit

app = Flask(__name__)

heroes = {
    "player": BaseUnit,
    "enemy": BaseUnit
}

arena = Arena()


@app.route("/")
def menu_page():
    """ Стартовая страница"""
    return render_template("index.html")


@app.route("/fight/")
def start_fight():
    """страница боя"""
    arena.start_game(player=heroes.get("player"), enemy=heroes.get("enemy"))
    return render_template("fight.html", heroes=heroes, result="Бой начался!")


@app.route("/fight/hit")
def hit():
    """БОй"""
    if arena.game_is_running:
        result = arena.player_hit()
        return render_template("fight.html", heroes=heroes, result=result)
    return render_template("fight.html", heroes=heroes, result=arena.battle_result)


@app.route("/fight/use-skill")
def use_skill():
    """ Использование скилов"""
    if arena.game_is_running:
        result = arena.player_use_skill()
        return render_template("fight.html", heroes=heroes, result=result)
    return render_template("fight.html", heroes=heroes, result=arena.battle_result)


@app.route("/fight/pass-turn")
def pass_turn():
    if arena.game_is_running:
        result = arena.next_turn()
        return render_template("fight.html", heroes=heroes, result=result)
    return render_template("fight.html", heroes=heroes, result=arena.battle_result)


@app.route("/fight/end-fight")
def end_fight():
    """ Конец боя"""
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    """ Выбор героя, оружия экепировки"""
    if request.method == "GET":
        header = "Выберите героя"
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        classes = unit_classes
        return render_template(
            "hero_choosing.html",
            result={
                "header": header,
                "classes": classes,
                "weapons": weapons,
                "armors": armors
            }
        )
    if request.method == "POST":
        name = request.form["name"]
        armor_name = request.form["armor"]
        weapon_name = request.form["weapon"]
        unit_class = request.form["unit_class"]
        player = PlayerUnit(name=name, unit_class=unit_classes.get(unit_class))
        player.equip_weapon(Equipment().get_weapon(weapon_name))
        player.equip_armor(Equipment().get_armor(armor_name))
        heroes["player"] = player
        return redirect(url_for("choose_enemy"))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    """ Выбор врага"""
    if request.method == "GET":
        header = "Выберите врага"
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        classes = unit_classes
        return render_template(
            "hero_choosing.html",
            result={
                "header": header,
                "classes": classes,
                "weapons": weapons,
                "armors": armors
            }
        )
    if request.method == "POST":
        name = request.form["name"]
        armor_name = request.form["armor"]
        weapon_name = request.form["weapon"]
        unit_class = request.form["unit_class"]
        enemy = EnemyUnit(name=name, unit_class=unit_classes.get(unit_class))
        enemy.equip_weapon(Equipment().get_weapon(weapon_name))
        enemy.equip_armor(Equipment().get_armor(armor_name))
        heroes["enemy"] = enemy
        return redirect(url_for("start_fight"))


if __name__ == "__main__":
    app.run()
