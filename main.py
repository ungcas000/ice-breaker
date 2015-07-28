#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import jinja2
import os
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

#This is the portion of the code that stores the ending time for the timer
class Timer(ndb.Model):
    hours = ndb.IntegerProperty(required = True)
    minutes = ndb.IntegerProperty(required = True)
    seconds = ndb.IntegerProperty(required = True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/dashboard.html')

        self.response.write(template.render())

class TimerTestHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/timer.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/timer', TimerTestHandler),
], debug=True)
