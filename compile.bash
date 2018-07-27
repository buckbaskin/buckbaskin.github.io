echo "Compressing images"
for filename in content/img/full/*.jpg; do
    BASE=$(basename $filename .jpg)
    convert $filename -sampling-factor 4:2:0 -strip -resize 1040x585\
    -quality 85 -interlace JPEG -colorspace sRGB content/img/$BASE.jpg
done
echo "Done compressing images"
pelican content -o blog -s pelicanconf.py
