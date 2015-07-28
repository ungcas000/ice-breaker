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
import random
from random import choice
import logging
from google.appengine.api import urlfetch

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

#This is the model that stores data for the user
class BreakUser(ndb.Model):
    endHours = ndb.IntegerProperty()
    endMinutes = ndb.IntegerProperty()
    endSeconds = ndb.IntegerProperty()
    breakTime = ndb.IntegerProperty()
    studyTime = ndb.IntegerProperty()


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/dashboard.html')

        self.response.write(template.render())


class TimerHandler(webapp2.RequestHandler):
    def post(self):

        #reads the data inputed by the start studying page into the database
        userStudyTime = int(self.request.get('timeToStudy'))
        userBreakTime = int(self.request.get('timeToBreak'))

        newUser = BreakUser(studyTime = userStudyTime, breakTime = userBreakTime)
        newUserID = newUser.put()


        #user variables   NEED TO ACCESS
        userStudyTime = 90
        userBreakTime = 20

        #dictionary for jinja replacement
        templateVars = {
            'studyTime': userStudyTime,    #need to access current user data
            'breakTime': userBreakTime    #need to access current user data
        }

        template = jinja_environment.get_template('templates/timer.html')
        self.response.write(template.render(templateVars))






class BreakHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/break.html')
        self.response.write(template.render())

    def post(self):

        #returns length of break and challenge
        def getActivity():
            activity_dict = ['Go for a run', 'Do Yoga', 'Attend a dance class']
            activity2_dict = ['Jumping Jacks', 'Push-ups', 'Plank']

            if self.request.get('break') >= '15':
                return random.choice(activity_dict)

            else:
                return random.choice(activity2_dict)

        activity = getActivity()
        template = jinja_environment.get_template('templates/activity.html')
        break_vars = {'break' : self.request.get('break'), 'activity' : activity}

        self.response.write(template.render(break_vars))

        # self.response.write('<h1> Break the Ice </h1>' + '<br>' + 'You have ' + self.request.get('break') + ' minute(s).' + '<br>')
        # self.response.write(' <h2> Your challenge: </h2> ' + activity)

class StartStudyingHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/startStudying.html')
        self.response.write(template.render())

    #     #this is not needed b/c copied to the timer handler
    # def post(self):
    #     #store study time and break time into database
    #     userStudyTime = int(self.request.get('timeToStudy'))
    #     userBreakTime = int(self.request.get('timeToBreak'))
    #
    #     newUser = User(studyTime = userStudyTime, breakTime = userBreakTime)
    #     newUserID = newUser.put()


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/timer', TimerHandler),
    ('/break', BreakHandler),
    ('/study', StartStudyingHandler)
], debug=True)
