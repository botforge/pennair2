#!/usr/bin/env bash
sphinx-apidoc -o ./_modules ../src/pennair2 -f
make html