#!/bin/bash
datetime=`date +%Y%m%d`
#echo $datetime
#mkdir -p  ${datetime}
if [ ! -d "./${datetime}" ]
then
mkdir  ${datetime}
fi
