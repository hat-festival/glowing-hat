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

First, put the hat in `webserver` mode; on the Hat Pi:

```bash
cd ~/hatlights
make webserver
```

and light it up; on the Camera Pi:

```bash
cd ~/hatlights/camera
make light-hat
```

> All of the lights on the hat should now be on

Grab the script from [here](https://randomnerdtutorials.com/video-streaming-with-raspberry-pi-camera/):

```bash
curl https://raw.githubusercontent.com/RuiSantosdotme/Random-Nerd-Tutorials/master/Projects/rpi_camera_surveillance_system.py -o /tmp/focuscam.py
```

> This code has no visible license so I'm not directly including it here

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

Presuming the Hat is still in `webserver` mode, on the Camera Pi, start the capture:

```bash
cd ~/hatlights/camera
make front
```

Follow the prompts, then wait while it takes <number-of-lights> photographs. Then:

- Rotate the hat 90 degress (so the camera is now facing its left-hand side)
- Restart the camera streaming:
  - `python /tmp/focuscam.py`
- And adjust things so that the hat is again filling the frame

Now capture the next set of images:

```bash
make left
```

And wait, then turn it again and run the above steps for `back` and `right`.

So now you should have a whole load of images. Pull them onto your laptop, as a peer of this repo:

```bash
rsync -av pi@fancycamera.local:hat-analysis ../
```
