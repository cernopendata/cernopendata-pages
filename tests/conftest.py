# -*- coding: utf-8 -*-
#
# This file is part of CERN Open Data Portal.
# Copyright (C) 2017 CERN.
#
# CERN Open Data Portal is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# CERN Open Data Portal is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CERN Open Data Portal; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.


"""Pytest configuration."""

from __future__ import absolute_import, print_function

import os
import shutil
import tempfile

import pytest
from flask import Flask
from flask_babelex import Babel
from flask_breadcrumbs import Breadcrumbs
from flask_menu import Menu

from cernopendata_pages import config
from cernopendata_pages.views import blueprint


@pytest.yield_fixture()
def instance_path():
    """Instance path."""
    instance_path = tempfile.mkdtemp()

    yield instance_path

    shutil.rmtree(instance_path)


@pytest.yield_fixture()
def static_folder(instance_path):
    """Static file directory."""
    pth = os.path.join(instance_path, 'static')
    if not os.path.exists(pth):
        os.makedirs(pth)
    yield pth
    shutil.rmtree(pth)


@pytest.fixture()
def app(instance_path, static_folder):
    """Flask application fixture."""
    app = Flask(
        'testapp',
        instance_path=instance_path,
        static_folder=static_folder,
    )
    app.config.from_object(config)
    app.config.update(
        TESTING=True,
        BASE_TEMPLATE='cernopendata_pages/base.html',
    )
    Babel(app)
    Menu(app)
    Breadcrumbs(app)

    app.register_blueprint(blueprint)
    return app
