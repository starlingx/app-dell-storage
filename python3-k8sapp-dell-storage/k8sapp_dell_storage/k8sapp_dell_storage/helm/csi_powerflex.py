#
# Copyright (c) 2024 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

from sysinv.common import exception

from k8sapp_dell_storage.common import constants as app_constants
from k8sapp_dell_storage.helm import storage


class CSIPowerFlexHelm(storage.StorageBaseHelm):
    """ Class to encapsulate helm operations for the CSI PowerFlex chart. """

    CHART = app_constants.HELM_CHART_CSI_POWERFLEX
    HELM_RELEASE = app_constants.FLUXCD_HELMRELEASE_CSI_POWERFLEX
    SERVICE_NAME = app_constants.HELM_APP_DELL_STORAGE

    def get_overrides(self, namespace=None):

        controller = {
            "controllerCount": self._num_replicas_for_platform_app()
        }

        overrides = {
            app_constants.HELM_NS_DELL_STORAGE: {
                "controller": controller,
            }
        }

        if namespace in self.SUPPORTED_NAMESPACES:
            return overrides[namespace]
        elif namespace:
            raise exception.InvalidHelmNamespace(chart=self.CHART,
                                                 namespace=namespace)
        else:
            return overrides
