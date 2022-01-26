from fastcore.all import *
from fastscript.core import call_parse,Param
from .core import *

@call_parse
def fastgpu_poll(
    path:str='.',  # Path containing `to_run` directory
    exit:int=1,  # Exit when `to_run` is empty
):
    "Poll `path` for scripts using `ResourcePoolGPU.poll_scripts`"
    rp = ResourcePoolGPU(path=path)
    rp.poll_scripts(exit_when_empty=exit)

