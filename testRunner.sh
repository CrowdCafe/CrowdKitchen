#!/bin/bash
tests=(api)
for arg in "$tests"; do
	python manage.py test $arg
done