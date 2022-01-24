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

## Focus the camera

First, make sure the hat is running in a fully-lit mode.

Grab the script from [here](https://randomnerdtutorials.com/video-streaming-with-raspberry-pi-camera/):

```bash
curl https://raw.githubusercontent.com/RuiSantosdotme/Random-Nerd-Tutorials/master/Projects/rpi_camera_surveillance_system.py -o /tmp/focuscam.py
```

and run it:

```bash
python /tmp/focuscam.py
```

and point your browser [here](http://fancycamera.local:8000/index.html)

Now:

- Point the camera at the front of the hat
- Move close enough that the hat fills the frame
- Focus so the lights are fairly sharp
- Turn down the exposure so only the lights are visible

## Capture the images

On the Hat Pi, put it in `webserver` mode:

```bash
cd ~/hatlights
make webserver
```

Once that's running, on the Camera Pi, start the capture:

```bash
make front
```

and wait while it takes <number-of-lights> photographs. Then:

- Rotate the hat 90 degress (so the camera is now facing its left-hand side)
- Put the hat back in a fully-lit mode:
  - `make restart-services`
- Restart the camera streaming:
  - `python /tmp/focuscam.py`
- And adjust things so that the hat is again filling the frame

Now capture the next set of images:

```bash
make left
```

And wait, then turn it again and run the above steps for `back` and `right`.
