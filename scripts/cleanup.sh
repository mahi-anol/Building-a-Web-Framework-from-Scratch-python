#!/bin/bash

# Exit on any error
set -e

if [ -d "build" ]; then
    echo "🗑️  Removing build"
    rm -rf "build"
fi

if [ -d "dist" ]; then
    echo "🗑️  Removing dist"
    rm -rf "dist"
fi

if [ -d "mahi_wsgi_web_framework.egg-info" ]; then
    echo "🗑️  Removing mahi_wsgi_web_framework.egg-info"
    rm -rf "mahi_wsgi_web_framework.egg-info"
fi
