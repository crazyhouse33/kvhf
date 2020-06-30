#!/bin/bash
# This is a script to allow for people to easely use this repo hook. .githooks should be able to be versioned but its not an option unfortunally

githooks=$(git rev-parse --show-toplevel)"/.git/hooks"
echo $githooks

ln -s $(realpath .pre-commit) $githooks/pre-commit
ln -s $(realpath .pre-push) $githooks/pre-push
