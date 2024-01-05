# basic concept only!

import random as r
import time

class main_character:
    def __init__(self, name, hp, atk, defense, s1=None, s2=None, s3=None, ultima=None):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        self.ultima = ultima
        
    def __str__(self):
        return "A young venturer of the east—travelling in pursuit of his ultimate calling."
        
    def attack(self, enemy):
        enemy.hp -= self.atk
        return f"Enemy has taken {self.atk}"
    
    def death(self):
        if hp <= 0:
            print("Nash has been defeated.")
            time.sleep(1)
            return "Game Over"
            
        
class Enemy(main_character):
    def __init__(self):
        super().__init__("Bandit", 50, r.randrange(5), 2, "Basic Attack", "Guard Down")
    
    

main = main_character(
    "Nash", 100, r.randrange(10), 5, "Valhalla", "Nordic Resolution", 
    "Eye of the Tiger", "Art of Destruction")
    
print(main)
print(main.attack(Enemy()))
