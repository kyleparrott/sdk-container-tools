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


class SDKToolsTargetTest(unittest.TestCase):
    disco_target = 'stm32f407-disco-gcc'

    def setUp(self):
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        sys.stdout = sys.stderr = open(os.devnull, 'w')
        self.base_dir = tempfile.mkdtemp()
        self.test_dir = os.path.join(self.base_dir, 'test-case')
        shutil.copytree('/examples/kubos-rt-example', self.test_dir, ignore=shutil.ignore_patterns('.git'))
        os.chdir(self.test_dir)
        kubos.link_global_targets()
        yotta.target.execCommand = mock.MagicMock()
        yotta.target.displayCurrentTarget = mock.MagicMock()


    def setup_set_target(self):
        new_target = self.disco_target
        source_dir = '/usr/local/lib/yotta_targets/stm32f407-disco-gcc'
        dest_dir = os.path.join(self.test_dir, 'yotta_targets', 'target-stm32f407-disco-gcc')
        shutil.copytree(source_dir, dest_dir, ignore=shutil.ignore_patterns('.git'))
        with open(os.path.join(self.test_dir, '.yotta.json'), 'w') as yotta_json:
            yotta_json.write(yotta_json_template)


    def test_show_target_none_set(self):
        with self.assertRaises(SystemExit):
            kubos.show_target()


    def test_show_target(self):
        search_dict = {'target': self.disco_target,
                       'set_target': None}
        self.setup_set_target()
        kubos.show_target()
        call_dict = utils.get_arg_dict(yotta.target.displayCurrentTarget.call_args_list)
        yotta.target.displayCurrentTarget.assert_called()
        self.assertTrue(search_dict <= call_dict)


    def test_set_target(self):
        new_target = 'msp430f5529-gcc'
        search_dict = {'taget': new_target,
                       'set_target': new_target}
        self.setup_set_target()
        kubos.set_target(new_target)
        yotta.target.execCommand.assert_called()
        call_dict = utils.get_arg_dict(yotta.target.execCommand.call_args_list)
        self.assertTrue(search_dict <= call_dict)


    def tearDown(self):
        shutil.rmtree(self.test_dir)
        sys.stdout = self.stdout
        sys.stderr = self.stderr



if __name__ == '__main__':
    unittest.main()

