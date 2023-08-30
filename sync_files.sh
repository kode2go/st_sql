#!/bin/bash
# This script will sync up GPU data from LENGAU
# mkdir logs
pushd logs
rsync -arvz --progress -e ssh bbarsch@scp.chpc.ac.za:/mnt/lustre/logs/gpu .
popd
