#
# Copyright (c) 2023 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

from sysinv.common import exception

from k8sapp_dell_storage.common import constants as app_constants
from k8sapp_dell_storage.helm import storage


class CSMObservabilityHelm(storage.StorageBaseHelm):
    """ Class to encapsulate helm operations for the CSM chart. """

    CHART = app_constants.HELM_CHART_CSM_OBSERVABILITY
    HELM_RELEASE = app_constants.FLUXCD_HELMRELEASE_CSM_OBSERVABILITY
    SERVICE_NAME = app_constants.HELM_APP_DELL_STORAGE

    def get_overrides(self, namespace=None):

        overrides = {
            app_constants.HELM_NS_DELL_STORAGE: {}
        }

        if namespace in self.SUPPORTED_NAMESPACES:
            return overrides[namespace]
        elif namespace:
            raise exception.InvalidHelmNamespace(chart=self.CHART,
                                                 namespace=namespace)
        else:
            return overrides
