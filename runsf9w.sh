#!/bin/bash

if [ $# -ne 1 ]; then
	python sf9w2sf9.py sf9w2sf9/sample/helloworld.sf9w sf9w2sf9/sample/helloworld.sf9w.sf9
	python sf9.py sf9w2sf9/sample/helloworld.sf9w.sf9
	rm sf9w2sf9/sample/helloworld.sf9w.sf9
else
	python sf9w2sf9.py $1 $1.sf9
	python sf9.py $1.sf9
	rm $1.sf9
fi
