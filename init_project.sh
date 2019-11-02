#!/bin/bash
ROOT_DIR=`pwd`
echo -e "You are in $ROOT_DIR directory"
export PYTHONPATH=$PYTHONPATH:$ROOT_DIR
echo -e "PYTHONPATH is = $PYTHONPATH"
cd src/common_utils/database_preparing
CURR_DIR=`pwd`
echo -e "You are now in $CURR_DIR directory"
export PYTHONPATH=$PYTHONPATH:$CURR_DIR
echo -e "PYTHONPATH now is = $PYTHONPATH"
python3 set_init_configure.py
cd ../../..
echo -e "You are back in project root folder"

