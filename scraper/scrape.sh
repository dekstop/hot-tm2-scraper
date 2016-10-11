#!/bin/bash

#mydir=$( cd "$( dirname "$0" )" && pwd )
#datadir=${mydir}/data

curl='curl --silent --show-error'
agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2'


if [[ $# -ne 3 ]]
then
  echo "Usage : $0 <outdir> <min_id> <max_id>"
  exit 1
fi

datadir=$1
min_id=$2
max_id=$3

mkdir -p $datadir > /dev/null 2>&1

for id in `seq $min_id $max_id`
do
  status=`$curl -I http://tasks.hotosm.org/project/${id} \
  -H 'Referer: http://tasks.hotosm.org/' \
  -H "User-Agent: ${agent}" \
  --compressed | head -n 1 | cut -d " " -f 2` || exit 1
  
  if [ "$status" -eq "404" ]
  then
    echo "Project does not exist: $id"
    exit 1
  elif [ "$status" -eq "302" ]
  then
    echo "Skipping project: $id"
    sleep 1
  else
    echo "Loading data for project: $id"
    sleep 1
   
    mkdir -p ${datadir}/${id}

    # project page
    echo "/project/${id}"
    $curl http://tasks.hotosm.org/project/${id} \
      -H 'Referer: http://tasks.hotosm.org/' \
      -H "User-Agent: ${agent}" \
      --compressed > ${datadir}/${id}/index.html || exit 1
    sleep 1
    
    # stats
    echo "/project/${id}/stats"
    $curl http://tasks.hotosm.org/project/${id}/stats \
      -H 'Accept: application/json, */*' \
      -H "Referer: http://tasks.hotosm.org/project/${id}" \
      -H "User-Agent: ${agent}" \
      --compressed > ${datadir}/${id}/stats.json || exit 1
    sleep 1

    # tasks
    echo "/project/${id}/tasks.json"
    $curl http://tasks.hotosm.org/project/${id}/tasks.json \
      -H 'Accept: application/json, */*' \
      -H "Referer: http://tasks.hotosm.org/project/${id}" \
      -H "User-Agent: ${agent}" \
      --compressed > ${datadir}/${id}/tasks.json || exit 1
    sleep 1

    # contributors
    echo "/project/${id}/contributors"
    $curl http://tasks.hotosm.org/project/${id}/contributors \
      -H 'Accept: application/json, text/javascript, */*; q=0.01' \
      -H 'X-Requested-With: XMLHttpRequest' \
      -H "Referer: http://tasks.hotosm.org/project/${id}" \
      -H "User-Agent: ${agent}" \
      --compressed > ${datadir}/${id}/contributors.json || exit 1
    sleep 1
  fi
done
