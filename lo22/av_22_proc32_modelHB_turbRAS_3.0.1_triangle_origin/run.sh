#!/bin/bash
chmod a+x execute.sh
./execute.sh $1 $2 $3 2>&1 | tee log.log
