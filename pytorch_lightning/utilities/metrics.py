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
"""Helper functions to operate on metric values. """
import numbers
from typing import Any

import torch

from pytorch_lightning.utilities.apply_func import apply_to_collection
from pytorch_lightning.utilities.exceptions import MisconfigurationException


def metrics_to_scalars(metrics: Any) -> Any:
    """
    Recursively walk through a collection and convert single-item tensors to scalar values

    Raises:
        MisconfigurationException:
            If ``value`` contains multiple elements, hence preventing conversion to ``float``
    """

    def to_item(value: torch.Tensor) -> numbers.Number:
        if value.numel() != 1:
            raise MisconfigurationException(
                f"The metric `{value}` does not contain a single element" f" thus it cannot be converted to float."
            )
        return value.item()

    return apply_to_collection(metrics, torch.Tensor, to_item)
