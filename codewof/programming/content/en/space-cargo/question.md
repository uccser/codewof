# Space Cargo

Make a function `eject_cargo(cargo, hull_capacity)` that takes two arguments:

- `cargo`, a Python list of strings representing items stored in the hull of your spaceship. Each item weighs 1 unit.
- `hull_capacity`, an integer representing how much space you have on board.

If the spaceship has more cargo than hull capacity, it should pop items from the end of `cargo` and **print** `'Ejected {item}'`, until the spaceship can carry the remaining items in it's hull.
Then it should **return** the remaining items.
