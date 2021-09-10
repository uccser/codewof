def eject_cargo(cargo, hull_capacity):
    while len(cargo) > hull_capacity:
        ejected_item = cargo.pop()
        print('Ejected ' + ejected_item)
    return cargo


print(eject_cargo(['Fuel Cell', 'Fuel Cell', 'Space Food', 'Rain Coat'], 2))
print(eject_cargo(['Fuel Cell', 'Fuel Cell', 'Space Food', 'Rain Coat'], 4))
print(eject_cargo(['First Aid Kit', 'Space Plant', 'Bottled Water', 'Fuel Cell'], 0))
print(eject_cargo([], 0))
print(eject_cargo([], 1))
