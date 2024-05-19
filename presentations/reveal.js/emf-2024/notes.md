# Exploring HatSpace

Hello EMF. Are we having a good time?

---

### I glued 100 WS2812 NeoPixels to a hat then mapped them in 3D space

My name is Sam. I made this hat for EMF 2022 and I found myself answering so many questions about it that I basically started writing this lightning talk in my head. So now here I am to tell you about it.

---

## Components

It's all made with a load of stuff you can mostly buy off eBay. The white hat was originally supposed to be a prototype, because I have a much nicer smoked acrylic hard-hat that I had intended to use, but by the time I'd stuck everything together it was too late, and the prototype had made it into production. And actually, in hindsight, the idea of making a prototype is fairly ludicrous, because then I'd have two of these, which is arguably two too many anyway.

---

## Not a timing device 

I hot-glued the lights to the hat, turning in a random(ish) direction after I'd glued-down each one, attempting to move towards empty space each time. I also managed to stick 2 or 3 of them on backwards because I'm an idiot, and of course by the time I was done there were little wisps of hot-glue all round the room, a common experience for many of us, I'm sure, during EMF season.

One day I'm gonna get rich and famous when I invent a hot-glue gun that doesn't do this.

I cable-tied the Pi to the power-bank and wired everything up, producing this device, which you absolutely would not want to try to take through an airport.

---

## Mapping the lights

So this is where the interesting stuff starts: we need to take 400 very precise photos of the hat. First we need some method of mounting the hat and the camera a fixed distance apart and absolutely square-on to each other. So of course I used Lego.

So we build a little rig like this, and then once everything is securely mounted, in a reasonably dark room, we run a script that lights the lights, one at a time, and takes a photo. Once we've got our 100 photos from the front, we turn the hat through 90 degrees, and take 100 more photos. And then again, and again, for all four sides.

---

## Analysing the photos

Now we run the photos through OpenCV, to find the bright spots. Each photo should have at most one bright spot - if there's no spot on a given photo, we presume the light was on the far side of the hat and just move on.

So after this, we get a little bit of JSON like this for each photo.

Now we take all these little JSON objects and run them through another script to do some transformations...

---

## Analysing the photos

And we get some YAML like this, which represents the absolute pixel locations of each light. Some of them come out as fractional, because we got multiple values for a given light on a given axis, so we take the average.

And some of them only have two out of three axes. This happens for reasons which I gave up trying to understand, but it turns out it doesn't really matter - as long as we have correct values for most of the lights, we can fill in the gaps by hand. So there I was, sticking bits of blue-tac to the problem lights, then lighting up the nearby lights in the Python console, and slowly homing in on the correct positions. It's not a terrible hack if it works.

We run these through one more transformation to scale these numbers so x runs from -1 to +1 across the hat, z runs from -1 to +1 front-to-back, and then because the hat is mostly the top-half of a sphere, the y-values run from 0 at the base to +1 at the top. And now the lights are fully-mapped in hat-space, and we can say things like 'light up all the lights for which z is greater than zero' or 'sort the entire hat along the y-axis'.

---

## Pixel metadata

So each pixel is represented by some nice metadata like this. We can also work out the angle of each pixel in each of the x, y and z planes, using some half-remembered trigonometry.

---

## Matt Parker's Christmas tree

All of this was heavily inspired by Matt Parker's Christmas tree, where he draped 500 NeoPixels over his tree and then located them in 3D space. If you haven't seen this, it's well worth watching, and it's safe to say that without this I wouldn't have known where to start.

---

## Hue, saturation, value

The NeoPixels present themselves as a Python list, where you can just assign an RGB triple to an index like this and the first light turns magenta. This is intuitive, I suppose, but it can lead us down a sub-optimal path - the first iteration of the hat, from 2022, dealt _only_ in RGBs, which led to some horrendously fiddly maths when trying to fade between colours, for example.

So for the 2024 edition, I'm using the HSV model, which is so much smoother - the hue is just a circle with red at 0.0, green at 1/3 and blue at 2/3, with all the other colours in between, and the python colorsys module knows how to translate between the different models.

Each pixel gets some more metadata and we adjust the hue, saturation and value fields when preparing to light the hat. A pixel never knows what its RGB triple is - that's essentially an artefact that gets calculated as late as possible, at the moment we actually send data to the real LEDs.

Doing it this way also enables us to easily do gamma-correction, which is something I've long pretended to understand, and adjust the brightness of the hat - we just apply a brightness factor to the value as we calculate the RGB. The 2022 edition had no brightness control, which led to me blinding people. 

---

## Turning sound into light

I attached a USB microphone to it and attempted to implement Fast Fourier Transforms. I had presumed that, like with gamma-correction, if I pretended to understand FFTs for long enough, that eventually I would, but it didn't work out. As you can see, it does respond to sound, but not in any sort of reliable way. In my head, I had imagined it basically jumping up and down to the sound of a kick drum, but it just does this. This might be because I bought a very cheap USB mic, but I think it's more likely that I've badly half-assed my FFT implementation. If anybody has any insights or experience with this, and wants to help me hack on some terrible Python, please come and find me afterwards.

---

## When all you have is a hat...

A Hat is just an array of pixels - the fact that it's wrapped around a hat is kind of incidental, which means it's isomorphic to lots of other NeoPixel things, and for many of these things it's much easier to establish the positions of each light. So I've had the same code running on these flat LED panels.

---

## When all you have is a hat...

One of these little cube:bit things.

---

## When all you have is a hat...

And the string of LEDs attached to our tent over at Hat Village.

---

# What have we learned?

You should totally do something like this because before I started, I knew very little about any of this stuff, and now I have Opinions about many new things. This is the most Programming Purely For The Art Of It thing that I've done in a while, and if that's not in the spirit of EMF, I don't know what is.

Also check carefully before you glue your pixels down, and maybe don't buy the cheapest USB microphone on eBay.

---

# Links

---