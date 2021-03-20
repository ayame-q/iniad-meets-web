#!/bin/sh

if "$DEBUG"; then
  exec npm run serve
else
  exec "$@"
fi