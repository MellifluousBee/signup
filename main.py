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
import webapp2
import re
import cgi

title = """
<html>
<head>
    <title>Signup</title>
</head>
"""

form = """
<form method="post">
    <html>
    <head>
        <title>Signup</title>
    </head>
    <body>
    <h1>Signup:</h1><br>
    <label>
        Username:
        <input type="text" name="username" value="%(username)s">
        <div style="color: red; display: inline-block;">%(error_name)s</div>
    </label>
    <br>
    <label>
        Password:
        <input type="password" name="password">
        <div style="color: red; display: inline-block;">%(error_pwd)s</div>
    </label>
    <br>
    <label>
        Verify Password:
        <input type="password" name="verify">
        <div style="color: red; display: inline-block;">%(error_match)s</div>
    </label>
    <br>
    <label>
        Email(Optional):
        <input type="text" name="email" value="%(email)s">
        <div style="color: red; display: inline-block;">%(error_email)s</div>
    </label>
    <br>
    <input type="submit">
    </body>
    </html>
</form>
"""
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)


class MainPage(webapp2.RequestHandler):


    def write_form(self, error_name="", error_pwd="", error_match="", error_email="", username="", email=""):
        self.response.out.write(form %{"error_name": error_name, "error_pwd": error_pwd, "error_match":error_match,
                                        "error_email": error_email, "username": username, "email": email})

    def get(self):
        self.write_form()

    def post(self):

        global username
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        name = valid_username(username)
        pwd = valid_password(password)
        mail = valid_email(email)

        errname_escaped = ""
        errpwd_escaped = ""
        errmatch_escaped = ""
        errmail_escaped = ""


        if not name:
            error_name="That's not a valid username.".format(username)
            errname_escaped = cgi.escape(error_name, quote=True)

        if username == "":
            error_noname = "You didn't write anything".format(username)
            errname_escaped = cgi.escape(error_noname, quote=True)

        if not password:
            error_pwd="That wasn't a valid password."
            errpwd_escaped = cgi.escape(error_pwd, quote=True)

        elif password != verify:
            error_match="Your passwords didn't match."
            errmatch_escaped = cgi.escape(error_match, quote=True)

        if not valid_email(email):
            error_email="That's not a valid email."
            errmail_escaped = cgi.escape(error_email, quote=True)


        self.write_form(errname_escaped, errpwd_escaped, errmatch_escaped, errmail_escaped, username, email)

        if (name and pwd and mail and (password == verify)):

            self.redirect("/welcome")


class Welcome(webapp2.RequestHandler):

    def get(self):

        response = title + "<p style='font-size:30px;'>" "Welcome " + username + "!" "</p>"
        self.response.write(response)


app = webapp2.WSGIApplication([('/', MainPage),('/welcome', Welcome)], debug=True)
