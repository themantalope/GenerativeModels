# Copyright (c) MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import unittest

import numpy as np
import torch
from parameterized import parameterized

from generative.metrics import MMD

TEST_CASES = [
    [
        {"y_transform": None, "y_pred_transform": None},
        {"y": torch.ones([3, 3, 144, 144]), "y_pred": torch.ones([3, 3, 144, 144])},
        0.0,
    ],
    [
        {"y_transform": None, "y_pred_transform": None},
        {"y": torch.ones([3, 3, 144, 144, 144]), "y_pred": torch.ones([3, 3, 144, 144, 144])},
        0.0,
    ],
]


class TestMMDMetric(unittest.TestCase):
    @parameterized.expand(TEST_CASES)
    def test_results(self, input_param, input_data, expected_val):
        results = MMD(**input_param)._compute_metric(**input_data)
        np.testing.assert_allclose(results.detach().cpu().numpy(), expected_val, rtol=1e-4)

    def test_if_inputs_different_shapes(self):
        with self.assertRaises(ValueError):
            MMD()(torch.ones([3, 3, 144, 144]), torch.ones([3, 3, 145, 145]))


if __name__ == "__main__":
    unittest.main()
