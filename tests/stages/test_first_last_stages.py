"""
Test building stages DAG.
"""

from pytest_mock import MockFixture

from tests import set_config
from tests.stages import Arun_workflow, run_workflow


def test_first_last_stages(mocker: MockFixture, tmp_path):
    """
    A -> B -> C -> D
    first_stages = [B]
    last_stages = [C]
    Should run: B -> C
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

    first_stages = ['B']
    last_stages = ['C']

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
    run_workflow(mocker)

    from cpg_utils.hail_batch import get_batch

    print('Job by stage:', get_batch().job_by_stage)
    assert 'A' not in get_batch().job_by_stage
    assert get_batch().job_by_stage['B']['job_n'] == 1
    assert get_batch().job_by_stage['C']['job_n'] == 1
    assert 'D' not in get_batch().job_by_stage


def test_first_last_stages_shadow(mocker: MockFixture, tmp_path):
    """
    AA -> AC
       -> AB -> AD
             -> AE -> AF -> AG
             -> AG
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

    first_stages = ['AB']
    last_stages = ['AF']

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
    Arun_workflow(mocker)

    from cpg_utils.hail_batch import get_batch

    print('Job by stage:', get_batch().job_by_stage.keys())
    assert 'AA' not in get_batch().job_by_stage
    assert 'AG' not in get_batch().job_by_stage
    for inc_stage in ['AC', 'AB', 'AD', 'AE', 'AF']:
        assert get_batch().job_by_stage[inc_stage]['job_n'] == 1
