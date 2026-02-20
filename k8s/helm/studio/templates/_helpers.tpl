{{- define "dark8-studio.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "dark8-studio.fullname" -}}
{{- printf "%s-%s" (include "dark8-studio.name" .) .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "dark8-studio.serviceAccountName" -}}
{{- if .Values.serviceAccount.name }}
{{- .Values.serviceAccount.name }}
{{- else }}
{{- printf "%s-%s-sa" (include "dark8-studio.name" .) .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end }}
{{- end -}}
