#!/bin/bash

read -p "How much processes?: " PROC
read -p "test file .cors: " FILE
for (( a = 0; a < $PROC; a++ ))
do
gnome-terminal --window-with-profile=sole -e "bash test.sh $a $PROC $FILE"
done
read -p "Press Enter, when all terminals are closed!" skip
echo parsing...
python3 parse_result.py $PROC $FILE