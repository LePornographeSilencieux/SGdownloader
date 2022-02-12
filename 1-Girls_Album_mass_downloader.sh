#! /bin/sh

#USERNAME="$1"
#PASSWORD="$2"
#shift
#shift

COOKIE_FILE="$1"
shift

WAITING_TIME=10

SCRIPT_PYTHON_1="./src/SG_gallery_downloader.py"

if [ $# -lt 1 ]; then
    echo "Missing arguments"
    echo "$0 cookie_file.txt ListOfAlbums.txt [...]"
    echo ""
    echo "Format of ListOfAlbums.txt :"
    echo "https://www.suicidegirls.com/girls/braaa/album/4900880/crumbs/"
    echo "https://www.suicidegirls.com/girls/valeriya/album/4882585/une-fleur-rebelle/"
    echo "..."
    echo ""
    exit -1
fi

source ./functions.sh

########################################

ERROR_STR=
ERROR=0
for ARG in "$@"
do
    if [ -f "${ARG}" ]; then
	IN_NAME="${ARG}"
	BASENAME=`basename "${IN_NAME}"`
	OUTPUT_NAME="${OUTPUT_PREFIX}${BASENAME}"
	echo "-- ${BASENAME} --"

	while IFS="" read -r line || [ -n "${line}" ]
	do
	    echo ${line}
	    ${PYTHON} ${SCRIPT_PYTHON_1} -c "${COOKIE_FILE}" -u "${line}"
#	    ${PYTHON} ${SCRIPT_PYTHON_1} \
#		      -l "${USERNAME}" -p "${PASSWORD}" \
#		      -u "${line}"
	    if [ $? -ne 0 ]; then
		ERROR_STR="${line}\n${ERROR_STR}"
		ERROR=1
	    fi
	    echo "------------------------------------------------"
	    sleep ${WAITING_TIME}
	done < "${IN_NAME}"
    fi
done

if [ ${ERROR} -ne 0 ]; then
    echo "Errors on sets :"
    echo -e "${ERROR_STR}"
fi
