# Locating the lights in 3d-space

Inspired by [Matt Parker's 500-LED Christmas Tree](https://www.youtube.com/watch?v=WuMRJf6B5Q4), let's work out the `(x, y, z)` of each light.

The basic principle is:

- find yourself a dark place
- point the camera at the front of the hat
- for each light in the string:
  - turn it on
  - take a photo

Then turn the hat though 90 degrees and take another set of photos, and repeat until you've captured the front, left, back and right sides of the hat.

Now [using some fancy Computer Vision tools](https://pypi.org/project/opencv-python/), locate the brightest spot in each image.

For the `front` images, the `(x, y)` of the bright spot is straight-up the `(x, y)` in hatspace; the `back` images give `(image-width - x, y)`. For the `right` images, the bright spot is `(z, y)` in hatspace; the `left` images yield `(image-width - z, y)`.

## Getting the photos

### Set up a second Pi

From a clean install, clone this repo, then:

```bash
sudo raspi-config nonint do_hostname fancycamera
sudo raspi-config nonint do_camera 1
```

```bash
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get install -y python3-pip
```

```bash
python -m pip install picamera
```

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

The hat is mounted high enough that its internal parts don't foul on the Lego, the camera is mounted at the right height to get the whole hat in frame, and the distance between the base of each platform is 58 studs. Please ignore the Thor picture it's all sitting on, it was the handiest Big Flat Surface I could find.

And how did I come up with that 56-stud distance?

### Calibrating the distance

There's a script [here](https://randomnerdtutorials.com/video-streaming-with-raspberry-pi-camera/) to put the camera in streaming mode. Grab it:

```bash
curl https://raw.githubusercontent.com/RuiSantosdotme/Random-Nerd-Tutorials/master/Projects/rpi_camera_surveillance_system.py -o /tmp/focuscam.py
```

> This code has no visible license so I'm not directly including it here

and run it:

```bash
python /tmp/focuscam.py
```

and point your browser [here](http://fancycamera.local:8000/index.html) and you should see streaming video of whatever the camera's pointing at. You want the camera pointing directly at the centre line of the hat, absolutely square-on:

![camera's eye view](/assets/cameras-eye-view.png)

Fixing the camera with the blu-tack allows for some very subtle manipulation at this point.

### Making a darkroom

It doesn't have to be _completely_ dark, but some darkness certainly helps. I used my full-size camera tripod to make a frame:

![tripod](/assets/tripod.png)

and then draped the darkest bedsheet I could find over it:

![bedsheet](/assets/bedsheet.png)

With the blinds closed and the lights off, it was surprisingly effective.

### Final alignment

You need to make sure that the view underneath the sheet is all good. Put the Hat Pi into `webserver` mode:

```bash
make webserver
```

make sure the streaming is still running on the Camera Pi:

```bash
python /tmp/focuscam.py
```

and inspect the [stream](http://fancycamera.local:8000/index.html). Because I was using an elasticated, fitted sheet, I had some problems with the sheet drooping down and getting in the way of the hat.

Once you're done, `ctrl-c` the streaming script.

## Taking the photos

Everything is now set for taking the photos. Presuming you have the front of the hat facing the camera, on the Camera Pi, do

```bash
cd hatlights/camera
make front
```

and follow the prompts. It will light each light one at a time, first in red and then in white, and take a photo of each. At the end it will light the whole hat and capture a reference image.

Once it's done, you need to rotate the hat 90 degrees (the Lego mount should make this fairly straightforward), and then probably check your alignment again with

```bash
python /tmp/focuscam.py
```

Presuming that's all OK, and you turned the hat clockwise (so its left side is now facing the camera), do:

```bash
make left
```

Then again for `back`, and `right`, and you're done.

Notes:

- the camera's automatic-while-balance is disabled, so all of the lights come out as green in the images
  - this doesn't matter, as all we're after is a bright-spot on the image
  - I presume disabling the AWB is what's causing this, but who knows?

## Processing the photos

Once you have a full set of photos, pull them locally:

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

To help deal with this problem, the `capture.py` script takes an additional photo of each light, lit with `[255, 25, 255]` (e.g. very bright white) and using a much longer exposure time, named `001-long.jpg` or whatever. So to solve for light `55`, for example, from the laptop (not inside the container), try something like

```bash
open ../analysis/left/055*jpg ../analysis/right/055*jpg
```

You should now be looking at the regular and long-exposure photos of light `055`, taken from each side. Presuming at least one of them has a bright spot on it, you just need to work out where it is (by drawing a box in Preview or whatever), then fill in the data in `locations.yaml`, according to these rules:

- for `front`, `x` yields `x`
- for `right`, `x` yields `z`
- for `back`, `image-width - x` yields `x`
- for `left`, `image-width - x` yields `z`

### Lights which are out of position

For reasons I cannot understand (and have given up trying), some lights insist on being _completely_ out of place along one axis. There is a dirty manual fix for these, though:

```bash
cd debug/
sudo PYTHONPATH=../ python dirty_script.py
```

This will trigger waves of light sweeping across the hat

> enable lines `35`, `36` or `37` to select the axis, and _decrease_ the step-size in line `32` to slow it all down

Running this will should expose any rogue lights, as they will light ahead of or behind those close to them. Once you've spotted an offender, mark it somehow (I stuck a little piece of blu-tack to mine), then run another script:

```bash
sudo PYTHONPATH=../ python step_lights.py
```

and `crtl-c` out when it gets to the light you want. Now you have the absolute index of your target, you can home-in on the correct values for it:

```bash
sudo PYTHONPATH=../ python calibrator.py x 1000
```

This will light all lights with an `x` value less than 1000. Adjust this value up and down until you get to the range which should have illuminated the bad light, then put this value in `locations.yaml`. Repeat for any other wonky lights, on any of the axes.

## And we're done

All of this tooling is a bit crufty because it was developed by running it on the hat until it worked. It doesn't have any tests, except the actual test of Are The Lights Correctly Located In Hatspace?
