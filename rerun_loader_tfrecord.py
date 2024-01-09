#!/usr/bin/env python3
"""Example of an executable data-loader plugin for the Rerun Viewer for tensorboard files."""
from __future__ import annotations

from tensorflow.python.summary.summary_iterator import summary_iterator
import rerun as rr  # pip install rerun-sdk
import argparse
import os

def log_tb_summary_file(filepath: str) -> None:
    """Log a tensorboard summary file to Rerun."""
    for event in summary_iterator(filepath):
        if not event.HasField("summary"):
            continue

        rr.set_time_sequence("step", event.step)
        rr.set_time_seconds("wall_time", event.wall_time)

        value = event.summary.value[0]
        if value.HasField("image"):
            name = event.summary.value[0].tag
            image_raw = event.summary.value[0].image.encoded_image_string
            rr.log(name, rr.ImageEncoded(contents=image_raw))
        elif value.HasField("simple_value"):  # scalar
            # Scalar
            name = event.summary.value[0].tag
            value = event.summary.value[0].simple_value
            rr.log(name, rr.TimeSeriesScalar(value))

        # here we could also handle other types of data, like histograms, audio, text, etc.


# The Rerun Viewer will always pass these two pieces of information:
# 1. The path to be loaded, as a positional arg.
# 2. A shared recording ID, via the `--recording-id` flag.
#
# It is up to you whether you make use of that shared recording ID or not.
# If you use it, the data will end up in the same recording as all other plugins interested in
# that file, otherwise you can just create a dedicated recording for it. Or both.
parser = argparse.ArgumentParser(
    description="""
This is an example executable data-loader plugin for the Rerun Viewer.
Any executable on your `$PATH` with a name that starts with `rerun-loader-` will be
treated as an external data-loader.

This example will load tensorboard summary files (tfrecord files with tfevents) and log them to Rerun,
and return a special exit code to indicate that it doesn't support anything else.

To try it out, copy it in your $PATH as `rerun-loader-python-example-tfrecord`,
then open a tensorboard summary file with Rerun (`rerun events.out.tfevents.xxx`).
    """
)
parser.add_argument("filepath", type=str)
parser.add_argument("--recording-id", type=str)
args = parser.parse_args()


def main() -> None:
    is_file = os.path.isfile(args.filepath)
    is_tb_summary_file = ".tfevents" in args.filepath

    # Inform the Rerun Viewer that we do not support that kind of file.
    if not is_file or not is_tb_summary_file:
        exit(rr.EXTERNAL_DATA_LOADER_INCOMPATIBLE_EXIT_CODE)

    rr.init("rerun_example_external_data_loader_tfrecord", recording_id=args.recording_id)
    # The most important part of this: log to standard output so the Rerun Viewer can ingest it!
    rr.stdout()

    log_tb_summary_file(args.filepath)


if __name__ == "__main__":
    main()
