#!/usr/bin/env python3
import os
import sys
from pathlib import Path

from stages import BuildAPrimePyramid, CumulativeCalc, FilterEvens, GeneratePrimes

import hailtop.batch as hb

from cpg_flow.workflow import run_workflow
from cpg_utils.config import set_config_paths

TMP_DIR = os.getenv('TMP_DIR')
GSA_KEY_FILE = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
PYTHON_IMAGE = 'australia-southeast1-docker.pkg.dev/cpg-common/images/python:3.10-slim-bookworm'
CONFIG_FILE = str(Path(__file__).parent / 'config.toml')

message = "Hello, Hail Batch! I'm CPG flow, nice to meet you."


def run_batch_workflow():
    backend = hb.LocalBackend(tmp_dir=TMP_DIR, gsa_key_file=GSA_KEY_FILE)

    b = hb.Batch(
        name='cpg-flow-test',
        backend=backend,
        default_image=PYTHON_IMAGE,
    )
    j = b.new_job(name='say-hello')
    j.command(f'echo "{message}" > {j.outfile}')
    b.write_output(j.outfile, f'{TMP_DIR}/out.txt')

    print(f'Submitting batch {b.name}')
    b.run()
    print(f'Batch {b.name} complete')


def run_cpg_flow(dry_run=False):
    workflow = [GeneratePrimes, CumulativeCalc, FilterEvens, BuildAPrimePyramid]

    set_config_paths([CONFIG_FILE])
    run_workflow(stages=workflow, dry_run=dry_run)


def validate_batch_workflow():
    if not os.path.exists(f'{TMP_DIR}/out.txt'):
        print('Batch workflow failed')
        sys.exit(1)

    success = False
    with open(f'{TMP_DIR}/out.txt', 'r') as f:
        success = f.read().strip() == message

    print(f'Batch workflow {"succeeded" if success else "failed"}')
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    run_cpg_flow()
