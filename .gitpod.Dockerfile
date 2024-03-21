# FROM gitpod/workspace-full:2024-03-17-11-10-27
FROM gitpod/workspace-python-3.11:2024-03-20-07-19-19
USER gitpod
RUN sudo apt update -q && \
    sudo apt install -yq redis && \
    sudo pip install boto3 requests uvicorn