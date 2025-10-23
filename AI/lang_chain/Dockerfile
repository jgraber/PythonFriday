FROM python:3.13-trixie

RUN apt-get update -qq

WORKDIR /workspace

COPY csv_requirements.txt /workspace/csv_requirements.txt
COPY csv_agent.py /workspace/csv_agent.py

RUN pip install -U -r csv_requirements.txt

CMD ["/bin/bash"]