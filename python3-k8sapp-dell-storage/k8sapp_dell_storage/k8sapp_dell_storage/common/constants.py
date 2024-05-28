#
# Copyright (c) 2023-2024 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

# Application Name
HELM_NS_DELL_STORAGE = 'dell-storage'
HELM_APP_DELL_STORAGE = 'dell-storage'

# Helm: Supported charts:
HELM_CHART_CSI_POWERFLEX = 'csi-powerflex'
HELM_CHART_CSI_POWERSTORE = 'csi-powerstore'
HELM_CHART_CSI_POWERMAX = 'csi-powermax'
HELM_CHART_CSI_POWERSCALE = 'csi-powerscale'
HELM_CHART_CSI_UNITY = 'csi-unity'
HELM_CHART_CSM_REPLICATION = 'csm-replication'
HELM_CHART_CSM_OBSERVABILITY = 'csm-observability'

# FluxCD
FLUXCD_HELMRELEASE_CSI_POWERFLEX = 'csi-powerflex'
FLUXCD_HELMRELEASE_CSI_POWERSTORE = 'csi-powerstore'
FLUXCD_HELMRELEASE_CSI_POWERMAX = 'csi-powermax'
FLUXCD_HELMRELEASE_CSI_POWERSCALE = 'csi-powerscale'
FLUXCD_HELMRELEASE_CSI_UNITY = 'csi-unity'
FLUXCD_HELMRELEASE_CSM_REPLICATION = 'csm-replication'
FLUXCD_HELMRELEASE_CSM_OBSERVABILITY = 'csm-observability'

# Label
HELM_COMPONENT_LABEL = 'app.starlingx.io/component'
HELM_COMPONENT_SUPPORTED_LABELS = ('platform', 'application')
