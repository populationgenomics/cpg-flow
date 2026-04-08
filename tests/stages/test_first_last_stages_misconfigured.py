"""
Test building stages DAG.
"""

import pytest
from pytest_mock import MockFixture

from tests import set_config
from tests.stages import D, run_workflow


@pytest.mark.parametrize('param', ['first_stages', 'last_stages'])
def test_unknown_stage_name(mocker: MockFixture, tmp_path, param):
    """Passing an unknown stage name in first_stages or last_stages raises WorkflowError."""
    conf = f"""
    [workflow]
    dataset_gcp_project = 'fewgenomes'
    access_level = 'test'
    dataset = 'fewgenomes'
    sequencing_type = 'genome'
    driver_image = 'stub'

    check_inputs = false
    check_intermediates = false
    check_expected_outputs = false

    {param} = ['NoSuchStage']

    [storage.default]
    default = '{tmp_path}'
    [storage.fewgenomes]
    default = '{tmp_path}'

    [hail]
    billing_project = 'fewgenomes'
    delete_scratch_on_exit = false
    backend = 'local'
    dry_run = true
    """

    set_config(conf, tmp_path / 'config.toml')
    from cpg_flow.workflow import WorkflowError

    with pytest.raises(WorkflowError, match=f'workflow/{param}.*NoSuchStage'):
        run_workflow(mocker, stages=[D])


def test_first_last_stages_misconfigured(mocker: MockFixture, tmp_path):
    """
    A -> B -> C -> D
    first_stages = [C]
    last_stages = [B]
    Will raise no stages to run
    """
    conf = f"""
    [workflow]
    dataset_gcp_project = 'fewgenomes'
    access_level = 'test'
    dataset = 'fewgenomes'
    sequencing_type = 'genome'
    driver_image = 'stub'

    check_inputs = false
    check_intermediates = false
    check_expected_outputs = false

    first_stages = ['C']
    last_stages = ['B']

    [storage.default]
    default = '{tmp_path}'
    [storage.fewgenomes]
    default = '{tmp_path}'

    [hail]
    billing_project = 'fewgenomes'
    delete_scratch_on_exit = false
    backend = 'local'
    dry_run = true
    """

    set_config(conf, tmp_path / 'config.toml')
    from cpg_flow.workflow import WorkflowError

    with pytest.raises(WorkflowError, match='No stages to run'):
        run_workflow(mocker, stages=[D])
