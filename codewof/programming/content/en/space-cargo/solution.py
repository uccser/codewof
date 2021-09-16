def eject_cargo(cargo, hull_capacity):
    while len(cargo) > hull_capacity:
        ejected_item = cargo.pop()
        print('Ejected ' + ejected_item)
    return cargo
