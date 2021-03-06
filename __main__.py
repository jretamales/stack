#!env/bin/python

import sys
import os
import json

from stack.controller import Controller
from stack.db import DB

basedir = os.getcwd()

if __name__ == "__main__":

    USAGE = 'USAGE: python __main__.py db|controller {db_method}|{controller_method} {params}'

    db_methods = [
        'setup',
        'auth',
        'get_project_list',
        'get_project_detail',
        'get_collector_detail',
        'get_network_detail',
        'set_collector_detail',
        'set_network_status',
        'set_collector_status',
        'get_collector_ids',
        'update_collector_detail'
    ]

    controller_processes = ['collect', 'process', 'insert']
    controller_commands = ['start', 'stop', 'restart']

    try:
        wrapper = sys.argv[1]
    except:
        print USAGE
        sys.exit()
    try:
        method = sys.argv[2]
    except:
        print USAGE
        sys.exit()

    if wrapper not in ['db', 'controller']:
        print USAGE
        sys.exit()

    if wrapper == 'db' and method in db_methods:
        db = DB()

        if method == 'setup':
            """
            python __main__.py db setup [project_list]
            """
            project_list = json.loads(sys.argv[3])
            resp = db.setup(project_list)
            print json.dumps(resp, indent=1)
        elif method == 'auth':
            """
            python __main__.py db auth project_name password
            """
            project_name = sys.argv[3]
            password = sys.argv[4]
            resp = db.auth(project_name, password)
            print json.dumps(resp, indent=1)
        elif method == 'get_project_list':
            """
            python __main__.py db get_project_list
            """
            resp = db.get_project_list()
            print json.dumps(resp, indent=1)

        # TODO - WHY WONT THIS WORK?!
        elif method == 'get_collector_ids':
            """
            python __main__.py db get_collector_ids project_id
            """
            project_id = sys.argv[3]
            resp = db.get_collector_ids(project_id)
            print json.dumps(resp, indent=1)
        elif method == 'get_project_detail':
            """
            python __main__.py db get_project_detail project_id
            """
            project_id = sys.argv[3]
            resp = db.get_project_detail(project_id)
            print json.dumps(resp, indent=1)
        elif method == 'get_collector_detail':
            """
            python __main__.py db get_collector_detail project_id collector_id
            """
            project_id = sys.argv[3]
            collector_id = sys.argv[4]
            resp = db.get_collector_detail(project_id, collector_id)
            print json.dumps(resp, indent=1)
        elif method == 'get_network_detail':
            """
            python __main__.py db get_network_detail project_id network
            """
            project_id = sys.argv[3]
            network = sys.argv[4]
            resp = db.get_network_detail(project_id, network)
            print json.dumps(resp, indent=1)
        elif method == 'set_collector_detail':
            """
            python __main__.py db set_collector_detail

            INPUT FORMATTING

            terms_list = '["your", "array", "of", "terms"]' | none
            languages = '["array", "of", "BPR-47 language codes"]' | none
            location = '["array", "of", "location", "points"]' | none

            Can be used to both create and update a collector's details
            """

            print ''
            print 'To create a collector, please fill in the fields when asked.'
            print ''
            print 'For the fields "languages", "locations", and "terms" please fill in either a command separated list, or "none":'
            print ''
            print 'languages = list, of, codes | none'
            print 'Ex. = pr, en'
            print ''
            print 'locations = list, of, location, points | none'
            print 'Ex. = -74, 40, -73, 41'
            print ''
            print 'terms = list, of, terms | none'
            print 'Ex. = social, media'
            print ''

            project_name = raw_input('Project Name: ')
            password = raw_input('Password: ')

            resp = db.auth(project_name, password)
            if resp['status']:
                project_id = resp['project_id']
            else:
                print 'Invalid Project! Please try again.'
                sys.exit(0)

            collector_name = raw_input('Collector Name: ')

            languages = raw_input('Languages: ')
            if languages == 'none':
                languages = None
            else:
                languages = languages.replace(' ', '')
                languages = languages.split(',')

            locations = raw_input('Locations: ')
            if locations == 'none':
                locations = None
            else:
                locations = locations.replace(' ', '')
                locations = locations.split(',')

                if len(locations) % 4 is not 0:
                    print 'The number of location coordinates need to be in pairs of four. Please consult the Twitter docs and try again.'
                    sys.exit(0)

            terms_list = raw_input('Terms: ')
            if terms_list == 'none':
                terms_list = None
            else:
                terms_list = terms_list.replace(' ', '')
                terms_list = terms_list.split(',')

            api = raw_input('API: ')
            network = 'twitter'

            consumer_key = raw_input('Consumer Key: ')
            consumer_secret = raw_input('Consumer Secret: ')
            access_token = raw_input('Access Token: ')
            access_token_secret = raw_input('Access Token Secret: ')

            api_credentials_dict = {
                'consumer_key'          : consumer_key,
                'consumer_secret'       : consumer_secret,
                'access_token'          : access_token,
                'access_token_secret'   : access_token_secret
            }

            resp = db.set_collector_detail(project_id, network, api, collector_name, api_credentials_dict, terms_list, languages=languages, location=locations)
            print json.dumps(resp, indent=1)
        elif method == 'update_collector_detail':
            """
            Calls db.update_collector_detail
            Can only update a single collector param at a time

            FOR TERMS - must provide term and collection status (1 or 0)
            FOR API AUTH CREDS - must provide full list, even if updating one
            """
            update_param = sys.argv[3]
            if update_param not in ['collector_name', 'api', 'oauth', 'terms', 'languages', 'locations']:
                print 'Invalid update paramter. Please try again.'
                print 'Valid update params: collector_name, api, oauth, terms, languages, locations.'
                sys.exit(0)

            print 'Collector update function called.'
            print ''
            print 'FOR TERMS - must provide term value and collection status.'
            print '     1 = collect | 0 = do not collect'
            print ''
            print 'FOR OAUTH CREDS - must provide full list'
            print ''
            print 'FOR languages and locations - must provide full new list of codes. Update will overwrite.'
            print ''
            print 'languages = list, of, codes | none'
            print 'Ex. = pr, en'
            print ''
            print 'locations = list, of, location, points | none'
            print 'Ex. = -74, 40, -73, 41'
            print ''
            print 'Updating for param: %s' % update_param
            print ''

            project_name = raw_input('Project Name: ')
            password = raw_input('Password: ')

            resp = db.auth(project_name, password)
            if resp['status']:
                project_id = resp['project_id']
            else:
                print 'Invalid Project! Please try again.'
                sys.exit(0)

            collector_id = raw_input('Collector ID: ')

            params = {}
            if update_param == 'collector_name':
                params['collector_name'] = raw_input('New Collector Name: ')

            elif update_param == 'api':
                params['api'] = raw_input('New API: ')

            elif update_param == 'languages':
                languages = raw_input('New Language Codes List: ')

                if languages == 'none':
                    languages = None
                else:
                    languages = languages.replace(' ', '')
                    languages = languages.split(',')

                params['languages'] = languages

            elif update_param == 'locations':
                locations = raw_input('New Location Codes List: ')

                if locations == 'none':
                    locations = None
                else:
                    locations = locations.replace(' ', '')
                    locations = locations.split(',')

                params['locations'] = locations

            elif update_param == 'oauth':
                consumer_key = raw_input('Consumer Key: ')
                consumer_secret = raw_input('Consumer Secret: ')
                access_token = raw_input('Access Token: ')
                access_token_secret = raw_input('Access Token Secret: ')

                api_credentials_dict = {
                    'consumer_key'          : consumer_key,
                    'consumer_secret'       : consumer_secret,
                    'access_token'          : access_token,
                    'access_token_secret'   : access_token_secret
                }
                params['api_credentials'] = api_credentials_dict

            elif update_param == 'terms':
                # Sets term type value based on collector API
                resp = db.get_collector_detail(project_id, collector_id)
                if resp['collector']['api'] == 'follow':
                    term_type = 'handle'
                else:
                    term_type = 'term'

                cont = True
                params['terms_list'] = []
                while cont == True:
                    new_term = raw_input('Term: ')
                    collect_status = int(raw_input('Collect: '))

                    if collect_status not in [1, 0]:
                        print 'Invalid collect status. Must be 1 or 0.'
                        sys.exit(0)

                    params['terms_list'].append({
                        'term': new_term,
                        'collect': collect_status,
                        'type': term_type,
                        'id': None
                    })
                    cont_ask = raw_input('Continue? [y/n]: ')
                    cont_ask = cont_ask.lower()
                    if cont_ask == 'y':
                        cont = True
                    else:
                        cont = False

            resp = db.update_collector_detail(project_id, collector_id, **params)
            print json.dumps(resp, indent=1)
    elif wrapper == 'controller' and method in controller_processes:
        """
        python __main__.py controller collect|process|insert start|stop|restart project_id {collector_id|network}

        WHERE

        collector_id - optional, only needed for a collection controller
        network - optional, needed for processor or inserter controllers
        """
        project_id = sys.argv[4]

        if method == 'collect':
            collector_id = sys.argv[5]
            c = Controller(project_id, method, collector_id=collector_id)
        else:
            network = sys.argv[5]
            c = Controller(project_id, method, network=network)

        command = sys.argv[3]
        if command in controller_commands:
            c.run(command)
        else:
            print 'USAGE: python __main__.py controller collect|process|insert start|stop|restart project_id {collector_id|network}'

    else:
        print 'Please try again!'
        sys.exit()
