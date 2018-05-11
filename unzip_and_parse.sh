#!/bin/bash

TOPURL="https://academicgraphv1wu.blob.core.windows.net/aminer/"
TMPJSON="tmp_json.json"

for i in $(seq 4 8); 
do 
    FILENAME=mag_papers_${i}.zip
    echo "Getting ${FILENAME}" >> out.log
    wget ${TOPURL}${FILENAME} &> /dev/null
    ls -l ${FILENAME}
    echo "Got ${FILENAME} with contents:" >> out.log
    ZIPPEDFILES=$(zipinfo -1 ${FILENAME})
    echo -e "${ZIPPEDFILES}" >> out.log
    for ZIPPED in ${ZIPPEDFILES};
    do
	unzip -p ${FILENAME} ${ZIPPED} > ${TMPJSON}
	echo -e "\tGot ${TMPJSON} from ${ZIPPED}" >> out.log
	python json_to_db.py >> out.log
	if [[ $? != 0 ]]; then
	    echo -e "\t\tFAIL"
	    return
	fi
	echo -e "\t\t ...dumped in the db" >> out.log
	rm ${TMPJSON}
    done
    rm ${FILENAME}
done
