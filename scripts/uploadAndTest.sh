#!/usr/bin/env bash
#Always execute from the root directory

user="pi"
ip="192.168.1.123"
srcFolder="./src"
destFolder="/home/pi/test"
privateKey="~/.ssh/workLaptopIsaac"

echo "Using Pi at $ip"

echo "Removing contents of existing test directory..."
ssh $user@$ip -i $privateKey "rm -rf $destFolder/*"

echo "Uploading hardware folder to Pi..."
scp -i $privateKey -r $srcFolder $user@$ip:$destFolder

echo "Executing Python3 test..."
ssh $user@$ip -i $privateKey "python3 $destFolder/src/main.py"

echo "SUCCESS!"