{{- define "celery-worker.fullname" -}}
{{ .Release.Name }}-celery-worker
{{- end }}
