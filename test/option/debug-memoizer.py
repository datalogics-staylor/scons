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
Test calling the --debug=memoizer option.
"""

import os
import string

import TestSCons

test = TestSCons.TestSCons(match = TestSCons.match_re)

# Find out if we support metaclasses (Python 2.2 and later).

class M:
    def __init__(cls, name, bases, cls_dict):
        cls.has_metaclass = 1

class A:
    __metaclass__ = M

try:
    has_metaclass = A.has_metaclass
except AttributeError:
    has_metaclass = None



test.write('SConstruct', """
def cat(target, source, env):
    open(str(target[0]), 'wb').write(open(str(source[0]), 'rb').read())
env = Environment(BUILDERS={'Cat':Builder(action=Action(cat))})
env.Cat('file.out', 'file.in')
""")

test.write('file.in', "file.in\n")

# The banner, and a list of representative method names that we expect
# to show up in the output.  Of course, this depends on keeping those
# names in the implementation, so if we change them, we'll have to
# change this test...
expect = [
    "Memoizer (memory cache) hits and misses",
    "Base.stat()",
    "Dir.srcdir_list()",
    "File.exists()",
    "FS._doLookup()",
    "Node._children_get()",
]

expect_no_metaclasses = """
scons: warning: memoization is not supported in this version of Python \\(no metaclasses\\)
""" + TestSCons.file_expr


if has_metaclass:

    def run_and_check(test, args, desc):
        test.run(arguments = args)
        stdout = test.stdout()
        missing = filter(lambda e, s=stdout: string.find(s, e) == -1, expect)
        if missing:
            print "Missing the following strings in the %s output:" % desc
            print "    " + string.join(missing, "\n    ")
            print "STDOUT ============"
            print stdout
            test.fail_test()

else:

    def run_and_check(test, args, desc):
        test.run(arguments = args, stderr = expect_no_metaclasses)
        stdout = test.stdout()
        present = filter(lambda e, s=stdout: string.find(s, e) != -1, expect)
        if present:
            print "The following unexpected strings are present in the %s output:" % desc
            print "    " + string.join(present, "\n    ")
            print "STDOUT ============"
            print stdout
            test.fail_test()


for args in ['-h --debug=memoizer', '--debug=memoizer']:
    run_and_check(test, args, "command line '%s'" % args)

test.must_match('file.out', "file.in\n")



test.unlink("file.out")



os.environ['SCONSFLAGS'] = '--debug=memoizer'

run_and_check(test, '', 'SCONSFLAGS=--debug=memoizer')

test.must_match('file.out', "file.in\n")



test.pass_test()
