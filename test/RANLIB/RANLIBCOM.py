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

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

"""
Test the ability to configure the $RANLIBCOM construction variable.
"""

import TestSCons

_python_ = TestSCons._python_

test = TestSCons.TestSCons()

ranlib = test.detect('RANLIB', 'ranlib')

if not ranlib:
    test.skip_test("Could not find 'ranlib', skipping test.\n")



test.write('myar.py', """
import sys
outfile = open(sys.argv[1], 'wb')
for f in sys.argv[2:]:
    infile = open(f, 'rb')
    for l in filter(lambda l: l != '/*ar*/\\n', infile.readlines()):
        outfile.write(l)
sys.exit(0)
""")

test.write('myranlib.py', """
import sys
lines = open(sys.argv[1], 'rb').readlines()
outfile = open(sys.argv[1], 'wb')
for l in filter(lambda l: l != '/*ranlib*/\\n', lines):
    outfile.write(l)
sys.exit(0)
""")

test.write('SConstruct', """
env = Environment(tools=['default', 'ar'],
                  ARCOM = r'%(_python_)s myar.py $TARGET $SOURCES',
                  RANLIBCOM = r'%(_python_)s myranlib.py $TARGET',
                  LIBPREFIX = '',
                  LIBSUFFIX = '.lib')
env.Library(target = 'output', source = ['file.1', 'file.2'])
""" % locals())

test.write('file.1', "file.1\n/*ar*/\n/*ranlib*/\n")
test.write('file.2', "file.2\n/*ar*/\n/*ranlib*/\n")

test.run(arguments = '.')

test.must_match('output.lib', "file.1\nfile.2\n")



test.pass_test()
