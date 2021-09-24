# Space Cargo

Make a function `eject_cargo(cargo, hull_capacity)` that takes two arguments:

- `cargo`, a Python list of strings representing items stored in the hull of your spaceship. Each item weighs 1 unit.
- `hull_capacity`, an integer representing how much space you have on board.

It should pop items from the end of `cargo` and then **print** `'Ejected {item}'`. 
It should do this until the spaceship is no longer too full.
Then it should **return** the remaining items.
