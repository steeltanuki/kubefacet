{{/*
Copyright 2026 Alessandro Rontani

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
*/}}

{{- define "kubefacet.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "kubefacet.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := include "kubefacet.name" . -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{- define "kubefacet.namespace" -}}
{{- .Release.Namespace -}}
{{- end -}}

{{- define "kubefacet.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "kubefacet.labels" -}}
helm.sh/chart: {{ include "kubefacet.chart" . }}
app.kubernetes.io/name: {{ include "kubefacet.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/part-of: kubefacet
app.kubernetes.io/managed-by: {{ .Release.Service }}
kubefacet.steeltanuki.it/release: {{ .Release.Name }}
kubefacet.steeltanuki.it/release-namespace: {{ .Release.Namespace }}
{{- end -}}

{{- define "kubefacet.selectorLabels" -}}
app.kubernetes.io/name: {{ include "kubefacet.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{- define "kubefacet.ownershipAnnotations" -}}
meta.helm.sh/release-name: {{ .Release.Name | quote }}
meta.helm.sh/release-namespace: {{ .Release.Namespace | quote }}
kubefacet.steeltanuki.it/ownership: {{ printf "%s/%s" .Release.Namespace .Release.Name | quote }}
{{- end -}}

{{- define "kubefacet.serviceAccountName" -}}
{{- printf "%s-manager" (include "kubefacet.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "kubefacet.webhookServiceName" -}}
{{- printf "%s-webhook" (include "kubefacet.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "kubefacet.metricsServiceName" -}}
{{- printf "%s-metrics" (include "kubefacet.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "kubefacet.webhookSecretName" -}}
{{- if eq .Values.certificate.mode "externalSecret" -}}
{{- .Values.certificate.externalSecret.secretName -}}
{{- else -}}
{{- printf "%s-webhook-tls" (include "kubefacet.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}

{{- define "kubefacet.webhookIssuerName" -}}
{{- printf "%s-webhook-issuer" (include "kubefacet.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "kubefacet.webhookCAIssuerName" -}}
{{- printf "%s-ca-issuer" (include "kubefacet.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "kubefacet.webhookCACertificateName" -}}
{{- printf "%s-webhook-ca" (include "kubefacet.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "kubefacet.webhookCertificateName" -}}
{{- printf "%s-webhook-serving" (include "kubefacet.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "kubefacet.webhookDNSNames" -}}
{{- $service := include "kubefacet.webhookServiceName" . -}}
{{- list $service (printf "%s.%s" $service (include "kubefacet.namespace" .)) (printf "%s.%s.svc" $service (include "kubefacet.namespace" .)) (printf "%s.%s.svc.cluster.local" $service (include "kubefacet.namespace" .)) | join "," -}}
{{- end -}}

{{- define "kubefacet.image" -}}
{{- printf "%s:%s" .Values.image.repository (default .Chart.AppVersion .Values.image.tag) -}}
{{- end -}}
