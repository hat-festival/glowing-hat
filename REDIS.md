# What to store in Redis?

- The rotating `hue` from the `ColourWheel`
- The current `mode`
  - lookups for this string to actual ModeClass
  - get the modes to register themselves?
- The current RGB colour
- The current colour-set as a rotating `deque`-ish list of `RGB` triples
- `axis`
- `invert` value

- colour-set names as a rotating queue?
- mode names as a rotating queue?

when we call `next_mode` or whatever, get the first mode, store it in `mode`, then rotate the queue

hoops:

- modes
- colour-sets
- colours
