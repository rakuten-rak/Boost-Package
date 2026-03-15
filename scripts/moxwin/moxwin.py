"""
Windows tool functions

Copyright (c) 2023 Moxibyte GmbH

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import os
import json
import subprocess

def GetCodepage():
    return "".join(filter(str.isalnum, subprocess.getoutput('chcp').split(':')[-1].strip()))
    
def FindLatestVisualStudio():
    vswhere = os.getenv('programfiles(x86)') + '\\Microsoft Visual Studio\\Installer\\vswhere.exe'
    try:
        out = subprocess.check_output((vswhere, '-latest', '-nocolor', '-format', 'json'))
    except FileNotFoundError:
        raise ValueError("vswhere.exe not found. Please install Visual Studio or the Build Tools.")
    return json.loads(out.decode(f'cp{GetCodepage()}'))

def GetVisualStudioYearNumber(vswhere):
    if not vswhere:
        raise ValueError("No Visual Studio installation found (vswhere returned no results).")

    installationVersion = str(vswhere[0].get('installationVersion', '')).split('.')[0]
    if installationVersion == '15':
        return '2017'
    if installationVersion == '16':
        return '2019'

    # Premake currently supports up to VS 2022 (internal version 17).
    # Treat any newer Visual Studio (18+, e.g. VS 2025/2026) as VS 2022 for generator purposes.
    try:
        if int(installationVersion) >= 17:
            return '2022'
    except ValueError:
        pass

    raise ValueError(
        f"Unsupported Visual Studio version '{installationVersion}'. "
        "Please install Visual Studio 2017, 2019, or 2022."
    )

def GetVisualStudioPath(vswhere):
    return vswhere[0]['installationPath']

