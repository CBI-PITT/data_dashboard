#!/usr/bin/env bash
# Build the React frontend (dashboard/) and ship the output into the python
# package (data_dashboard/web/). Run once from the data_dashboard repo root;
# requires Node 16+ (nvm install 16). The server does not need node.
set -e
cd "$(dirname "$0")/dashboard"
npm ci || npm install
npm run build
cd ..
rm -rf data_dashboard/web
mkdir -p data_dashboard/web
cp -r dashboard/build/* data_dashboard/web/
echo "React build copied to data_dashboard/web/"
