#!/bin/sh 

MP4Box -fps $1 -add $2 $3 > /dev/null
rm -f $2
