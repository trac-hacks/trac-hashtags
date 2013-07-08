#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright 2013-2018 Olemis Lang <olemis at gmail.com>
#
# License: BSD

r"""Parse any ticket description or comment text with @<Username> or #<tag>.

Copyright 2013-2018 Olemis Lang <olemis at gmail.com>
Licensed under the BSD License
"""
__author__ = 'Olemis Lang'

import pkg_resources

from genshi.core import START
from genshi.filters.transform import Transformer

#from trac.config import Option
from trac.core import Component, implements
#from trac.web.api import ITemplateStreamFilter
#from trac.web.chrome import add_script, add_stylesheet, ITemplateProvider, add_script_data
from trac.web.href import Href

from trac.web import IRequestFilter
from trac.wiki.api import IWikiSyntaxProvider
from genshi.builder import tag
import re

class TagsModule(Component):
        implements(IWikiSyntaxProvider, IRequestFilter)
        
    
        #IWikiSyntaxProvider methods
        
        def _format_link(self, formatter, ns, match):
            self.log.warning('\n\nEnter _format_link: \nNameSpace: %s\nMatch: %s\nHREF: %s\n', ns, match, formatter.href)
            TagName = re.findall('[^#]+', ns)[0]
            return tag.a(ns, href=formatter.href.tags(TagName) )
        
        def get_wiki_syntax(self):
            """Return an iterable that provides additional wiki syntax.

            Additional wiki syntax correspond to a pair of `(regexp, cb)`,
            the `regexp` for the additional syntax and the callback `cb`
            which will be called if there's a match.  That function is of
            the form `cb(formatter, ns, match)`.
            """
            self.log.warning('\n\nEnter get_wiki_syntax\n\n')
            yield(r"#[A-Za-z_]+[a-zA-Z_0-9]*", lambda x, y, z: self._format_link(x, y, z))

        def get_link_resolvers(self):
            """Return an iterable over `(namespace, formatter)` tuples.

            Each formatter should be a function of the form::

              def format(formatter, ns, target, label, fullmatch=None):
                  pass

            and should return some HTML fragment. The `label` is already
            HTML escaped, whereas the `target` is not. The `fullmatch`
            argument is optional, and is bound to the regexp match object
            for the link.
            """
            
            self.log.warning('\n\nEnter get_link_resolvers\n\n')
            return []
            
        #IRequestFilter Methods
        
        def pre_process_request(self, req, handler):
            self.log.warning("\n\nEntered pre_process_request\n\n")
            self.log.warning('\nreq.args: %s\n', req.args)
            
            
            if req.args.get('save') == 'Submit changes' or req.args.get('submit') == 'Submit changes':    #Check if this is a submit changes request          
                
                #Read the fields that support wikiformatting                
                PageText = req.args.get('text') or ''  #Read the page content in Wiki Pages
                TicketDescription = req.args.get('field_description') or ''  #Read the ticket description
                TicketComment = req.args.get('comment') or ''  #Read the ticket comment
                
                
                #Parse the wikiformatting fields to get the hash-tags
                FoundTags = re.findall(r"(?<=#)[A-Za-z_]+[a-zA-Z0-9_]*", PageText) 
                FoundTags.extend(re.findall(r"(?<=#)[A-Za-z_]+[a-zA-Z0-9_]*", TicketDescription))
                FoundTags.extend(re.findall(r"(?<=#)[A-Za-z_]+[a-zA-Z0-9_]*", TicketComment))
                
                
                #Add the found tags to the keyword fields
                CurrentKeywordField = req.args.get('tags') or ''  #for Wiki pages           
                CurrentTags = CurrentKeywordField.split(',')
                
                CurrentKeywordField = req.args.get('field_keywords') or ''   #For Tickets
                CurrentTags.extend(CurrentKeywordField.split(','))
                
                for i, Tag in enumerate(CurrentTags):   #Cleanup empty tags
                    CurrentTags[i] = CurrentTags[i].strip()
                    if CurrentTags[i] == '':
                        CurrentTags.pop(i)
                
                
                for Tag in FoundTags:
                    if Tag not in CurrentTags:
                        CurrentTags.append(Tag)
                        
                TagsField = ','.join(CurrentTags)
                if req.args.get('tags') is not None: 
                    req.args['tags'] = TagsField
                    
                if req.args.get('field_keywords') is not None:
                    req.args['field_keywords'] = TagsField
                
                
            return handler
        
        def post_process_request(self, req, template, data, content_type):
            return template, data, content_type
        
        
        
