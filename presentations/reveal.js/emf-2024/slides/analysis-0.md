## Analysing the photos

`{ "x": 623, "y": 260 }` <!-- .element: class="fragment fade-right" data-fragment-index="1" -->

Notes:

Now we run the photos through OpenCV. Each photo should have at most one bright spot - if there's no spot on a given photo, we presume the light was on the far side of the hat and just move on.

So after this, we get a little bit of JSON like this for each photo -click-

Now we take all these little JSON objects and run them through another script to do some transformations and generate this YAML
