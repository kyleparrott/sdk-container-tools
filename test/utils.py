# Kubos SDK
# Copyright (C) 2016 Kubos Corporation
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

import os
import shutil
import sys
import tempfile
import unittest

disco_target = 'stm32f407-disco-gcc'

class ContainerTestCase(unittest.TestCase):
    proj_name = 'test-case'

    def setUp(self):
        #Hide stdout and stderr for this test
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        sys.stdout = sys.stderr = open(os.devnull, 'w')
        self.base_dir = tempfile.mkdtemp()
        self.test_dir = os.path.join(self.base_dir, self.proj_name)


    def tearDown(self):
        shutil.rmtree(self.base_dir)
        sys.stdout = self.stdout
        sys.stderr = self.stderr


def copy_example(dest):
    shutil.copytree('/examples/kubos-rt-example', dest, ignore=shutil.ignore_patterns('.git'))
