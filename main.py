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
import datetime

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


#This is the model that stores data for the user
class BreakUser(ndb.Model):
    endHours = ndb.IntegerProperty()
    endMinutes = ndb.IntegerProperty()
    endSeconds = ndb.IntegerProperty()
    breakTime = ndb.IntegerProperty()
    studyTime = ndb.IntegerProperty()
    identity = ndb.StringProperty(required = True)

#this test returns true if the current user is NOT in the database
#it will return false if the user IS in the database
def CreateNewUser(currentUserID):
    #all users already in datastore
    allUserIDs = []
    #create list of all registered users
    logging.info("generating a list of all known users")
    for indivUser in BreakUser.query().fetch():
        tempID = indivUser.identity
        logging.info("adding known user %s to the list", tempID)
        allUserIDs.append(tempID)
    #compare current user to registered users to see if already registered
    for userID in allUserIDs:
        logging.info("comparing current user %s with known user %s",
                      currentUserID, userID)
        if(userID == currentUserID):
            logging.info("result of test is false")
            return False
    #not in database
    logging.info("result of test is true")
    return True

#using the ajax communication
class SetEndTime(webapp2.RequestHandler):
    #updating time
    logging.info("entered SetEndTime function")
    time = datetime.datetime.now().time()
    logging.info("testing time function: ", time)



    # logging.info("enter SetEndTme function")
    # currUser = users.get_current_user()
    # currID = currUser.user_id()
    # logging.info("current user id: %s", currID)
    # #finding the right user
    # for indivUser in BreakUser.query().fetch():
    #     logging.info("looking for correct database user")
    #     if( indivUser.identity == currID):
    #         #found user model created in main
    #         logging.info("found correct database user")
    #         indivUser.studyTime = int(self.request.get('timeToStudy'))
    #         indivUser.put()
    #         # userStudyTime = indivUser.studyTime
    #         break
    #
    # logging.info("updated user in database")




class MainHandler(webapp2.RequestHandler):
    def get(self):
        #creates a user for the current user on the page
        googleUser = users.get_current_user()
        userGoogleID = googleUser.user_id()
        logging.info("current user %s created", userGoogleID)

        #run testForUser to see if in database
        userTest = CreateNewUser(userGoogleID)
        logging.info("result of CreateNewUser test for user %s is %s", userGoogleID, userTest)
        if(userTest):
            newUser = BreakUser(identity = userGoogleID)
            newUser.put()

        template = jinja_environment.get_template('templates/dashboard.html')
        self.response.write(template.render())

#this is the timer handler for AFTER THE STUDY PAGE
class TimerHandler(webapp2.RequestHandler):
    #fix this after testing
    def get(self):
        self.post()

    def post(self):
        logging.info("enter TimerHandler")
        currUser = users.get_current_user()
        currID = currUser.user_id()
        logging.info("current user id: %s", currID)
        #finding the right user
        for indivUser in BreakUser.query().fetch():
            logging.info("looking for correct database user")
            if( indivUser.identity == currID):
                #found user model created in main
                logging.info("found correct database user")
                indivUser.studyTime = int(self.request.get('timeToStudy'))
                indivUser.put()
                # userStudyTime = indivUser.studyTime
                break

        logging.info("updated user in database")


        #dictionary for jinja replacement
        templateVars = {
            'studyTime': indivUser.studyTime    #need to access current user data
        }

        template = jinja_environment.get_template('templates/timer.html')
        self.response.write(template.render(templateVars))

        SetEndTime(indivUser.identity, indivUser.studyTime)

class BreaktimerHandler(webapp2.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        logging.info("enter breaktimerHandler")
        currUser = users.get_current_user()
        currID = currUser.user_id()
        logging.info("current user id: %s", currID)
        #finding the right user
        for indivUser in BreakUser.query().fetch():
            logging.info("looking for correct database user")
            if( indivUser.identity == currID):
                #found user model created in main
                logging.info("found correct database user")
                breakTime = indivUser.breakTime
                break


        #dictionary for jinja replacement
        template2Vars = {
            'breakTime': breakTime,    #need to access current user data
        }

        template = jinja_environment.get_template('templates/breaktimer.html')
        self.response.write(template.render(template2Vars))



class BreakHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/break.html')
        self.response.write(template.render())

    def post(self):
        #updating user info to represent how long they want to break for
        logging.info("enter breakHandler")
        currUser = users.get_current_user()
        currID = currUser.user_id()
        logging.info("current user id: %s", currID)
        #finding the right user
        for indivUser in BreakUser.query().fetch():
            logging.info("looking for correct database user")
            if( indivUser.identity == currID):
                #found user model created in main
                logging.info("found correct database user")
                indivUser.breakTime = int(self.request.get('break'))
                indivUser.put()
                # userStudyTime = indivUser.studyTime
                break

        logging.info("updated user in database")




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

#this loads the study page and that allows the data to be fed to the timer
class StartStudyingHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/startStudying.html')
        self.response.write(template.render())



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/timer', TimerHandler),
    ('/break', BreakHandler),
    ('/study', StartStudyingHandler),
    ('/breaktimer', BreaktimerHandler),
    ('/logEndTime', SetEndTime),
], debug=True)
