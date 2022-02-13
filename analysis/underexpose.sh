for dir in front back left right; do
    for file in $(ls /opt/hat-analysis/${dir}); do
        echo /opt/hat-analysis/${dir}/${file}
        convert /opt/hat-analysis/${dir}/${file} -evaluate subtract 70% /opt/hat-analysis/${dir}/${file}
    done
done
