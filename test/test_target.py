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

import argparse
import imp
import distutils
import mock
import os
import shutil
import sys
import tempfile
import unittest
import yotta

dir_name = os.path.dirname(os.path.abspath(__file__))
util_file = os.path.join(dir_name, 'utils.py')
test_utils = imp.load_source('utils', util_file)
utils = imp.load_source('utils', '/sdk/kubos/test/utils.py')
kubos = imp.load_source('kubos', '/kubos-sdk/kubos-sdk.py')

# This test is only supposed to run inside the ci-test container (inherits from
# kubostech/kubos-sdk container. That's why there are hard-coded absolute paths
# in the test

yotta_json_template = '''
{
    "build": {
          "target": "stm32f407-disco-gcc,*",
          "targetSetExplicitly": true
    }
}
'''

class SDKToolsTargetTest(test_utils.ContainerTestCase):

    def _setUp(self):
        test_utils.copy_example(self.test_dir)
        os.chdir(self.test_dir)
        kubos.link_global_targets()
        yotta.target.execCommand = mock.MagicMock()
        yotta.target.displayCurrentTarget = mock.MagicMock()


    def setup_set_target(self):
        new_target = test_utils.disco_target
        source_dir = os.path.join('/', 'usr', 'local', 'lib', 'yotta_targets', 'stm32f407-disco-gcc')
        dest_dir = os.path.join(self.test_dir, 'yotta_targets', 'target-stm32f407-disco-gcc')
        shutil.copytree(source_dir, dest_dir, ignore=shutil.ignore_patterns('.git'))
        with open(os.path.join(self.test_dir, '.yotta.json'), 'w') as yotta_json:
            yotta_json.write(yotta_json_template)


    def test_show_target_none_set(self):
        with self.assertRaises(SystemExit):
            kubos.show_target()


    def test_show_target(self):
        search_dict = {'target': test_utils.disco_target,
                       'set_target': None}
        self.setup_set_target()
        kubos.show_target()
        call_dict = utils.get_arg_dict(yotta.target.displayCurrentTarget.call_args_list)
        yotta.target.displayCurrentTarget.assert_called()
        self.assertTrue(search_dict <= call_dict)


    def test_set_target(self):
        new_target = 'msp430f5529-gcc'
        search_dict = {'target': new_target,
                       'set_target': new_target}
        self.setup_set_target()
        kubos.set_target(new_target)
        yotta.target.execCommand.assert_called()
        call_dict = utils.get_arg_dict(yotta.target.execCommand.call_args_list)
        self.assertTrue(search_dict <= call_dict)


if __name__ == '__main__':
    unittest.main()

