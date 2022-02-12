for dir in front back left right; do
    for file in $(ls /opt/hat-analysis/${dir}); do
        echo /opt/hat-analysis/${dir}/${file}
        convert /opt/hat-analysis/${dir}/${file} -rotate 180 /opt/hat-analysis/${dir}/${file}
    done
done
