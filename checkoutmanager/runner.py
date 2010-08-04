from optparse import OptionParser
import os

import pkg_resources

from checkoutmanager import config
from checkoutmanager import utils

ACTIONS = ['exists', 'up', 'st', 'co', 'missing']
CONFIGFILE_NAME = '~/.checkoutmanager.cfg'
ACTION_EXPLANATION = {
    'exists': "Print whether checkouts are present or missing",
    'up': "Grab latest version from the server.",
    'st': "Print status of files in the checkouts",
    'co': "Grab missing checkouts from the server",
    'missing': "Print directories that are missing from the config file",
    }


def main():
    usage = ["Usage: %prog action [group]",
             "  group (optional) is a heading from your config file.",
             "  action can be " + '/'.join(ACTIONS) + ":\n"]
    usage += [action + "\n  " + ACTION_EXPLANATION[action] + "\n"
              for action in ACTIONS]
    usage = "\n".join(usage)
    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="Show debug output")
    (options, args) = parser.parse_args()
    if options.verbose:
        utils.VERBOSE = True

    configfile = os.path.expanduser(CONFIGFILE_NAME)
    if not os.path.exists(configfile):
        print "Config file %s does not exist." % configfile
        print "Copy %s as a sample" % pkg_resources.resource_filename(
            'checkoutmanager.tests', 'sample.cfg')
        return

    if len(args) < 1:
        parser.print_help()
        return
    action = args[0]
    # TODO: check actions

    conf = config.Config(configfile)

    group = None
    if len(args) > 1:
        group = args[1]
        if group not in conf.groupings:
            print "Group %s not in %r" % (group, conf.groupings)
            return

    if action == 'missing':
        # Special case
        conf.report_missing(group=group)
        return

    for dirinfo in conf.directories(group=group):
        getattr(dirinfo, 'cmd_' + action)()
