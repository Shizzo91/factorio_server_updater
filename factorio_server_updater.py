#!/usr/bin/env python3
# @Autor Joel
# region imports
import requests
import re
import subprocess
import shlex
import tempfile
from io import BytesIO
# endregion
# region versions check
def currend_version() -> str:
    """
    get the currend version of factorio server
    :return: version
    :rtype: str
    """
    version_command = "/opt/factorio/bin/x64/factorio --version"
    shell_version_command = shlex.split(version_command)
    version_popen = subprocess.Popen(
        shell_version_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if version_popen:
        pattern = re.compile("[\sa-z:]*(?P<version>[\d]+\.[\d]+\.[\d]+)", re.IGNORECASE)
        match = pattern.match(version_popen.communicate()[0].decode())
        if match is not None:
            return match.group('version')
    return ""

def last_verion() -> str:
    """
    get the
    :return: version
    :rtype: str
    """
    url = "https://factorio.com/api/latest-releases"
    request = requests.get(url)
    return request.json().get('stable', {}).get('headless', "")
# endregion
def update(last_version: str):
    url = f"https://www.factorio.com/get-download/{last_version}/headless/linux64"
    request = requests.get(url)
    tar = BytesIO(request.content)
    tmp_file = tempfile.NamedTemporaryFile("w+b")
    tmp_file.write(tar.getvalue())

    untar_command = f"tar -xvf \"{tmp_file.name}\" -C \"/opt\""
    shell_untar_command = shlex.split(untar_command)
    untar_popen = subprocess.Popen(
        shell_untar_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    untar_popen.communicate()

    chown_command = f"chown -R factorio:factorio \"/opt/factorio\""
    shell_chown_command = shlex.split(chown_command)
    chown_popen = subprocess.Popen(
        shell_chown_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    chown_popen.communicate()

def main():
    last_v = last_verion()
    currend_v = currend_version()
    latest_v = max(last_v, currend_v)
    if currend_v != latest_v:
        update(latest_v)

if __name__ == '__main__':
    main()