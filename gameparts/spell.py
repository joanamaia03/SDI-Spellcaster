class Spell:
    def __init__(self, name, damage, mana_cost):
        self.name = name
        self.damage = damage
        self.mana_cost = mana_cost

    def __str__(self):
        return f"{self.name} (Damage: {self.damage}, Mana Cost: {self.mana_cost})"