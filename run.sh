#!/bin/bash
set -x
source /opt/openfoam7/etc/bashrc
START_TIME_BLM=$SECONDS
blockMesh 2>&1 | tee -i blockMesh.log
END_TIME_BLM=$(($SECONDS - $START_TIME_BLM))
#setFields 2>&1 | tee -i setFields.log
START_TIME_CHM=$SECONDS
checkMesh 2>&1 | tee -i checkMesh.log
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
echo "blockMesh: (($END_TIME_BLM / 3600)) hours ((($END_TIME_BLM % 3600) / 60)) min (($END_TIME_BLM % 60)) sec"
echo "checkMesh: (($END_TIME_CHM / 3600)) hours ((($END_TIME_CHM % 3600) / 60)) min (($END_TIME_CHM % 60)) sec"
echo "decomposePar: (($END_TIME_DCP / 3600)) hours ((($END_TIME_DCP % 3600) / 60)) min (($END_TIME_DCP % 60)) sec"
echo "mpirun interFoam: (($END_TIME_MPI / 3600)) hours ((($END_TIME_MPI % 3600) / 60)) min (($END_TIME_MPI % 60)) sec"
echo "reconstructPar: (($END_TIME_RCP / 3600)) hours ((($END_TIME_RCP % 3600) / 60)) min (($END_TIME_RCP % 60)) sec"
