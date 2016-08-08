import imp
import os
import shutil
import sys
import tempfile
import unittest

kubos = imp.load_source('kubos', '/kubos-sdk/kubos-sdk.py')

# This test is only supposed to run inside the ci-test container (inherits from
# kubostech/kubos-sdk container. That's why there are hard-coded absolute paths
# in the test

class SDKToolsInitTest(unittest.TestCase):
    def setUp(self):
        #Hide stdout and stderr for this test
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        sys.stdout = sys.stderr = open(os.devnull, 'w')
        self.base_dir = tempfile.mkdtemp()
        self.test_dir = os.path.join(self.base_dir, 'test-case')
        os.makedirs(self.test_dir)
        os.chdir(self.test_dir)


    def test_init(self):
        kubos._init('test-case')
        module_json = os.path.join(self.test_dir, 'test-case', 'module.json')
        main_c = os.path.join(self.test_dir, 'test-case', 'source', 'main.c')
        self.assertTrue(os.path.isfile(module_json))
        self.assertTrue(os.path.isfile(main_c))


    def tearDown(self):
        shutil.rmtree(self.base_dir)
        sys.stdout = self.stdout
        sys.stderr = self.stderr


if __name__ == '__main__':
    unittest.main()

