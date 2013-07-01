#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright 2013-2018 Olemis Lang <olemis at gmail.com>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


r"""Trac 1.x plug-in that parses hashtags in text with #<word>.

The plug-in parses 'hash tagged' words (like in Twitter or Google+)
Whenever user types a word with # e.g. #trac the word is linked and
the word is regarded as tag that is listed on a separate page. In order
to do so the plugin hooks into the existing #[ticket number] parser
without conflicts. Hence the ticket number parser remains working as
usual, but if a word starts after # it is regarded as regular tag.
When users click on the parsed hash tag, all connected tickets with
the same hash tag is listed. So this helps to semantically connect
tickets.
The source-code of the plug-in has been made open-source . It is
published on Nothing Agency GitHub account
(https://github.com/nothingagency) so others can either download the
source-code or contribute to it.

Copyright 2013-2018 Olemis Lang <olemis at gmail.com>
Licensed under the Apache License
"""
__author__ = 'Olemis Lang'

# Ignore errors to avoid Internal Server Errors
from trac.core import TracError
TracError.__str__ = lambda self: unicode(self).encode('ascii', 'ignore')

try:
    from trachashtags import *
    msg = 'Ok'
except Exception, exc:
#    raise
    msg = "Exception %s raised: '%s'" % (exc.__class__.__name__, str(exc))
