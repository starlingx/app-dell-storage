#
# Copyright (c) 2023 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

from k8sapp_dell_storage.common import constants as app_constants

from sysinv.tests.db import base as dbbase


class K8SAppDellStorageAppMixin(object):
    app_name = app_constants.HELM_APP_DELL_STORAGE
    path_name = app_name + '.tgz'

    def setUp(self):
        super(K8SAppDellStorageAppMixin, self).setUp()


class K8SAppDellStorageControllerTestCase(K8SAppDellStorageAppMixin,
                                          dbbase.BaseIPv6Mixin,
                                          dbbase.BaseCephStorageBackendMixin,
                                          dbbase.ControllerHostTestCase):
    pass


class K8SAppDellStorageAIOTestCase(K8SAppDellStorageAppMixin,
                                   dbbase.BaseCephStorageBackendMixin,
                                   dbbase.AIOSimplexHostTestCase):
    pass
