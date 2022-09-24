#!/bin/bash

ng build
rm -rf ../../backend/backend/static/*
cp dist/mini_pupper/* ../../backend/backend/static/
