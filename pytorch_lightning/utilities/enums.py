# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Enumerated utilities"""
from enum import Enum
from typing import List, Optional, Union


class LightningEnum(str, Enum):
    """Type of any enumerator with allowed comparison to string invariant to cases."""

    @classmethod
    def from_str(cls, value: str) -> Optional["LightningEnum"]:
        statuses = [status for status in dir(cls) if not status.startswith("_")]
        for st in statuses:
            if st.lower() == value.lower():
                return getattr(cls, st)
        return None

    def __eq__(self, other: Union[str, Enum]) -> bool:
        other = other.value if isinstance(other, Enum) else str(other)
        return self.value.lower() == other.lower()

    def __hash__(self) -> int:
        # re-enable hashtable so it can be used as a dict key or in a set
        # example: set(LightningEnum)
        return hash(self.value.lower())


class AMPType(LightningEnum):
    """Type of Automatic Mixed Precission used for training.

    >>> # you can match the type with string
    >>> AMPType.APEX == 'apex'
    True
    """

    APEX = "apex"
    NATIVE = "native"


class DistributedType(LightningEnum):
    """Define type of ditributed computing.

    >>> # you can match the type with string
    >>> DistributedType.DDP == 'ddp'
    True
    >>> # which is case invariant
    >>> DistributedType.DDP2 in ('ddp2', )
    True
    """

    @staticmethod
    def interactive_compatible_types() -> List["DistributedType"]:
        """Returns a list containing interactive compatible DistributeTypes"""
        return [
            DistributedType.DP,
            DistributedType.DDP_SPAWN,
            DistributedType.DDP_SHARDED_SPAWN,
            DistributedType.TPU_SPAWN,
        ]

    def is_interactive_compatible(self) -> bool:
        """Returns whether self is interactive compatible"""
        return self in DistributedType.interactive_compatible_types()

    DP = "dp"
    DDP = "ddp"
    DDP2 = "ddp2"
    DDP_CPU = "ddp_cpu"
    DDP_SPAWN = "ddp_spawn"
    TPU_SPAWN = "tpu_spawn"
    DEEPSPEED = "deepspeed"
    HOROVOD = "horovod"
    DDP_SHARDED = "ddp_sharded"
    DDP_SHARDED_SPAWN = "ddp_sharded_spawn"
    DDP_FULLY_SHARDED = "ddp_fully_sharded"


class DeviceType(LightningEnum):
    """Define Device type by its nature - acceleatrors.

    >>> DeviceType.CPU == DeviceType.from_str('cpu')
    True
    >>> # you can match the type with string
    >>> DeviceType.GPU == 'GPU'
    True
    >>> # which is case invariant
    >>> DeviceType.TPU in ('tpu', 'CPU')
    True
    """

    CPU = "CPU"
    GPU = "GPU"
    IPU = "IPU"
    TPU = "TPU"


class GradClipAlgorithmType(LightningEnum):
    """Define gradient_clip_algorithm types - training-tricks.
    NORM type means "clipping gradients by norm". This computed over all model parameters together.
    VALUE type means "clipping gradients by value". This will clip the gradient value for each parameter.

    References:
        clip_by_norm: https://pytorch.org/docs/stable/nn.html#torch.nn.utils.clip_grad_norm_
        clip_by_value: https://pytorch.org/docs/stable/nn.html#torch.nn.utils.clip_grad_value_
    """

    VALUE = "value"
    NORM = "norm"


class AutoRestartBatchKeys(LightningEnum):
    """
    Defines special dictionary keys used to track sampler progress with multiple workers.
    """

    PL_SAMPLERS = "__pl_samplers"
