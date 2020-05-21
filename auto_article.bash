DATE="2020-05-17"
EDITDATE=`date +%Y-%m-%d`
IDX=27
FILE="content/restomod-${DATE}.md"
if [ -z ${PICLOC+x} ]; then
    echo "Using default image location"
    PICLOC="~/Downloads/"
fi
IMAGESOURCE="${PICLOC}/${DATE}"

echo Image Source
echo ${IMAGESOURCE}

if [ ! -f ${FILE} ]; then

echo "New file"
touch ${FILE};

echo "---
Title: Restomod Day ${IDX}
Category: Building
Tags: XMods, Restomod
Date: ${DATE}
Updated: ${EDITDATE}
Summary: Pictures for the day
Image: img/IMG_5468.jpg
---

Pictures for the day
" >> ${FILE};

for FULLPATHIMG in ${IMAGESOURCE}/*.jpg; do
    IMG=$(basename ${FULLPATHIMG})
    echo ${FULLPATHIMG}
    ENDPATH="content/img/full/${IMG}"

    cp -v ${FULLPATHIMG} ${ENDPATH}

    printf "![Image]({attach}/img/${IMG})\n\n" >> ${FILE};
done

else
    echo "File Already Exists"
fi

echo ${FILE};
vim ${FILE};
