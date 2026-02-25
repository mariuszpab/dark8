from .exec_ops import register as register_exec_ops
from .file_ops import register as register_file_ops
from .flow_ops import register as register_flow_ops
from .patch_ops import register as register_patch_ops


def register_all_commands():
    register_file_ops()
    register_flow_ops()
    register_exec_ops()
    register_patch_ops()
