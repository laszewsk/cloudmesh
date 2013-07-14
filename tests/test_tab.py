""" run with

nosetests -v --nocapture

or

nosetests -v

"""
import sys
sys.path.insert(0, '..')

import json
import os
import warnings
import pprint
pp = pprint.PrettyPrinter(indent=4)

from cloudmesh.util.util import HEADING
from cloudmesh.util.util import check_file_for_tabs


class Test_cloudmesh:

    # filename = "credentials-example.yaml"

    #filename = None
    filename = "/tmp/test.yaml"
        
    def setup(self):

        print "WRITING THE FILE", self.filename
        with open(self.filename, 'w') as f:
            f.write('First line\n')
            f.write('Second \t line\n')
            f.write('Second \t line with another \t tab\n')
        f.close()            

    def tearDown(self):
        pass

    def test01_check(self):
        HEADING("CHECK FOR TABS")
        assert check_file_for_tabs(self.filename)

