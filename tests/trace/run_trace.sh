#! /usr/bin/env bash


BASEFILENAME=test_input
TRACEINPUT=${BASEFILENAME}.inp

mkdir temp
cd temp


# Remove old files
rm trcdif trcinp trcmsg trcout trctpr trcxtv *.scn tracin 

# Copy input
cp ../$TRACEINPUT tracin

# Run TRACE
/software/TH-codes/TRACE/patch9/trace-V50P9-linux2-intel-x64-release.x 

cp trcxtv ../${BASEFILENAME}.xtv