# TODO: Append title metadata, then copy to content instead of blog
#   This will result in the right heading and title automatically
# TODO: Add date metadata automatically

pointdir=blog/pages

for book in notes/*; do 
    bookid=$(basename ${book});
    echo Book ${bookid};
    mkdir -p ${pointdir}/${book}
    for chapter in ${book}/*.ipynb; do 
        chapterid=$(basename ${chapter} .ipynb);
        chapterprefix=$(dirname ${chapter})
        echo Chapter ${chapter} ${chapterprefix} ${chapterid}; 
        jupyter nbconvert --to html ${chapter}
        cp -v ${chapterprefix}/${chapterid}.html ${pointdir}/${chapterprefix}/
    done;
done
