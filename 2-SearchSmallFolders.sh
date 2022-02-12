#! /bin/sh

MIN_LIMIT=30

# Print folders containing less than 30 files

if [ $# -lt 1 ]; then
    echo "Missing argument"
    echo "$0 FolderToSearch"
    echo ""
    echo "Usage: (example for current folder)"
    echo "$0 ."
    echo ""
    exit -1
fi

source ./functions.sh

########################################

SEARCH_DIR="$1"

for ENTRY in "${SEARCH_DIR}"/*
do
    #echo "${ENTRY}"
    if [ -d "${ENTRY}" ]; then
	#echo "${ENTRY}"
	COUNTER=0
	for SUB_ENTRY in "${ENTRY}"/*
	do
	    COUNTER=$(( COUNTER + 1 ))
	done
	#echo "${ENTRY} : ${COUNTER}"
	if [ ${COUNTER} -le ${MIN_LIMIT} ]; then
	    echo "${ENTRY} : ${COUNTER}"
	fi
    fi
done
