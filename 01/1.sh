#!/bin/bash

read cases
for i in `seq $cases`
do
	read line
	# Search the line in students.txt, got the names of the students,
	# sorts them and join the lines with ','
	output="$(grep "$line" students.txt | cut -d',' -f1 | sort | paste -d, -s)"
	echo "Case #$i: ${output:-NONE}"
done
