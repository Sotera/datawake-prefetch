"""

Copyright 2014 Sotera Defense Solutions, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import json
import tangelo
import cherrypy
from datawaketools import graphs
from datawaketools import datawake_db


"""

Serves graphs for the datawake forensic viewer.  Graph building is primailry done in datawaketools.graphs

"""

DEBUG = True


def getUserData():
    assert ('user' in cherrypy.session)
    user = cherrypy.session['user']
    assert ('org' in user)
    return user, user['org']


#
# Return the graph display options
#
def listGraphs():
    (user, org) = getUserData()
    return json.dumps(dict(graphs=['none',
                                   'browse path',
                                   'browse path - with adjacent urls',
                                   'browse path - with adjacent urls min degree 2',
                                   'browse path - with adjacent phone #\'s',
                                   'browse path - with adjacent email #\'s',
                                   'browse path - with text selections',
                                   'browse path- with look ahead']))


#
# Return list of trails with user and size counts
#
def getTrails():
    user, org = getUserData()
    results = datawake_db.getTrailsWithUserCounts(org)
    results.insert(0, {})
    return json.dumps(results)


#
# return all time stamps from the selected trail,users,org
# returns a dictionary of the form  {'min':0,'max':0,'data':[]}
#
def getTimeWindow(users, trail=u'*'):
    user, org = getUserData()
    if trail == u'':
        trail = u'*'
    print 'getTimeWindow(', users, ',', trail, ')'
    if len(users) > 0:
        users = users.split(",")
    else:
        users = []
    return json.dumps(datawake_db.getTimeWindow(org, users, trail))


#
# Return users within an org who have been active on at least one trail
# returns a list of dicts, {name:_, id:_}
#
def listUsers():
    user, org = getUserData()
    return json.dumps(datawake_db.getActiveUsers(org))


#
# Delete all user activity within a time frame
#
def deleteUser(users, startdate, enddate):
    user, org = getUserData()
    tangelo.log('deleteUser(' + users + ',' + startdate + ',' + enddate + ')')
    datawake_db.deleteUserData(org, users, startdate, enddate)
    return json.dumps(dict(success=True))


def getGraph(name, startdate=u'', enddate=u'', users=u'', trail=u'*', domain=u''):
    user, org = getUserData()
    tangelo.log(str(user))
    if trail == u'':
        trail = u'*'
    userlist = map(lambda x: x.replace('\"', '').strip(), users.split(','))
    userlist = filter(lambda x: len(x) > 0, userlist)
    tangelo.log('getGraph( ' + str(name) + ',' + str(startdate) + ',' + str(enddate) + ',' + str(userlist) + ',' + str(trail) + ',' + str(domain) + ')')

    if name == 'browse path':
        graph = graphs.getBrowsePathEdges(org, startdate, enddate, userlist, trail, domain)
        return json.dumps(graphs.processEdges(graph['edges'], graph['nodes']))

    if name == 'browse path - with adjacent urls':
        graph = graphs.getBrowsePathAndAdjacentWebsiteEdgesWithLimit(org, startdate, enddate, 1, userlist, trail, domain)
        return json.dumps(graphs.processEdges(graph['edges'], graph['nodes']))

    if name == 'browse path - with adjacent urls min degree 2':
        graph = graphs.getBrowsePathAndAdjacentWebsiteEdgesWithLimit(org, startdate, enddate, 2, userlist, trail, domain)
        return json.dumps(graphs.processEdges(graph['edges'], graph['nodes']))

    if name == 'browse path - with adjacent phone #\'s':
        graph = graph = graphs.getBrowsePathAndAdjacentPhoneEdgesWithLimit(org, startdate, enddate, 1, userlist, trail, domain)
        return json.dumps(graphs.processEdges(graph['edges'], graph['nodes']))

    if name == 'browse path - with adjacent email #\'s':
        graph = graphs.getBrowsePathAndAdjacentEmailEdgesWithLimit(org, startdate, enddate, 1, userlist, trail, domain)
        return json.dumps(graphs.processEdges(graph['edges'], graph['nodes']))

    if name == 'browse path - with text selections':
        graph = graphs.getBrowsePathWithTextSelections(org, startdate, enddate, userlist, trail, domain)
        return json.dumps(graphs.processEdges(graph['edges'], graph['nodes']))

    if name == 'browse path- with look ahead':
        graph = graphs.getBrowsePathWithLookAhead(org, startdate, enddate, userlist, trail, domain)
        return json.dumps(graphs.processEdges(graph['edges'], graph['nodes']))

    return json.dumps(dict(nodes=[], links=[]))


get_actions = {
    'list': listGraphs,
    'getusers': listUsers,
    'delete': deleteUser,
    'trails': getTrails
}

post_actions = {
    'timewindow': getTimeWindow,
    'get': getGraph
}

delete_actions = {
    'deleteUser': deleteUser
}


@tangelo.restful
def post(action, *args, **kwargs):
    if 'user' not in cherrypy.session:
        return json.dumps(dict())
    post_data = json.loads(cherrypy.request.body.read())

    def unknown(**kwargs):
        return tangelo.HTTPStatusCode(400, "invalid service call")

    return post_actions.get(action, unknown)(**post_data)


@tangelo.restful
def get(action, *args, **kwargs):
    if 'user' not in cherrypy.session:
        return json.dumps(dict())

    def unknown(**kwargs):
        return tangelo.HTTPStatusCode(400, "invalid service call")

    return get_actions.get(action, unknown)(**kwargs)


@tangelo.restful
def delete(action, *args, **kwargs):
    if 'user' not in cherrypy.session:
        return json.dumps(dict())

    def unknown(**kwargs):
        return tangelo.HTTPStatusCode(400, "invalid service call")

    return delete_actions.get(action, unknown)(**kwargs)