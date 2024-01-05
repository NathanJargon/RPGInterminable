# basic concept only!

import random as r
import time

class Nash:
    def __init__(self, hp, atk, defense, s1=None, s2=None, s3=None, ultima=None)
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        self.ultima = ultima
        
    def __str__(self):
        print("A young venturer of the east—travelling in pursuit of his ultimate calling.")
        
    def attack(self, enemy):
        enemy.hpdecrease(self.atk)
        return f"Enemy has taken {self.atk}"
    
    def death(self):
        if hp <= 0:
            print("Nash has been defeated.")
            time.sleep(1)
            return "Game Over"
            
        
class Terrorist(Nash):
    super().__init__(50, random.randrange(5), 2, "Basic Attack", "Guard Down")
    
    def
    

main = Nash(
    100, random.randrange(10), 5, "Valhalla", "Nordic Resolution", 
    "Eye of the Tiger", "Art of Destruction")
    
