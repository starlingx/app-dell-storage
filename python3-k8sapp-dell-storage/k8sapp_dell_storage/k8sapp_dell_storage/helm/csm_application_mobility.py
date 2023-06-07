#
# Copyright (c) 2023 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

from sysinv.common import exception
from sysinv.helm import base

from k8sapp_dell_storage.common import constants as app_constants


class CSMApplicationMobilityHelm(base.FluxCDBaseHelm):
    """ Class to encapsulate helm operations for the CSM Application Mobility chart. """

    CHART = app_constants.HELM_CHART_CSM_APPLICATION_MOBILITY

    HELM_RELEASE = app_constants.FLUXCD_HELMRELEASE_CSM_APPLICATION_MOBILITY

    SUPPORTED_NAMESPACES = base.BaseHelm.SUPPORTED_NAMESPACES + \
        [app_constants.HELM_NS_DELL_STORAGE]
    SUPPORTED_APP_NAMESPACES = {
        app_constants.HELM_APP_DELL_STORAGE: SUPPORTED_NAMESPACES,
    }

    SERVICE_NAME = app_constants.HELM_APP_DELL_STORAGE

    def execute_manifest_updates(self, operator):
        # On application load, this chart is disabled in the metadata.
        # Insert as needed.
        if self._is_enabled(operator.APP, self.CHART,
                                app_constants.HELM_NS_DELL_STORAGE):
            operator.chart_group_chart_insert(
                operator.CHART_GROUPS_LUT[self.CHART],
                operator.CHARTS_LUT[self.CHART])

    def execute_kustomize_updates(self, operator):
        if not self._is_enabled(operator.APP, self.CHART,
                                app_constants.HELM_NS_DELL_STORAGE):
            operator.helm_release_resource_delete(self.HELM_RELEASE)

    def get_overrides(self, namespace=None):

        replicas = self._num_replicas_for_platform_app()

        overrides = {
            app_constants.HELM_NS_DELL_STORAGE: {
                "replicaCount": replicas
            }
        }

        if namespace in self.SUPPORTED_NAMESPACES:
            return overrides[namespace]
        elif namespace:
            raise exception.InvalidHelmNamespace(chart=self.CHART,
                                                 namespace=namespace)
        else:
            return overrides
