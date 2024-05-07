OUTFILE=${1}
shift

docker run --volume $(pwd)/../conf/panel/strings/:/opt/output/ word-maker ${OUTFILE} "${@}"
