#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.core.handlers.base import BaseHandler
from django.middleware.csrf import CsrfViewMiddleware
#from debug_toolbar.middleware import DebugToolbarMiddleware
import logging

class DummyHandler(BaseHandler):
    """Required to process request and response middleware"""

    def __call__(self, request):
        self.load_middleware()
        self._request_middleware = self._csrf_filter(self._request_middleware)
        self._view_middleware = self._csrf_filter(self._view_middleware)
        self._response_middleware = self._csrf_filter(self._response_middleware)
        self._exception_middleware = self._csrf_filter(self._exception_middleware)
        response = self.get_response(request)
        for middleware_method in self._response_middleware:
            response = middleware_method(request, response)
        return response
    def _csrf_filter(self,middleware):
        return [ x for x in middleware if x.im_class not in ( CsrfViewMiddleware, ) ]
  
