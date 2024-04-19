## Analysing the photos

```yaml
- index: 0
  x: 1348.0
  y: 999.0
  z: 648.0
- index: 1
  x: 1642.0
  y: 774.5
  z: 833.0
- index: 2
  x: 1629.0
  y: 551.0
  z: 1267.0
```

Notes:

And we get some YAML like this, which represents the absolute pixel locations of each light. Some them come out as fractional - this happens when we got multiple values for a given light on a given axis, so we take the average.

And some of them only have two out of three axes. This happens for reasons which I gave up trying to understand, but it turns out it doesn't really matter - as long as you have correct values for most of the lights, you can fill in the gaps by hand. So there I was, sticking bits of blue-tac to the problem lights, then lighting up the nearby lights in the Python console, and slowly homing in on the correct positions. Janky as hell, but it worked.
