#!/bin/bash

set -o errexit
set -o nounset
#set -o xtrace #uncomment for debug

if [ $# -eq 0 ]; then
    echo "No arguments supplied. Required arugments: -t <TAG> -r <REGISTRY>"
    exit 1
fi

while getopts t:r: option
do
case "${option}"
in
t) TAG=${OPTARG};;
r) REGISTRY=${OPTARG};;
esac
done

TRAINING=training:$TAG
PREDICTION=prediction:$TAG
MODEL_RUNNER=model-runner:$TAG

docker build -t $TRAINING -t $REGISTRY/$TRAINING ./training
docker push $REGISTRY/$TRAINING

docker build -t $PREDICTION -t $REGISTRY/$PREDICTION ./prediction
docker push $REGISTRY/$PREDICTION

docker build -t $MODEL_RUNNER -t $REGISTRY/$MODEL_RUNNER ./model-runner
docker push $REGISTRY/$MODEL_RUNNER


