#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2017 Guenter Bartsch, Heiko Schaefer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import unittest
import logging
import codecs

from nltools import misc

from sqlalchemy.orm import sessionmaker
import model

from zamiaprolog.logicdb import LogicDB
from aiprolog.runtime    import AIPrologRuntime
from aiprolog.parser     import AIPrologParser

from kb import HALKB

UNITTEST_MODULE  = 'unittests'
UNITTEST_CONTEXT = 'unittests'

class TestAIProlog (unittest.TestCase):

    def setUp(self):

        config = misc.load_config('.nlprc')

        #
        # logic DB
        #

        self.db = LogicDB(model.url)

        #
        # knowledge base
        #

        self.kb = HALKB(UNITTEST_MODULE)
        self.kb.clear_all_graphs()

        self.kb.parse_file (UNITTEST_CONTEXT, 'n3', 'tests/chancellors.n3')

        #
        # aiprolog environment setup
        #

        self.prolog_rt = AIPrologRuntime(self.db, self.kb)
        self.parser    = AIPrologParser()

        self.prolog_rt.set_trace(True)

        self.db.clear_module(UNITTEST_MODULE)

    # @unittest.skip("temporarily disabled")
    def test_rdf_results(self):

        self.parser.compile_file('tests/chancellors_rdf.pl', UNITTEST_MODULE, self.db, self.kb)

        clause = self.parser.parse_line_clause_body('chancellor(X)')
        logging.debug('clause: %s' % clause)
        solutions = self.prolog_rt.search(clause)
        logging.debug('solutions: %s' % repr(solutions))
        self.assertEqual (len(solutions), 2)

    # @unittest.skip("temporarily disabled")
    def test_rdf_exists(self):

        clause = self.parser.parse_line_clause_body("rdf ('http://www.wikidata.org/entity/Q567', 'http://www.wikidata.org/prop/direct/P21', 'http://www.wikidata.org/entity/Q6581072')")
        logging.debug('clause: %s' % clause)
        solutions = self.prolog_rt.search(clause)
        logging.debug('solutions: %s' % repr(solutions))
        self.assertEqual (len(solutions), 1)

    # @unittest.skip("temporarily disabled")
    def test_rdf_optional(self):

        self.parser.compile_file('tests/chancellors_rdf.pl', UNITTEST_MODULE, self.db, self.kb)

        clause = self.parser.parse_line_clause_body("is_current_chancellor (X)")
        logging.debug('clause: %s' % clause)
        solutions = self.prolog_rt.search(clause)
        logging.debug('solutions: %s' % repr(solutions))
        self.assertEqual (len(solutions), 1)


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    
    unittest.main()

