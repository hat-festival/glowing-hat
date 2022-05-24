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

And how did I come up with that 58-stud distance?

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

Once you're done here, move on to [analysing the data](/analysis/README.md).
