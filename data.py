class Data:
    def __init__(self, UI):
        self.UI = UI
        self.coins = 0
        self._health = 5
        self.UI.create_hearts(self._health)

        self.unlocked_level = 0
        self.current_level = 0

    @property
    def coins(self):
        return self._coins

    @coins.setter
    def coins(self, value):
        self._coins = value
        if self.coins >= 100:
            self.coins -= 100
            self.health += 1
        self.UI.show_coins(self.coins)

    @property
    def health(self):
        return self._health
    
    @health.setter
    def health(self, value):
        self._health = value
        self.UI.create_hearts(value)