#
# Copyright (c) 2023 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

from k8sapp_dell_storage.tests import test_plugins

from sysinv.db import api as dbapi
from sysinv.tests.helm import base
from sysinv.tests.db import base as dbbase
from sysinv.tests.db import utils as dbutils


class DellStorageTestCase(test_plugins.K8SAppDellStorageAppMixin,
                          base.HelmTestCaseMixin):
    def setUp(self):
        super(DellStorageTestCase, self).setUp()
        self.app = dbutils.create_test_app(name='dell_storage')
        self.dbapi = dbapi.get_instance()


class DellStorageTestCaseDummy(DellStorageTestCase,
                               dbbase.ProvisionedControllerHostTestCase):

    def test_dummy(self):
        pass
