#
# Copyright (c) 2023,2025-2026 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
# All Rights Reserved.
#

""" System inventory App lifecycle operator."""

from oslo_log import log as logging

from sysinv.common import constants
from sysinv.common.kube_utils import KubeResourceType
from sysinv.common.kube_utils import KubeUtils
from sysinv.helm import lifecycle_base
from sysinv.helm import lifecycle_utils
from sysinv.helm.lifecycle_constants import LifecycleConstants

from k8sapp_dell_storage.common import constants as app_constants

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

        elif hook_info.lifecycle_type == LifecycleConstants.APP_LIFECYCLE_TYPE_OPERATION:
            if (hook_info.operation == constants.APP_REMOVE_OP and
                    hook_info.relative_timing == LifecycleConstants.APP_LIFECYCLE_TIMING_POST and
                    hook_info.extra.get('app_removed', True)):
                return self.post_remove()

        super(DellStorageAppLifecycleOperator, self).app_lifecycle_actions(
            context, conductor_obj, app_op, app, hook_info
        )

    def post_remove(self):
        """Post remove actions: clean up leases left behind by Dell CSI drivers."""

        LOG.info("Removing remaining leases from %s namespace",
                 app_constants.HELM_NS_DELL_STORAGE)

        kube_utils = KubeUtils()

        leases = kube_utils.list_resources(
            resource_type=KubeResourceType.lease,
            namespace=app_constants.HELM_NS_DELL_STORAGE)

        if leases:
            kube_utils.delete_collection_resource(
                resource_type=KubeResourceType.lease,
                namespace=app_constants.HELM_NS_DELL_STORAGE)
            LOG.info("Leases removed from %s namespace",
                     app_constants.HELM_NS_DELL_STORAGE)
