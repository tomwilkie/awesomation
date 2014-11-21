#!/bin/bash

set -eu

function DoSpeedTest {
	start=`date +%s`
	runtime=`{ time curl http://speedtest.netcologne.de/test_10mb.bin > /dev/null 2>&1; } 2>&1 | grep real | awk -F'[sm. \t]' '{print $3$4}'`
	bandwidth=$(bc -l <<< "scale=2; 80000000/$runtime")
	echo ${start}, ${bandwidth}
}

DoSpeedTest >> ~/speed.csv
