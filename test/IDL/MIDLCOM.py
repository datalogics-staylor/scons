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
Test the ability to configure the $MIDLCOM construction variable.
"""

import TestSCons

_python_ = TestSCons._python_

test = TestSCons.TestSCons()



test.write('mymidl.py', """
import sys
outfile = open(sys.argv[1], 'wb')
for f in sys.argv[2:]:
    infile = open(f, 'rb')
    for l in filter(lambda l: l != '/*midl*/\\n', infile.readlines()):
        outfile.write(l)
sys.exit(0)
""")

test.write('SConstruct', """
env = Environment(tools=['default', 'midl'],
                  MIDLCOM = r'%(_python_)s mymidl.py $TARGET $SOURCES')
env.TypeLibrary(target = 'aaa', source = 'aaa.idl')
""" % locals())

test.write('aaa.idl', "aaa.idl\n/*midl*/\n")

test.run(arguments = '.')

test.must_match('aaa.tlb', "aaa.idl\n")



test.pass_test()
