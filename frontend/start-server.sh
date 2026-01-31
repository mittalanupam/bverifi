#!/bin/sh
# Bind to 0.0.0.0 so Railway's proxy can reach the app (required on Railway)
exec serve -s build -l "0.0.0.0:${PORT:-3000}"
