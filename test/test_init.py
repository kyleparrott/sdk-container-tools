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

import imp
import os
import shutil
import sys
import tempfile
import unittest

dir_name = os.path.dirname(os.path.abspath(__file__))
util_file = os.path.join(dir_name, 'utils.py')
test_utils = imp.load_source('utils', util_file)
kubos = imp.load_source('kubos', '/kubos-sdk/kubos-sdk.py')

# This test is only supposed to run inside the ci-test container (inherits from
# kubostech/kubos-sdk container. That's why there are hard-coded absolute paths
# in the test

class SDKToolsInitTest(test_utils.ContainerTestCase):
    def setUp(self):
        super(SDKToolsInitTest, self).setUp()
        os.mkdir(self.test_dir)
        os.chdir(self.test_dir)


    def test_init(self):
        kubos._init(self.proj_name)
        module_json = os.path.join(self.test_dir, self.proj_name, 'module.json')
        main_c = os.path.join(self.test_dir, self.proj_name, 'source', 'main.c')
        self.assertTrue(os.path.isfile(module_json))
        self.assertTrue(os.path.isfile(main_c))


if __name__ == '__main__':
    unittest.main()

