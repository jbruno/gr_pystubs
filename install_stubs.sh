#!/bin/bash

#Look for stubs and metadata
proj=$(dirname $(readlink -f $0))
output=$proj/.output
src=$output/stubs
[[ -d $src ]] || { echo "could not find stubs"; exit 1; }
dst=$(<$proj/.output/gr_path.txt)

#Make sure we can write to the destination
[[ -w $dst ]] || { echo "permission denied"; exit 1; }

#Clear install manifest
manifest=$output/install_manifest.txt
[[ -e $manifest ]] && rm $manifest

cd $src

#Install and create manifest
for f in $(find * -type f)
do 
    # dst_dir=/tmp/stubs/$(dirname $f)
    dst_dir=$dst/$(dirname $f)
    dst_f=$dst_dir/$(basename $f) 
    install -D -t $dst_dir $f
    printf "$dst_f\n"
    echo $dst_f >> $manifest
done
