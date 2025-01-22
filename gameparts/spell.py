import random

class Spell:
    def __init__(self, name, damage, mana_cost):
        self.name = name
        self.damage = damage
        self.mana_cost = mana_cost
        self.is_reflect = name.lower() == "reflect"
    def __str__(self):
        return f"{self.name} (Damage: {self.damage}, Mana Cost: {self.mana_cost})"

    def cast(self, caster, target, all_spells):
        if self.is_reflect:
            caster.reflecting = True
            return 0
        if caster.mana < self.mana_cost:
            return "fail"
        caster.mana -= self.mana_cost
        if self.name.lower() == "big charge":
            caster.mana += self.damage
            caster.take_damage(5)  # Cost 5 HP
            return 0
        target.take_damage(self.damage)
        return self.damage