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
Demonstrates the Call Tracing Tool

Run this with the '--trace-calls' paramater

Example (compare output from those two):
    python example.py
    python example.py --trace-tools

"""

import tools.tracer   # load this first


def main():
    ''' The main function in a program'''

    # Do some stuff
    data =  'I'

    # Call another function
    return foo(data)


def foo(data):
    ''' A function '''
    data = data + ' am'
    return bar(data)


def bar(data):
    ''' Another function '''
    data = data + ' doing stuff'
    return data


if __name__ == "__main__":
    print main()
