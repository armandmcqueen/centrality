#!/usr/bin/env bash

# Wrapper around streamlit that handles loading the config file and passing it to streamlit.

set -e

# Load a config and save it to an environment variable. If not argument was passed, load the default config
if [ $# -eq 0 ]; then
    $(python config_util.py set)
else
    echo "Loading config $1"
    $(python config_util.py set -f $1)
fi

env | grep CENT
pushd rapidui
streamlit run Home.py
popd

# Unset the environment variable. Probably not needed
$(python config_util.py unset)
