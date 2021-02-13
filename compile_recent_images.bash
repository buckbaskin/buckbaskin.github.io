if [ -z "$(ls -A content/img/full/)"  ]; then
    echo "No New Images to Compress"
else
    let "CORES_MINUS=$(nproc --all) - 1"
    echo "Working with ${CORES_MINUS} cores"
    echo "Compressing Images"
    for filename in $(find content/img/full/*.jpg -mmin -240); do
        echo Compressing ${filename}

        BASE=$(basename $filename .jpg)
        convert $filename -sampling-factor 4:2:0 -strip -resize 1040x585\
        -quality 85 -interlace JPEG -colorspace sRGB content/img/$BASE.jpg &

        num_children=`ps --no-headers -o pid --ppid=$$ | wc -w`
        if [ $num_children -gt ${CORES_MINUS} ]
        then
            echo waiting for reduced job count
            wait
        fi
    done
    wait

    echo "Done with JPG"
    echo "Starting PNG"

    for filename in $(find content/img/full/*.png -mmin -240); do
        echo Compressing ${filename}

        BASE=$(basename $filename .png)
        convert $filename -sampling-factor 4:2:0 -strip -resize 1040x585\
        -quality 85 -interlace JPEG -colorspace sRGB content/img/$BASE.jpg &

        num_children=`ps --no-headers -o pid --ppid=$$ | wc -w`
        if [ $num_children -gt ${CORES_MINUS} ]
        then
            echo waiting for reduced job count
            wait
        fi
    done
    wait

    echo "Done compressing images"
fi
