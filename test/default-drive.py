#!/usr/bin/env python
#
# __COPYRIGHT__
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

"""
This test verifies (on Windows systems) that specifying an
absolute path name without a drive letter uses the SConstruct
file's drive as the default.
"""

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

import os
import os.path
import string
import sys

import TestSCons

test = TestSCons.TestSCons()

if sys.platform != 'win32':
    test.pass_test()

test.subdir('src')

test.write(['src', 'SConstruct'], """
def cat(env, source, target):
    target = str(target[0])
    source = map(str, source)
    f = open(target, "wb")
    for src in source:
        f.write(open(src, "rb").read())
    f.close()

env = Environment(BUILDERS={'Build':Builder(action=cat)})
env.Build('../build/file.out', 'file.in')
""")

test.write(['src', 'file.in'], "src/file.in\n")

build_file_out = test.workpath('build', 'file.out')

print os.path.splitdrive(build_file_out)[1]
test.run(chdir = 'src',
         arguments = os.path.splitdrive(build_file_out)[1])

test.must_match(['build', 'file.out'], "src/file.in\n")

test.pass_test()
