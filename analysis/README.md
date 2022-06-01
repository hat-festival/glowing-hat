# Locating the lights in 3d-space, part 2

## Processing the photos

Once you have a [full set of photos](/camera/README.md), pull them locally:

```bash
rsync -av pi@fancycamera.local:analysis/ /opt/analysis/
```

> You could do the following analysis on the Pi, but it seems a little unfair

### Find the Bright Spots

The first thing to do is find the Brightest Spot in each image:

```bash
find /opt/analysis -name "*json" -delete
python find_bright_spots.py
```

Notes:

- presuming the camera was correctly adjusted, each photo should have at most one bright spot
- if there's no such spot, we assume that light was on the far-side of the hat, and we ignore that photo

So now for each photo with a bright spot, we have some `json` like:

```json
{ "x": 623, "y": 260 }
```

### Locate the lights in 3d-space

We can now take these little bits of JSON and run them through a further tool:

```bash
PYTHONPATH=../lib python locate_pixels.py
```

which takes the JSON from the previous step, runs it through a number of transformations, and eventually generates `conf/locations.yaml`:

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

These are the absolute pixel locations of each light

- Some of them will be fractional - this happens when multiple values were found for a light on a given axis, so the average of those is used
- Some of them will have only two out of three axes - we'll fix those next

## Fixing the errors

In theory, each light should have _at least_ two bright-spot JSON files: one for its left-right position, and one for back-front. Lights that are at the extreme edges of the hat will get three files, because they can be seen from both sides (and a light right at the top-centre of the hat would get four entries). In practice its a little messier than that

### Lights with no `x` or `z`

Lights right on the sides of the hat (when looking from the front or back) or those right at the front or back (when viewing from the side) can be difficult for the camera to see, and these may not get a full set of coordinates. To find out which lights are affected, run

```bash
cd analysis/
python find_trouble_lights.py
```

to see output like

```bash
No 'x' for [54, 77, 91, 96]
No 'z' for [52]
```

To help deal with this problem, the `capture.py` script takes an additional photo of each light, lit with `[255, 255, 255]` (e.g. very bright white) and using a much longer exposure time, named `001-long.jpg` or whatever. So to solve for light `55`, for example, from the laptop (not inside the container), try something like

```bash
open ../analysis/left/055*jpg ../analysis/right/055*jpg
```

You should now be looking at the regular and long-exposure photos of light `055`, taken from each side. Presuming at least one of them has a bright spot on it, you just need to work out where it is (by drawing a box in Preview or whatever), then fill in the data in `locations.yaml`, according to these rules:

- for `front`, `x` yields `x`
- for `right`, `x` yields `z`
- for `back`, `image-width - x` yields `x`
- for `left`, `image-width - x` yields `z`

### Lights which are out of position

For reasons I cannot understand (and have given up trying), some lights insist on being _completely_ out of place along one axis. There is a dirty manual fix for these, though. Back on the Hat Pi:

```bash
cd debug/
sudo PYTHONPATH=../ python dirty_script.py
```

This will trigger waves of light sweeping across the hat

> enable lines `35`, `36` or `37` to select the axis, and _decrease_ the step-size in line `32` to slow it all down

Running this should expose any rogue lights, as they will light ahead of or behind those close to them. Once you've spotted an offender, mark it somehow (I stuck a little piece of blu-tack to mine), then run another script:

```bash
sudo PYTHONPATH=../ python step_lights.py
```

and `crtl-c` out when it gets to the light you want. Now you have the absolute index of your target, you can home-in on the correct values for it:

```bash
sudo PYTHONPATH=../ python calibrator.py x 1000
```

This will light all lights with an `x` value less than 1000. Adjust this value up and down until you get to the range which should have illuminated the bad light, then put this value in `locations.yaml`. Repeat for any other wonky lights, on any of the axes.

## Find the centres

Also use `calibrator` to find the centres of each axis, and record them in `conf/locations.yaml`.

> Because the hat is essentially the top-half of a sphere, I found it useful to locate the centre of the `y`-axis at the bottom of the hat:

```
python -c "import yaml ; from pathlib import Path ; print(max(list(map(lambda x: x['y'], yaml.safe_load(Path('conf/locations.yaml').read_text())['lights']))))"
```

## And we're done

All of this tooling is very crufty because it was developed by running it on the hat until it worked. It doesn't have any tests, except the actual test of Are The Lights Correctly Located In Hatspace?
