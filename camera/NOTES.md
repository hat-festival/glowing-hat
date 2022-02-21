# Locating the lights in 3d-space

Inspired by [Matt Parker's 500-LED Christmas Tree](https://www.youtube.com/watch?v=WuMRJf6B5Q4), let's work out the `(x, y, z)` of each light.

The basic principle is:

- find yourself a dark place
- point the camera at the front of the hat
- for each light in the string:
  - turn it on
  - take a photo

Then turn the hat though `π / 2 rad` and take another set of photos, and repeat until you've captured the front, left, back and right sides of the hat.

Now [using some fancy Computer Vision tools](https://pypi.org/project/opencv-python/), locate the brightest spot in each image.

For the `front` images, the `(x, y)` of the bright spot is straight-up the `(x, y)` in hatspace; the `back` images give `(image-width - x, y)`. For the `right` images, the bright spot is `(z, y)` in hatspace; the `left` images yield `(image-width - z, y)`.

## Getting the photos

In addition to a second Pi with [a camera](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera), we'll need some method of placing the hat and the camera a fixed distance apart and square-on to each other. Did I use Lego? Of course I used Lego.

### Attaching the hat

The strapping inside the hat has this plastic bracket thing at the centre:

![hat bracket](/assets/hat-bracket.png)

So I constructed a Lego interface for this

![hat interface](/assets/hat-interface.png)

and they fit together like this

![lego in hat](/assets/lego-hat-junction.png)

### Mounting the camera

I tried lining up the holes with Technic beams and using cable-ties and all that, but eventually I found the best way to mount the camera to the Lego was by sticking it on with some blu-tack:

![camera mount](/assets/camera-mount.png)

### Linking it all together

After a lot of tinkering and fine-tuning, I came up with this arrangement:

![side view](/assets/side-view.png)

The hat is mounted high enough that its internal parts don't foul on the Lego, the camera is mounted at the right height to get the whole hat in frame, and the distance between the base of each platform is 58 studs.

And how did I

FOCUSCAM

## Taking the photos

Something about adjusting the exposure, killing AWB, taking the secondary pictures

## Processing the photos

Once you have a full set of photos, pull them locally:

```bash
rsync -av pi@fancycamera.local:analysis/ /opt/analysis/
```

> You could do this analysis on the Pi, but it seems a little unfair

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

We can now take these little bits of JSON and run them through a futher tool:

```bash
foo
```

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

To help deal with this problem, the `capture.py` script takes an additional photo of each light, using a much longer exposure time, named `001-long.jpg` or whatever. So to solve for light `55`, for example, from the laptop (not inside the container), try something like

```bash
open ../analysis/left/055*jpg ../analysis/right/055*jpg
```

You should now be looking at the regular and long-exposure photos of light `055`, taken from each side. Presuming at least one of them has a bright spot on it, you just need to work out where it is (by drawing a box in Preview or whatever), then fill in the data in `locations.yaml`, according to these rules:

- for `front`, `x` yields `x`
- for `right`, `x` yields `z`
- for `back`, `image-width - x` yields `x`
- for `left`, `image-width - x` yields `z`

### Lights which are out of position

Dityscript, blalblah, spt the out-of-place lights

Say we have a light with a bogus `x` value:

To get the index of the offending light, run

```bash
sudo python step_lights.py
```

and `crtl-c` out when it gets to the light you want.

Now you can home-in on the correct values for this light:

```bash
sudo python calibrator.py x 1000
```

which will light all lights for with an `x` value less than 1000. Adjust this value up and down until you get the range which should have illuminated the bad light, then put this value in `locations.yaml`
