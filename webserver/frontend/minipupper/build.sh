#!/bin/bash

ng build
rm -rf ../../backend/backend/static/*
cp dist/minipupper/* ../../backend/backend/static/
