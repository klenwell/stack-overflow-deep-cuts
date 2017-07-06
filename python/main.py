"""
To run:
    python main.py
    >>> usage()
"""
from collections import deque
from datetime import datetime, timedelta
import pdb
import time

import stackexchange
import yaml

from models.scored_question import ScoredQuestion

#
# Constants
#
USAGE = """
USAGE:

Use fetch_deep_cuts method to fetch a collection of results. You can then cycle
through them using next and prev methods.

> cuts = fetch_deep_cuts('python')
> cuts.next()
> cuts.prev()
"""

#
# Default Configuration
#
config = {
    'api_key'       : None,
    'accepted'      : False,
    'closed'        : False,
    'max_hours'     : 48,
    'min_hours'     : 2,

    # Tags are comma-separated OR (not AND) lists of tags.
    'include_tags'  : '',
    'exclude_tags'  : ''
}

#
# Public API
#
def usage():
    print(USAGE)

def fetch_deep_cuts(tags, **options):
    options['include_tags'] = tags
    questions = fetch_questions(**options)
    return Carousel(ScoredQuestion.filter_search_results(questions))

#
# Private Methods
#
def fetch_questions(**options):
    # Options
    api_key = options.get('api_key', config.get('api_key'))
    accepted = options.get('accepted', config.get('accepted'))
    closed = options.get('closed', config.get('closed'))
    max_hours = options.get('max_hours', config.get('max_hours'))
    min_hours = options.get('min_hours', config.get('min_hours'))
    include_tags = options.get('include_tags', config.get('include_tags'))
    exclude_tags = options.get('exclude_tags', config.get('exclude_tags'))

    # API Interface
    so = stackexchange.Site(stackexchange.StackOverflow, api_key)

    # Respect the rate limit. throttle_stop will throw an error when we hit the
    # limit which we can catch. (This is the default behavior.)
    so.throttle_stop = True

    # Search for Stack Overflow questions
    questions = so.search(accepted=accepted,
                          closed=closed,
                          fromdate=hours_ago_to_unix_timestamp(max_hours),
                          todate=hours_ago_to_unix_timestamp(min_hours),
                          tagged=include_tags,
                          nottagged=exclude_tags)

    return questions

def read_stackoverflow_secrets(key=None):
    secrets = read_secrets()
    so_secrets = secrets['stackoverflow']
    return so_secrets.get(key) if key else so_secrets

def read_secrets():
    with open("../secrets.yml", 'r') as stream:
        return yaml.load(stream)

def hours_ago_to_unix_timestamp(hours_ago):
    # https://api.stackexchange.com/docs/dates
    return int(time.mktime((datetime.now() - timedelta(hours=hours_ago)).timetuple()))

#
# Helper Classes
#
class Carousel(object):
    # Based on https://stackoverflow.com/a/2777223/1093087
    # Because Python 3 iters don't have a next method and next(iter) conflicts with
    # pdb's next method.
    def __init__(self, collection):
        self.collection = collection
        self.index = 0

    @property
    def current(self):
        return self.collection[self.index]

    @property
    def first(self):
        self.index = 0
        return self.current

    @property
    def last(self):
        self.index = len(self.collection) - 1
        return self.current

    def next(self):
        try:
            result = self.collection[self.index]
            self.index += 1
        except IndexError:
            print("You've reached last item. Returning to first item.")
            self.index = 0
            result = self.next()
        return result

    def prev(self):
        self.index -= 1
        if self.index < 0:
            print("You've reached first item. Going to last item.")
            self.index = len(self.collection)
            return self.prev()
        return self.current

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.collection)

#
# Main Block
#
def main():
    usage()
    config['api_key'] = read_stackoverflow_secrets('api_key')
    pdb.set_trace()

def sandbox():
    # Use this to test and debug script in main block below.
    usage()
    config['api_key'] = read_stackoverflow_secrets('api_key')
    tags = 'jquery'
    questions = fetch_deep_cuts(tags)
    print(len(questions))
    pdb.set_trace()

if __name__ == '__main__':
    main()
