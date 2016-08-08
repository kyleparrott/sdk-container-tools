import argparse
import distutils
import imp
import mock
import os
import shutil
import sys
import tempfile
import unittest
import yotta

utils = imp.load_source('utils', '/sdk/kubos/test/utils.py')
kubos = imp.load_source('kubos', '/kubos-sdk/kubos-sdk.py')

class SDKToolsBuildTest(unittest.TestCase):
    disco_target = 'stm32f407-disco-gcc'

    def setUp(self):
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        sys.stdout = sys.stderr = open(os.devnull, 'w')
        self.base_dir = tempfile.mkdtemp()
        self.test_dir = os.path.join(self.base_dir, 'test-case')
        shutil.copytree('/examples/kubos-rt-example', self.test_dir, ignore=shutil.ignore_patterns('.git'))
        os.chdir(self.test_dir)
        yotta.build.installAndBuild = mock.MagicMock()
        kubos.link_std_modules = mock.MagicMock()
        new_target = self.disco_target
        new_target_args = argparse.Namespace(target_or_path=new_target,
                                              config=None,
                                              target=new_target,
                                              set_target=new_target,
                                              save_global=False,
                                              no_install=False)
        yotta.target.execCommand(new_target_args, '')


    def test_build(self):
        search_dict = {'target': self.disco_target,
                       'cmake_generator': 'Ninja',
                       'release_build': True}
        target_source = '/usr/lib/yotta_targets/target-stm32f407-disco-gcc'
        target_dest_dir = os.path.join(self.test_dir, 'yotta_targets')
        shutil.copytree(target_source, target_dest_dir, ignore=shutil.ignore_patterns('.git'))
        kubos._build('')
        yotta.build.installAndBuild.assert_called()
        call_dict = utils.get_arg_dict(yotta.build.installAndBuild.call_args_list)
        self.assertTrue(search_dict <= call_dict)


    def tearDown(self):
        shutil.rmtree(self.test_dir)
        sys.stdout = self.stdout
        sys.stderr = self.stderr


if __name__ == '__main__':
    unittest.main()
