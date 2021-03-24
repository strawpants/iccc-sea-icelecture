#!/bin/bash

#Quick and dirty script to export a jupyter rise notebook to a pdf, using decktape (requires decktape to be installed)
# R. Rietbroek  27 Jan 2021

# Usage
# ./exportToPdf.sh Lecture1Example.ipynb


rooturl=`jupyter notebook list | awk '/^http/{sub("?token","notebooks/'$1'?token",$1);print $1}'`

#create a symbolic link so custom css is recognized by decktape
base=`basename $1 .ipynb`
ln -sf rise.css ${base}.css

decktape rise -s 1920x1080 $rooturl $base.pdf

# clean up the symbolic link
rm $base.css
