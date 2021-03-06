# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
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

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


###weather webhook example code starts below
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    action = getActionName(req)

    print("Action Name:")
    print(action)

    if action == "getpublications":
        return makeWebhookResult(getPubs(req))
    elif action == "getLIprofile":
        return makeWebhookResult(getLinkedIn(req))
    elif action == "checkwebhook":
        return makeWebhookResult(req)
    else:
        return {}

# Standard method to pull action name from request.
def getActionName(req):
    return req.get("result").get("action")


# Standard method to get a result parameter value.
def getResultParameter(req, name):
    data = ''
    context = getAllResultParameters(req)
    try:
        if (context and context[name] != ''):
            data = context[name]
    except:
        print('Could not find result parameter - ' + name + '.')

    return data

# Standard method to set a result parameter value.
def setResultParameter(req, name, value):
    #req['result']['contexts'][0]['parameters'][name] = value
    req['result']['parameters'][name] = value

# Standard method to get ALL result parameter object.
def getAllResultParameters(req):
    data = {}
    if (req['result'] and req['result']['parameters']):
        data = req['result']['parameters']
    return data

# Standard method to get ALL result context parameter object.
def getAllResultContextParameters(req):
    data = {}
    if (req['result'] and req['result']['contexts'] and req['result']['contexts'][0]):
        data = req['result']['contexts'][0]['parameters']
    return data

# Standard method to get a result context parameter value.
def getResultContextParameter(req, name):
    data = ''
    context = getAllResultContextParameters(req)
    try:
        if (context and context[name] != ''):
            data = context[name]
    except:
        print('Could not find result context parameter - ' + name + '.')

    return data

# def makeWebhookResult(data):
#
#     print("Data Return:")
#     print(data)
#
#     if data:
#         return data
#     else:
#         return {}
def makeWebhookResult(data):
    # query = data.get('query')
    # if query is None:
    #     return {}
    #
    # result = query.get('results')
    # if result is None:
    #     return {}
    #
    # channel = result.get('channel')
    # if channel is None:
    #     return {}
    #
    # item = channel.get('item')
    # location = channel.get('location')
    # units = channel.get('units')
    # if (location is None) or (item is None) or (units is None):
    #     return {}
    #
    # condition = item.get('condition')
    # if condition is None:
    #     return {}

    # print(json.dumps(item, indent=4))

    speech = "WAY TO GO! You have hooked your webhook up successfully."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "DrChivonPowersPhD Bot"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
