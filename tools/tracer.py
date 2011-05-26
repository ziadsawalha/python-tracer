#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# Copyright 2011 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# Author: Ziad Sawalha (http://launchpad.net/~ziad-sawalha)

"""
Call Tracing Tool

To use this:
1. include the tools diretory in your project (__init__.py and tracer.py)
2. import tools.tracer as early as possible into your module
3. add --trace-calls to any argument parsers you use so the argument doesn't get
flagged as invalid.

Usage:
# Add this as early as possible in the first module called in your service
import tools.tracer   #load this first

If a '--trace-calls' parameter is found, it will trace calls to the console and
space them to show the call graph.

"""

import os
import sys


if '--trace-calls' in sys.argv:
    stack_depth = 0

    def localtrace(frame, event, arg):
        global stack_depth
        if event == "return":
            stack_depth = stack_depth - 1
        elif event == "exception":
            co = frame.f_code
            func_name = co.co_name
            line_no = frame.f_lineno
            filename = co.co_filename
            exc_type, exc_value, exc_traceback = arg
            print '\033[91m%sERROR: %s %s on line %s of %s\033[0m' % \
                ('  ' * stack_depth, exc_type.__name__, exc_value, line_no,
                 func_name)
        return None

    def selectivetrace(frame, event, arg):
        global stack_depth
        if event == "exception":
            co = frame.f_code
            func_name = co.co_name
            line_no = frame.f_lineno
            filename = co.co_filename
            exc_type, exc_value, exc_traceback = arg
            print '\033[91m%sERROR: %s %s on line %s of %s\033[0m' % \
                ('  ' * stack_depth, exc_type.__name__, exc_value, line_no,
                 func_name)
        if event != 'call':
            return
        co = frame.f_code
        func_name = co.co_name
        if func_name == 'write':
            # Ignore write() calls from print statements
            return
        func_filename = co.co_filename
        if func_filename == "<string>":
            return
        if func_filename.startswith("/System"):
            return
        if func_filename.startswith("/Library"):
            return
        if 'macosx' in func_filename:
            return
        func_line_no = frame.f_lineno
        # If ../..//project/__init__.py exists, add ../ to Python search path, so that
        # it will override what happens to be installed in /usr/(local/)lib/python...
        possible_topdir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                           os.pardir,
                                           os.pardir))
        func_filename = func_filename.replace(possible_topdir, '')
        caller = frame.f_back
        caller_line_no = caller.f_lineno
        caller_filename = caller.f_code.co_filename.replace(possible_topdir,
                                                            '')
        print '%s%s::%s:%s      (from %s:%s)' % \
            ('  ' * stack_depth, func_filename, func_name, func_line_no,
             caller_filename, caller_line_no)
        stack_depth = stack_depth + 1
        return localtrace

    sys.settrace(selectivetrace)
    print 'Starting call tracer'