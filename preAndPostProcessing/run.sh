#!/bin/bash
set -x
source /opt/openfoam7/etc/bashrc
START_TIME_BLM=$SECONDS
#blockMesh 2>&1 | tee -i blockMesh.log
END_TIME_BLM=$(($SECONDS - $START_TIME_BLM))
START_TIME_SFD=$SECONDS
#setFields 2>&1 | tee -i setFields.log
END_TIME_SFD=$(($SECONDS - $START_TIME_SFD))
START_TIME_CHM=$SECONDS
#checkMesh 2>&1 | tee -i checkMesh.log
END_TIME_CHM=$(($SECONDS - $START_TIME_CHM))
START_TIME_DCP=$SECONDS
decomposePar 2>&1 | tee -i decomposePar.log
END_TIME_DCP=$(($SECONDS - $START_TIME_DCP))
START_TIME_MPI=$SECONDS
mpirun -np 4 interFoam -parallel 2>&1 | tee -i interFoam.log
END_TIME_MPI=$(($SECONDS - $START_TIME_MPI))
#interFoam 2>&1 | tee -i interFoam.log
START_TIME_RCP=$SECONDS
reconstructPar 2>&1 | tee -i reconstructPar.log
END_TIME_RCP=$(($SECONDS - $START_TIME_RCP))
DAYS=$((END_TIME_BLM / 3600 / 24))
HOURS=$(((END_TIME_BLM / 3600) % 24))
MINUTES=$(((END_TIME_BLM % 3600) / 60))
SECONDS=$((END_TIME_BLM % 60))
echo "blockMesh: $DAYS days $HOURS hours $MINUTES min $SECONDS sec"
DAYS=$((END_TIME_SFD / 3600 / 24))
HOURS=$(((END_TIME_SFD / 3600) % 24))
MINUTES=$(((END_TIME_SFD % 3600) / 60))
SECONDS=$((END_TIME_SFD % 60))
echo "setFields: $DAYS days $HOURS hours $MINUTES min $SECONDS sec"
DAYS=$((END_TIME_CHM / 3600 / 24))
HOURS=$(((END_TIME_CHM / 3600) % 24))
MINUTES=$(((END_TIME_CHM % 3600) / 60))
SECONDS=$((END_TIME_CHM % 60))
echo "checkMesh: $DAYS days $HOURS hours $MINUTES min $SECONDS sec"
DAYS=$((END_TIME_DCP / 3600 / 24))
HOURS=$(((END_TIME_DCP / 3600) % 24))
MINUTES=$(((END_TIME_DCP % 3600) / 60))
SECONDS=$((END_TIME_DCP % 60))
echo "decomposePar: $DAYS days $HOURS hours $MINUTES min $SECONDS sec"
DAYS=$((END_TIME_MPI / 3600 / 24))
HOURS=$(((END_TIME_MPI / 3600) % 24))
MINUTES=$(((END_TIME_MPI % 3600) / 60))
SECONDS=$((END_TIME_MPI % 60))
echo "mpirun interFoam: $DAYS days $HOURS hours $MINUTES min $SECONDS sec"
DAYS=$((END_TIME_RCP / 3600 / 24))
HOURS=$(((END_TIME_RCP / 3600) % 24))
MINUTES=$(((END_TIME_RCP % 3600) / 60))
SECONDS=$((END_TIME_RCP % 60))
echo "reconstructPar: $DAYS days $HOURS hours $MINUTES min $SECONDS sec"
