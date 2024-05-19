## Hue, saturation, value
```python
>>> import board, neopixel
>>> lights = neopixel.NeoPixel(board.D21, 100)
>>> lights[0] = (255, 0, 255)
```

```python
{
  "index": 10,
  "x": -0.01828410689170183,
  "y": 0.21729957805907174,
  "z": 0.7158931082981715,
  "angles": {
    "x": 73.11504937908333,
    "y": 358.53696809142565,
    "z": 94.80967471203176
  },
  "hue": 0.43,
  "saturation": 1.0,
  "value": 0.5,
}
```

Notes:

The NeoPixels present themselves as a Python list, where you can just assign an RGB triple to an index like this and the first light turns magenta. This is intuitive, I suppose, but it can lead us down a sub-optimal path - the first iteration of the hat, from 2022, dealt _only_ in RGBs, which led to some horrendously fiddly maths when trying to fade between colours, for example.

So for the 2024 edition, I'm using the HSV model, which is so much smoother - the hue is just a circle with red at 0.0, green at 1/3 and blue at 2/3, with all the other colours in between, and the python colorsys module knows how to translate between the different models.

Each pixel gets some more metadata and we adjust the hue, saturation and value fields when preparing to light the hat. A pixel never knows what its RGB triple is - that's essentially an artefact that gets calculated as late as possible, at the moment we actually send data to the real LEDs.

Doing it this way also enables us to easily do gamma-correction, which is something I've long pretended to understand, and adjust the brightness of the hat - we just apply a brightness factor to the value as we calculate the RGB. The 2022 edition had no brightness control, which led to me blinding people. 
