#!/bin/bash

#$Id: release.sh 33 2009-04-22 03:14:41Z patryn $

rm -rf release
mkdir release
mkdir release/src
mkdir release/Templates
mkdir release/Output
cp COPYING release
cp README release
cp LICENSE release
cp *.py release
cp src/*.py release/src
cp Templates/* release/Templates
