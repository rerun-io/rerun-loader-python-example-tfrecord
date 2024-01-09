# rerun-loader-python-example-tfrecord
This is an example data-loader plugin that lets you view a TFRecord of TFEvents (i.e., tensorboard files) in the [Rerun](https://github.com/rerun-io/rerun/) Viewer.
It uses the [external data loader mechanism](https://www.rerun.io/docs/howto/open-any-file#external-dataloaders) to add this capability to the viewer without modifying the viewer itself.

TODO put video here

External data loaders are executables that are available to the Rerun Viewer via the `PATH` variable, with a name that starts with `rerun-loader-`.

This example is written in Python, and uses [TensorFlow](https://www.tensorflow.org/) to read the files. The events are then logged to Rerun.

> NOTE: Not all events are supported yet. Scalars, images, text, and tensors should work. Unsupported events are skipped.

## Installing the Rerun Viewer
The simplest option is just:
```bash
pip install rerun-sdk
```
Read [this guide](https://www.rerun.io/docs/getting-started/installing-viewer) for more options.

## Installing the plugin
### Installing pipx

The most robust way to install the plugin to your `PATH` is using [pipx](https://pipx.pypa.io/stable/).

If you don't have `pipx` installed on your system, you can follow the official instructions [here](https://pipx.pypa.io/stable/installation/).


## Try it out
### Download an example `xxx.tfevents.xxx` file
```bash
curl -OL TODO make minimal example to push to repo
```

### Open in the Rerun Viewer
You can either first open the viewer, and then open the file from there using drag-and-drop or the menu>open… dialog,
or you can open it directly from the terminal like:
```bash
rerun events.tfevents.example
```
