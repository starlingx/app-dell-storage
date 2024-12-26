#
# Copyright (c) 2023,2025 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
# All Rights Reserved.
#

""" System inventory App lifecycle operator."""

from oslo_log import log as logging

from sysinv.common import constants
from sysinv.helm import lifecycle_base
from sysinv.helm import lifecycle_utils
from sysinv.helm.lifecycle_constants import LifecycleConstants


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

        if hook_info.lifecycle_type == LifecycleConstants.APP_LIFECYCLE_TYPE_RESOURCE:
            if hook_info.operation == constants.APP_APPLY_OP:
                if hook_info.relative_timing == LifecycleConstants.APP_LIFECYCLE_TIMING_PRE:
                    lifecycle_utils.create_local_registry_secrets(app_op, app, hook_info)
                    return lifecycle_utils.add_pod_security_admission_controller_labels(app_op, app, hook_info)
            elif hook_info.operation == constants.APP_REMOVE_OP and \
                    hook_info.relative_timing == LifecycleConstants.APP_LIFECYCLE_TIMING_POST:
                return lifecycle_utils.delete_local_registry_secrets(app_op, app, hook_info)

        super(DellStorageAppLifecycleOperator, self).app_lifecycle_actions(
            context, conductor_obj, app_op, app, hook_info
        )
