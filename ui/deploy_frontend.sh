#! /bin/bash

# set -e
# sudo -v

BOLD=$(tput bold)
GREEN=$(tput setaf 2)
BLUE=$(tput setaf 4)
MAGENTA=$(tput setaf 5)
RESET=$(tput sgr0)

SPIN='-\|/'
function wait_while() {
    echo -ne " "
    i=0
    while $1 2>/dev/null; do
        i=$(((i + 1) % 4))
        echo -ne "\b${SPIN:$i:1}"
        sleep .1
    done
    echo -ne "\b"
}

function wait_for_finish() {
    PROGRAM=$1
    function is_running() {
        kill -0 $PROGRAM
    }
    wait_while is_running
}

# Moving into working dir
cd upsBot-Client

printf "Creating Docker Image..."
docker build -t upsbot-frontend . &
wait_for_finish $!
echo "  "
echo "${BLUE}${BOLD}                     **** Image Created ****               ${RESET} ${BOLD}"
echo "  "

printf "Taging Image..."
docker tag upsbot-frontend gcr.io/gcp-ait-mod-sand-dev/upsbot-frontend &
wait_for_finish $!
echo "Done."

printf "Pushing Image to GCR..."
docker push gcr.io/gcp-ait-mod-sand-dev/upsbot-frontend &
wait_for_finish $!
echo "  "
echo "${MAGENTA}${BOLD}                     **** Image Pushed to GCR ****           ${RESET} ${BOLD}"
echo "  "

# Deploying Image to Cloud Run
gcloud run deploy upsbot-frontend --region us-east4 --image gcr.io/gcp-ait-mod-sand-dev/upsbot-frontend:latest &
wait_for_finish $!
echo "  "
echo "${GREEN}${BOLD}                   **** Frontend Deployed ****                ${RESET} ${BOLD}"
echo "  "
