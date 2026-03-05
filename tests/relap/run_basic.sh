#!/usr/bin/env bash

# Test script to run the base model

FILENAME=test_input

# Remove old output
rm -f indta ${FILENAME}.out ${FILENAME}.plt ${FILENAME}.scn read_steam_comment.o

# Exit with error when any further command fails
set -e

# RELAP
EXEDIR="/software/TH-codes/RELAP5MOD33lu"
RELAP="$EXEDIR/relap5-33p6lu-linux-ifc-opt-b2-parcs-snap.x"
STEAMTABLE="$EXEDIR/tpfh2onew"

# Run RELAP
$RELAP -i ${FILENAME}.i -o ${FILENAME}.out -Z $STEAMTABLE -r ${FILENAME}.plt