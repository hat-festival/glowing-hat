To create new `strings` for the `words` mode (only makes sense on the `panel`):

```bash
bash create.sh foo "Hat Village EMF2024"
```

will create a file at `conf/panel/strings/foo.yaml` containing `Hat Village EMF2024`

Then set the `modes.yaml` like:

```yaml
words:
  string: foo
```