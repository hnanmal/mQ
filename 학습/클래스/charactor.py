from levelup import Levelup_data


class Charactor_warrior(Levelup_data):
    def __init__(self):
        self.level = 1
        self.exp = 0
        self.hp_max = 10
        self.hp_crnt = 10
        self.atk = 2

    def get_exp(self, reward_exp):
        crnt_exp = self.exp + reward_exp

        if crnt_exp >= 100:
            crnt_exp -= 100
            self.level += 1

            # 레벨업 보상
            self.hp_max += self.hp_increase(self.level)
            self.hp_crnt = self.hp_max
            self.atk += self.atk_increase(self.level)

        self.exp = crnt_exp

    def 상태창(self):
        status = f"""
        level: {self.level}
        exp: {self.exp}
        atk: {self.atk}
        HP: {self.hp_crnt} / {self.hp_max}
        """
        # print(status)
        return status

    def __str__(self):
        return self.상태창()
