import json
import subprocess

module_data = json.load(open('/kubos-sdk/module.json', 'r'))

ver_str = "v%s" % module_data['version']
sdk_working_path = "/kubos-sdk"
dist_working_path = "/kubos-sdk/dist"

subprocess.check_output(["git", "checkout", ver_str], cwd=sdk_working_path)

subprocess.check_output(["./repo", "init", "-u", "git://github.com/openkosmosorg/kubos-manifest", "-m", "docker-manifest.xml", "-b", "refs/tags/%s" % ver_str], cwd=dist_working_path)

subprocess.check_output(["./repo", "sync"], cwd=dist_working_path)