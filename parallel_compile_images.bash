if [ -z "$(ls -A content/img/full/)"  ]; then
    echo "No New Images to Compress"
else
    echo "Compressing JPG"
    for filename in content/img/full/*.jpg; do
        echo Compressing ${filename}

        BASE=$(basename $filename .jpg)
        convert $filename -sampling-factor 4:2:0 -strip -resize 1040x585\
        -quality 85 -interlace JPEG -colorspace sRGB content/img/$BASE.jpg &

        num_children=`ps --no-headers -o pid --ppid=$$ | wc -w`
        if [ $num_children -gt 4 ]
        then
            echo waiting for reduced job count
            wait
        fi
    done
    wait
    echo "Done with JPG"

    echo "Compressing CAD PNG"
    for filename in content/img/full/CAD*.png; do
        echo Compressing ${filename}

        BASE=$(basename $filename .png)
        convert $filename -sampling-factor 4:2:0 -strip -resize 1040x585\
        -quality 85 -interlace JPEG -colorspace sRGB content/img/$BASE.jpg &

        num_children=`ps --no-headers -o pid --ppid=$$ | wc -w`
        if [ $num_children -gt 4 ] 
        then
            echo waiting for reduced job count
            wait
        fi
    done
    wait
    echo "Done with CAD PNG"

    echo "Done compressing images"
fi
