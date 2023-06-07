#
# Copyright (c) 2023 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

# Application Name
HELM_NS_DELL_STORAGE = 'dell-storage'
HELM_APP_DELL_STORAGE = 'dell-storage'

# Helm: Supported charts:
HELM_CHART_CSI_POWERSTORE = 'csi-powerstore'
HELM_CHART_CSI_UNITY = 'csi-unity'
HELM_CHART_CSM_REPLICATION = 'csm-replication'
HELM_CHART_CSM_OBSERVABILITY = 'csm-observability'
HELM_CHART_CSM_APPLICATION_MOBILITY = 'csm-application-mobility'

# FluxCD
FLUXCD_HELMRELEASE_CSI_POWERSTORE = 'csi-powerstore'
FLUXCD_HELMRELEASE_CSI_UNITY = 'csi-unity'
FLUXCD_HELMRELEASE_CSM_REPLICATION = 'csm-replication'
FLUXCD_HELMRELEASE_CSM_OBSERVABILITY = 'csm-observability'
FLUXCD_HELMRELEASE_CSM_APPLICATION_MOBILITY = 'csm-application-mobility'

# Label
HELM_COMPONENT_LABEL = 'app.starlingx.io/component'
HELM_COMPONENT_SUPPORTED_LABELS = ('platform', 'application')
