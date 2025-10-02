from charactor import Charactor_warrior
from enemy import Enemy


class Battle:
    def __init__(self, char: Charactor_warrior, enemy: Enemy):
        self.char = char
        self.enemy = enemy

    def attack(self):
        self.char.hp_crnt -= self.enemy.atk
        print(f"주인공은 {self.enemy.atk} 의 데미지를 입었다.")
        print(f"현재체력 : {self.char.hp_crnt}\n")
        self.enemy.hp_crnt -= self.char.atk
        print(f"적은 {self.char.atk} 의 데미지를 입었다.\n")

    def fight(self):
        while self.char.hp_crnt > 0 and self.enemy.hp_crnt > 0:
            self.attack()

        if self.enemy.hp_crnt <= 0:
            self.char.get_exp(self.enemy.exp)
            print("You win")
            print(f"You get exp {self.enemy.exp}\n")

        elif self.char.hp_crnt <= 0:
            self.char.get_exp(-50)
            print("You died")
            print(f"You lost exp 50\n")
