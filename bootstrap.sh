#!/bin/bash

set -ex

# Install task
TASK_VERSION="v3.30.1"
TASK_PATH="/usr/local/bin/"
if [[ $(task --version 2>&1 | cut -d ' ' -f 3) != ${TASK_VERSION} ]]; then
    sudo bash -c "$(curl --location https://taskfile.dev/install.sh)" -- -b ${TASK_PATH} -d ${TASK_VERSION}
    sudo wget -O /usr/share/bash-completion/completions/task.bash \
        https://raw.githubusercontent.com/go-task/task/${TASK_VERSION}/completion/bash/task.bash
    cat ~/.bashrc | grep 'source /usr/share/bash-completion/completions/task.bash' ||
        echo "source /usr/share/bash-completion/completions/task.bash" >>~/.bashrc
fi
