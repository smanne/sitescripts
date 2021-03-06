# This file is part of the Adblock Plus web scripts,
# Copyright (C) 2006-2016 Eyeo GmbH
#
# Adblock Plus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# Adblock Plus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Adblock Plus.  If not, see <http://www.gnu.org/licenses/>.

"""Tests for update manifest generation script."""

import os
import json
import pytest
import subprocess
import xml.etree.ElementTree as ET


def rdf2data(rdf):
    """Convert RDF to a more comparable data strcuture."""
    # We need this to address the RDF item ordering discrepancies.
    def et2data(node):
        return {
            'tag': node.tag,
            'text': node.text,
            'attrib': node.attrib,
            'subs': sorted(et2data(sub) for sub in node)
        }
    return et2data(ET.fromstring(rdf))


@pytest.fixture(scope='session')
def oracle(tests_dir):
    """Function that returns expected content of generated files."""
    def expected_value_of(what):
        return tests_dir.join('oracle').join(what).read().strip()
    return expected_value_of


def test_update_manifests(config_ini, hg_dir, tmpdir, oracle):
    env = dict(os.environ)
    env['SITESCRIPTS_CONFIG'] = str(config_ini)
    cmd = ['python', '-m', 'sitescripts.extensions.bin.updateUpdateManifests']
    subprocess.check_call(cmd, env=env)
    for filename in ['androidupdates.json', 'androidupdates.xml',
                     'ieupdate.json', 'update.rdf', 'updates.plist']:
        got = tmpdir.join(filename).read().strip()
        expect = oracle(filename)
        if filename.endswith('.json'):
            got = json.loads(got)
            expect = json.loads(expect)
        elif filename.endswith('.rdf'):
            got = rdf2data(got)
            expect = rdf2data(expect)
        assert got == expect
