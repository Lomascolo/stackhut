# Copyright 2015 StackHut Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
StackHut service support
"""
from __future__ import (unicode_literals, print_function, division, absolute_import)
from future import standard_library
standard_library.install_aliases()

from stackhut.run_command import RunCloudCmd, RunLocalCmd
from stackhut.build_commands import StackBuildCmd, HutBuildCmd

# TODO - small commands go here...
# different classes for common tasks
# i.e. shell out, python code, etc.
# & payload pattern matching helper classes



# StackHut primary commands
COMMANDS = [RunLocalCmd,
            RunCloudCmd,
            HutBuildCmd,
            StackBuildCmd,
            # debug, push, pull, test, etc.
            ]
