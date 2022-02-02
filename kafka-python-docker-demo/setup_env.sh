#!/bin/bash
#
# Install virtual env

# Variables
VENV_INSTALL_DIR=${HOME}/venv
VENV_INSTALL_NAME=kafka-python-demo

# Make dir
mkdir -p ${VENV_INSTALL_DIR}

# Install venv
python3 -m venv ${VENV_INSTALL_DIR}/${VENV_INSTALL_NAME}

# # Activate env and install reqs
# source venv/bin/activate
# pip3 install -r requirements.txt