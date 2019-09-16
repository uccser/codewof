# Driver speed

Write a function `check_speed(speed)` that checks the speed of drivers.
If the speed is less than or equal to 50, it should **print** `Ok.`.
Otherwise print the number of demerit points the driver should receive; the driver should receive one demerit point for every 5km/h they are above the speed limit (50km/h).
If this is higher than five, instead **print** `Licence suspended.`.

For example `check_speed(70)` should **print** `4` and `check_speed(53)` should **print** `0`.
