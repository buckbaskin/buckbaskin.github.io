for writeup in $(find content/*.md -mmin -240); do
    aspell check ${writeup};
    result=$?
    if [ $? -gt 0 ]
    then
        break
    fi
done
