{{- define "dark8-agent.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "dark8-agent.fullname" -}}
{{- printf "%s-%s" (include "dark8-agent.name" .) .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "dark8-agent.serviceAccountName" -}}
{{- if .Values.serviceAccount.name }}
{{- .Values.serviceAccount.name }}
{{- else }}
{{- printf "%s-%s-sa" (include "dark8-agent.name" .) .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end }}
{{- end -}}
