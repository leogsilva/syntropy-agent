#!/bin/bash
REL_NAME=$(date +%Y-%m-%d_%H%M)
git checkout sandbox
git pull
git checkout -b release/$REL_NAME
git remote update
git push origin release/$REL_NAME
