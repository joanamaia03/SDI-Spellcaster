class Player:
    def __init__(self, name, health=100, mana=50):
        self.name = name
        self.health = health
        self.mana = mana
        self.reflecting = False
        self.reflected_damage = 0
        
    def is_alive(self):
        return self.health > 0

    def cast_spell(self, spell):
        if self.mana >= spell.mana_cost:
            self.mana -= spell.mana_cost
            if spell.name == "Heal":
                self.health += abs(spell.damage)
                if self.health > 100:
                    self.health = 100
                return 0
            elif spell.name == "Mana Charge":
                self.mana += abs(spell.mana_cost)
                if self.mana > 100:
                    self.mana = 100
                return 0
            else:
                return spell.damage
        else:
            print(f"{self.name} does not have enough mana to cast {spell.name}.")
            return "fail"

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def __str__(self):
        return f"{self.name} (Health: {self.health}, Mana: {self.mana})"