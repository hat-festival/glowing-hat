for dir in front back left right; do
    for file in $(ls /opt/analysis/${dir}); do
        echo /opt/analysis/${dir}/${file}
        convert /opt/analysis/${dir}/${file} -evaluate subtract 70% /opt/analysis/${dir}/${file}
    done
done
