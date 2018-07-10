pandoc -s -c css/site.css -c css/index.css index.md -o index.html

for filename in markdown/*md; do
    echo $(basename $filename .md)
    pandoc -s -c css/site.css -c css/$(basename $filename .md).css $filename\
    -o $(basename $filename .md).html
done
