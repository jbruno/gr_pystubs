#!/bin/bash

proj=$(dirname $(readlink -f $0))
output=$proj/.output
manifest=$output/install_manifest.txt

#Check that install manifest exists
[[ -e $manifest ]] || { echo "install manifest not found"; exit 1; }

cat $manifest | while read f; do echo $f; rm -f $f; done

rm $manifest
