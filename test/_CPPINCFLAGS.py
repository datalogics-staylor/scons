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
Test that we can expand $_CPPINCFLAGS correctly regardless of whether
the target is an entry, a directory, or a file.  (Internally, this tests
that RDirs() is available to be called for each Node.FS type.)
"""

import TestSCons

test = TestSCons.TestSCons()

test.write('SConstruct', """\
env=Environment(CPPPATH=['tmp'], INCPREFIX='-I')
d=Entry('foo.d')
e=Entry('foo.e')
f=File('foo.f')
print env.subst('$_CPPINCFLAGS', target=e, source=f)
print env.subst('$_CPPINCFLAGS', target=d, source=f)
print env.subst('$_CPPINCFLAGS', target=f, source=d)
""")

expect = """\
-Itmp
-Itmp
-Itmp
"""

test.run(arguments = '-Q -q', stdout = expect)

test.pass_test()
