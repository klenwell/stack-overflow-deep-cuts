"""
To run:
    python main.py
    >>> usage()
"""
import yaml
import stackexchange

#
# Default Configuration
#
config = {

}

#
# Public API
#
def fetch(**options):
    pass

#
# Private Methods
#
def read_secrets():
    with open("../secrets.yml", 'r') as stream:
        return yaml.load(stream)

#
# Main Block
#
def main():
    secrets = read_secrets()
    print(secrets)
    #so = stackexchange.Site(stackexchange.StackOverflow, API_KEY)
    #print(USAGE)
    #pdb.set_trace()

if __name__ == '__main__':
    main()
