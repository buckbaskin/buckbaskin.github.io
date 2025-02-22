for f in $(ls content/*.md); do python md_to_text.py $f > linttmp/$f || break ; done
proselint --config=proselintrc.json linttmp/content/*.md
