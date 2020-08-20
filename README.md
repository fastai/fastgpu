# fastgpu
> A queue service for quickly developing scripts that use all your GPUs efficiently


`fastgpu` provides a single command, `fastgpu_poll`, which polls a directory to check for scripts to run, and then runs them on the first available GPU. If no GPUs are available, it waits until one is. If more than one GPU is available, multiple scripts are run in parallel, one per GPU.

An API is also provided for polling programmatically, which is extensible for assigning other resources to processes besides GPUs. For details on the API, see the docs for `core`.

## Install

`pip install fastgpu`

## How to use

`--help` provides command help:

```
$ fastgpu_poll --help
usage: fastgpu_poll [-h] [--path PATH] [--exit EXIT]

Poll `path` for scripts using `ResourcePoolGPU.poll_scripts`

optional arguments:
  -h, --help   show this help message and exit
  --path PATH  Path containing `to_run` directory
  --exit EXIT  Exit when `to_run` is empty
```

`path` defaults to the current directory. The path should contain a subdirectory `to_run` containing executable scripts you wish to run. It should not contain any other files, although it can contain subdirectories (which are ignored).

`fastgpu_poll` will run each script in `to_run` in sorted order. Each script will be assigned to one GPU. The `CUDA_VISIBLE_DEVICES` environment variable will be set to the ID of this GPU in the script's subprocess. In addition, the `FASTGPU_ID` environment variable will also be set to this ID.

Once a script is selected to be run, it is moved into a directory called `running`. Once it's finished, it's moved into `complete` or `fail` as appropriate. stdout and stderr are captured to files with the same name as the script, plus `stdout` or `stderr` appended.

If `exit` is `1` (which is the default), then once all scripts are run, `fastgpu_poll` will exit. If it is `0` then `fastgpu_poll` will continue running until it is killed; it will keep polling for any new scripts that are added to `to_run`.

To limit the GPUs available to fastgpu, set [CUDA_VISIBLE_DEVICES](https://devblogs.nvidia.com/cuda-pro-tip-control-gpu-visibility-cuda_visible_devices/) before polling, e.g.:

    CUDA_VISIBLE_DEVICES=2,3 fastgpu_poll script_dir
