{{/*
Expand the name of the chart.
*/}}
{{- define "demo-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "demo-app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "demo-app.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "demo-app.labels" -}}
helm.sh/chart: {{ include "demo-app.chart" . }}
app.kubernetes.io/version: {{ .Chart.Version | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
framework: {{ .Values.app.framework }}
project: {{ .Values.app.project }}
environment: {{ .Values.app.environment }}
{{ include "demo-app.selectorLabels" . }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "demo-app.selectorLabels" -}}
app.kubernetes.io/name: {{ .Release.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Common annotations
*/}}
{{- define "demo-app.annotations" -}}
managed-by: devops-team
{{- end }}

{{/*
Service Account annotations
*/}}
{{- define "demo-app.serviceAccountAnnotations" -}}
eks.amazonaws.com/role-arn: "arn:aws:iam::{{ .Values.serviceAccount.aws_account_id}}:role/role-secrets-{{ .Values.app.project }}-{{ .Values.app.environment }}-{{ .Values.app.framework }}"
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "demo-app.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "demo-app.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Common annotations
*/}}
{{- define "demo-app.ingressAnnotations" -}}
{{- if .Values.ingress.alb.enabled  -}}
alb.ingress.kubernetes.io/scheme: internet-facing
alb.ingress.kubernetes.io/load-balancer-name: "{{ .Values.app.project }}-{{ .Values.app.framework }}-{{ .Values.app.environment }}"
{{- else }}
alb.ingress.kubernetes.io/scheme: internal
{{- end }}
{{- if .Values.ingress.inbound_cidrs.enabled  -}}
alb.ingress.kubernetes.io/inbound-cidrs: {{ .Values.ingress.inbound_cidrs.enabled }}
{{- end }}
{{- if .Values.ingress.ssl.enabled  -}}
alb.ingress.kubernetes.io/ssl-redirect: {{ .Values.ingress.ssl.port }}
alb.ingress.kubernetes.io/listen-ports: '[{"HTTP": 80}, {"HTTPS": {{.Values.ingress.ssl.port }}}]'
{{- end }}
{{- if .Values.ingress.alb.delete_protection -}}
alb.ingress.kubernetes.io/load-balancer-attributes: deletion_protection.enabled=true
{{- end }}
alb.ingress.kubernetes.io/healthcheck-path: {{ .Values.readinessProbe.path }}
alb.ingress.kubernetes.io/success-codes: '200-403'
alb.ingress.kubernetes.io/target-group-attributes: stickiness.enabled=true,stickiness.lb_cookie.duration_seconds=300
alb.ingress.kubernetes.io/target-type: ip
{{- end }}
