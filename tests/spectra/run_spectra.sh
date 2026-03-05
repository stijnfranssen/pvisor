#! /usr/bin/env bash

rm -rf test
mkdir -p test
cd test

TESTNAME=test_input

cp ../${TESTNAME}.SPE ./

SPECTRAEXE=/software/TH-codes/SPECTRA-Linux/SPECTRA-25-09-0000.X

# SPECTRAEXE=/software/TH-codes/SPECTRA-Linux/SPECTRA-24-02-0000.X

$SPECTRAEXE ${TESTNAME}.SPE

cd ../
#rm -rf test
