for writeup in content/*.md; do
    aspell check ${writeup};
    result=$?
    if [ $? -gt 0 ]
    then
        break
    fi
done
