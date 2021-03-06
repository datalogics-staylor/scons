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
Verify that initializing a construction environment with just the
g++ tool uses the CCFLAGS.
"""

import TestSCons

test = TestSCons.TestSCons()

test.write('SConstruct', """
env = Environment(tools = ['g++'], CXX = 'g++')
env.Object(target = 'test.obj', source = 'test.cxx')
env.MergeFlags('+for_CCFLAGS -Wp,-for_CPPFLAGS')
""")

test.write('test.cxx', "test.cxx\n")

expect = """\
g++ -o test.obj -c +for_CCFLAGS -Wp,-for_CPPFLAGS test.cxx
"""

test.run(arguments = '-Q -n test.obj', stdout=expect)

test.pass_test()
