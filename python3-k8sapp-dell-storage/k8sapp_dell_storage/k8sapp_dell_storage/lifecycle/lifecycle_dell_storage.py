#
# Copyright (c) 2023 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
# All Rights Reserved.
#

""" System inventory App lifecycle operator."""

import yaml

from k8sapp_dell_storage.common import constants as app_constants

from oslo_log import log as logging

from sysinv.common import constants
from sysinv.helm import lifecycle_base
from sysinv.helm import lifecycle_utils


LOG = logging.getLogger(__name__)


class DellStorageAppLifecycleOperator(lifecycle_base.AppLifecycleOperator):
    def app_lifecycle_actions(self, context, conductor_obj, app_op, app, hook_info):
        """Perform lifecycle actions for an operation

        :param context: request context, can be None
        :param conductor_obj: conductor object, can be None
        :param app_op: AppOperator object
        :param app: AppOperator.Application object
        :param hook_info: LifecycleHookInfo object

        """

        if hook_info.lifecycle_type == constants.APP_LIFECYCLE_TYPE_RESOURCE:
            if hook_info.operation == constants.APP_APPLY_OP:
                if hook_info.relative_timing == constants.APP_LIFECYCLE_TIMING_PRE:
                    lifecycle_utils.create_local_registry_secrets(app_op, app, hook_info)
                    lifecycle_utils.add_pod_security_admission_controller_labels(app_op, app, hook_info)
                    return self.add_component_label_in_pods(app_op, app)
            elif hook_info.operation == constants.APP_REMOVE_OP and \
                    hook_info.relative_timing == constants.APP_LIFECYCLE_TIMING_POST:
                return lifecycle_utils.delete_local_registry_secrets(app_op, app, hook_info)

        super(DellStorageAppLifecycleOperator, self).app_lifecycle_actions(
            context, conductor_obj, app_op, app, hook_info
        )

    def add_component_label_in_pods(self, app_op, app):
        dbapi_instance = app_op._dbapi
        db_app_id = dbapi_instance.kube_app_get(app.name).id

        # List all charts enabled
        charts = self._get_charts_enabled(dbapi_instance, db_app_id)

        for chart in charts:
            # Loading user-overrides
            user_overrides = chart['user_overrides']
            # If user-overrides exists, checking if label was set by user.
            if user_overrides and app_constants.HELM_COMPONENT_LABEL in user_overrides:
                dict_chart_overrides = yaml.safe_load(user_overrides)
                label = dict_chart_overrides[app_constants.HELM_COMPONENT_LABEL]
                # Checking if it's a supported label. If not, set platform as default label.
                if label not in app_constants.HELM_COMPONENT_SUPPORTED_LABELS:
                    dict_chart_overrides[app_constants.HELM_COMPONENT_LABEL] = 'platform'
                    LOG.warn(f'User override for core affinity {label} is not supported,' +
                              'using platform as default label.')

                    chart['user_overrides'] = yaml.safe_dump(dict_chart_overrides)

                    dbapi_instance.helm_override_update(
                        db_app_id,
                        chart['name'],
                        app_constants.HELM_NS_DELL_STORAGE,
                        chart)

    def _get_charts_enabled(self, dbapi_instance, db_app_id):
        # Listing all helm charts from db_app_id
        overrides = dbapi_instance.helm_override_get_all(
            app_id=db_app_id
        )
        # Getting only charts enabled
        charts = [{
                    "name": i.name,
                    "user_overrides": i.user_overrides,
                    "system_overrides": i.system_overrides
                  } for i in overrides if i.system_overrides['enabled'] is True ]
        return charts
