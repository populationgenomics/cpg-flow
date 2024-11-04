FROM australia-southeast1-docker.pkg.dev/analysis-runner/images/driver:latest

RUN pip install metamist
COPY README.md .
COPY cpg_workflows cpg_workflows
RUN pip install .
