# Pull the photos

```bash
rsync -av pi@fancycamera.local:hat-analysis/ /opt/hat-analysis/
```

# Rotate the photos

The camera was inverted for ease-of-positioning so first we need to rotate everything:

```bash
bash rotate.sh
```

> I mean, we don't _need_ to, but it makes thinking about the following steps much easier

# Find the bright spots

Now we analyse the photos to find the bright spot in each:

```bash
python find_bright_spots.py
```

A "bright spot" here is one which basically blows-out the camera's auto-exposure

Notes:

- If the camera is correctly adjusted, each photo should have at most one bright spot
- If there's no such spot, we assume that light was on the far-side of the hat, and we ignore that photo

So now for each photo with a bright spot, we have some `json` like:

```json
{ "x": 623, "y": 260 }
```

This is purely the location of the brightest pixel in the photo, we'll do some smarter analysis next:
