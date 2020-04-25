if [ -z "$(ls -A content/img/full/)"  ]; then
    echo "No New Images to Compress"
else
    echo "Compressing JPG"
    for filename in content/img/full/*.jpg; do
        echo Compressing ${filename}
        BASE=$(basename $filename .jpg)
        convert $filename -sampling-factor 4:2:0 -strip -resize 1040x585\
        -quality 85 -interlace JPEG -colorspace sRGB content/img/$BASE.jpg
    done
    echo "Compressing PNG"
    for filename in content/img/full/CAD*.png; do
        BASE=$(basename $filename .png)
        convert $filename -sampling-factor 4:2:0 -strip -resize 1040x585\
        -quality 85 -interlace JPEG -colorspace sRGB content/img/$BASE.jpg
    done
    echo "Done compressing images"
fi
