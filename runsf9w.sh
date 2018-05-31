#!/bin/bash

if [ $# -ne 1 ]; then
	python sf9w2sf9.py sample/helloworld.sf9w sample/helloworld.sf9w.sf9
	python main.py sample/helloworld.sf9w.sf9
else
	python sf9w2sf9.py $1 $1.sf9
	python main.py $1.sf9
fi
