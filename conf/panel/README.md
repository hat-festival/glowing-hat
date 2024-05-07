# Generate new words

This is crufty as fuck, but, from the `make_words` directory:

```
make build
```

Then

```
docker run --volume $(pwd)/../conf/panel/strings/:/opt/output/ word-maker bar "foo bar baz"
```

will make the string `foo bar baz` at a file called `strings/bar.yaml`
