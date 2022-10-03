from dataclasses import dataclass


@dataclass
class Unit:
    name: str
    rank: int


@dataclass
class Freezer:
    units: list[Unit]


freezer = Freezer
freezer.units = []

unit1 = Unit("ml", 99)
freezer.units.append(unit1)

unit2 = Unit(rank=1, name="Kg")
freezer.units.append(unit2)

print(freezer.units)
print("-------")
print(freezer)
print("-------")
