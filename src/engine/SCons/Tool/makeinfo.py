"""SCons.Tool.makeinfo

Tool-specific initialization for Texinfo's makeinfo.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""

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

import os.path
import re

import SCons.Builder
import SCons.Scanner

TexinfoScanner = None
if TexinfoScanner is None:
    TexinfoScanner = SCons.Scanner.Classic('Texinfo', [], 'TEXINFOPATH',
                                           r'@(?:verbatim)?include\s+(.*)')

setfilename_re = re.compile(r'^@setfilename\s+(.*)$', re.M)
def info_emitter(target, source, env):
    setfilename_re_match = setfilename_re.search(
        open(source[0].rfile().get_abspath(), 'r').read())
    target = [target[0].dir.File(setfilename_re_match.group(1))]
    return target, source

InfoBuilder = None

def generate(env):
    env.SetDefault(
        MAKEINFO='makeinfo',
        MAKEINFOFLAGS='',
        TEXINFOPATH=[],
        _MAKEINFOINCFLAGS='${_concat("-I", TEXINFOPATH, "", __env__, RDirs)}',
        MAKEINFOCOM='$MAKEINFO $_MAKEINFOINCFLAGS $MAKEINFOFLAGS ${SOURCE}',
        TEXINFOPATH=[]
        )

    try:
        env['BUILDERS']['Info']
    except KeyError:
        global InfoBuilder, TexinfoScanner

        if InfoBuilder is None:
            InfoBuilder = SCons.Builder.Builder(action = '$MAKEINFOCOM',
                                                source_scanner = TexinfoScanner,
                                                emitter = info_emitter,
                                                suffix = '.info',
                                                src_suffix = ['.texi', '.texinfo'],
                                                single_source = 1,
                                                chdir = 1)
        env['BUILDERS']['Info'] = InfoBuilder

def exists(env):
    return env.Detect('makeinfo')
