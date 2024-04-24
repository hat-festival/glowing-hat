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

And we get some YAML like this, which represents the absolute pixel locations of each light. Some them come out as fractional, because we got multiple values for a given light on a given axis, so we take the average.

And some of them only have two out of three axes. This happens for reasons which I gave up trying to understand, but it turns out it doesn't really matter - as long as we have correct values for most of the lights, we can fill in the gaps by hand. So there I was, sticking bits of blue-tac to the problem lights, then lighting up the nearby lights in the Python console, and slowly homing in on the correct positions. Janky as hell, but it works.

We run these through one more transformation to scale these numbers so x runs from -1 to +1 across the hat, z runs from -1 to +1 front-to-back, and then because the hat is mostly the top-half of a sphere, the y-values run from 0 at the base to +1 at the top. And now the lights are fully-mapped in hat-space, and we can say things like "light up all the lights for which z is greater than zero".

We can also work out the angle of each pixel in each of the x, y and z planes, using some half-remembered trigonometry.
