#!/bin/bash

function __show_help() {
  echo "Container entrypoint commands:"
  echo "  help - show this help"
  echo "  test - run the tests"
  echo ""
  echo "Any other command will be executed within the container."
}

service redis-server start

case ${1} in
help)
  __show_help
  ;;

test)
  make --makefile make/Makefile.docker
  ;;

test-ci)
  make --makefile make/Makefile.docker test-ci
  ;;

*)
  exec "$@"
  ;;
esac
