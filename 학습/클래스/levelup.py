class Levelup_data:
    def __init__(self):
        pass

    def hp_increase(self, next_level):
        if next_level < 10:
            print("레벨업 보상으로 체력 10 상승")
            return 10
        elif next_level < 50:
            print("레벨업 보상으로 체력 20 상승")
            return 20
        else:
            print("레벨업 보상으로 체력 30 상승")
            return 30

    def atk_increase(self, next_level):
        if next_level < 10:
            print("레벨업 보상으로 공격력 1 상승")
            return 1
        elif next_level < 50:
            print("레벨업 보상으로 공격력 2 상승")
            return 2
        else:
            print("레벨업 보상으로 공격력 3 상승")
            return 3
