"""
Test building Workflow object.
"""

from unittest import mock

from cpg_flow.targets import Cohort, MultiCohort, SequencingGroup
from cpg_flow.workflow import path_walk
from cpg_utils import Path, to_path

from tests import set_config

TOML = """
[workflow]
dataset_gcp_project = 'fewgenomes'
access_level = 'test'
dataset = 'fewgenomes'
driver_image = 'test'
sequencing_type = 'genome'

check_inputs = false
check_intermediates = false
check_expected_outputs = false
path_scheme = 'local'

[storage.default]
default = "{directory}"

[storage.fewgenomes]
default = "{directory}"

[hail]
billing_project = 'fewgenomes'
delete_scratch_on_exit = false
backend = 'local'
"""


def mock_create_create_cohort(*_) -> MultiCohort:
    m = MultiCohort()
    c = m.create_cohort(id='COH123', name='fewgenomes')
    ds = m.create_dataset('my_dataset')

    def add_sg(id, external_id):
        return ds.add_sequencing_group(
            id=id,
            external_id=external_id,
            sequencing_type='genome',
            sequencing_technology='short-read',
            sequencing_platform='illumina',
        )

    c.add_sequencing_group_object(add_sg('CPGAA', external_id='SAMPLE1'))
    c.add_sequencing_group_object(add_sg('CPGBB', external_id='SAMPLE2'))
    return m


@mock.patch('cpg_flow.inputs.create_multicohort', mock_create_create_cohort)
def test_workflow(tmp_path):
    """
    Testing running a workflow from a mock cohort.
    """
    conf = TOML.format(directory=tmp_path)
    set_config(conf, tmp_path / 'config.toml')

    from cpg_flow.inputs import get_multicohort
    from cpg_flow.stage import (
        CohortStage,
        SequencingGroupStage,
        StageInput,
        StageOutput,
        stage,
    )
    from cpg_flow.workflow import run_workflow
    from cpg_utils.config import dataset_path
    from cpg_utils.hail_batch import get_batch

    output_path = to_path(dataset_path('cohort.tsv'))

    multi_cohort = get_multicohort()

    assert len(multi_cohort.get_sequencing_groups()) == 2

    assert multi_cohort.alignment_inputs_hash is None
    mc_hash = multi_cohort.get_alignment_inputs_hash()
    assert multi_cohort.alignment_inputs_hash == mc_hash
    assert mc_hash == 'e3b0c44298fc1c149afbf4c8996fb92427ae41_2'

    @stage
    class MySequencingGroupStage(SequencingGroupStage):
        """
        Just a sequencing-group-level stage.
        """

        def expected_outputs(self, sequencing_group: SequencingGroup) -> Path:
            return to_path(dataset_path(f'{sequencing_group.id}.tsv'))

        def queue_jobs(self, sequencing_group: SequencingGroup, inputs: StageInput) -> StageOutput | None:
            j = get_batch().new_job('SequencingGroup job', self.get_job_attrs(sequencing_group))
            j.command(f'echo {sequencing_group.id}_done >> {j.output}')
            get_batch().write_output(j.output, str(self.expected_outputs(sequencing_group)))
            print(f'Writing to {self.expected_outputs(sequencing_group)}')
            return self.make_outputs(sequencing_group, self.expected_outputs(sequencing_group))

    @stage(required_stages=MySequencingGroupStage)
    class MyCohortStage(CohortStage):
        """
        Just a cohort-level stage.
        """

        def expected_outputs(self, cohort: Cohort) -> Path:
            return output_path

        def queue_jobs(self, cohort: Cohort, inputs: StageInput) -> StageOutput | None:
            path_by_sg = inputs.as_path_by_target(MySequencingGroupStage)
            assert len(path_by_sg) == len(cohort.get_sequencing_groups())
            j = get_batch().new_job('Cohort job', self.get_job_attrs(cohort))
            j.command(f'touch {j.output}')
            for _, sg_result_path in path_by_sg.items():
                input_file = get_batch().read_input(str(sg_result_path))
                j.command(f'cat {input_file} >> {j.output}')
            get_batch().write_output(j.output, str(self.expected_outputs(cohort)))
            print(f'Writing to {self.expected_outputs(cohort)}')
            return self.make_outputs(cohort, self.expected_outputs(cohort))

    run_workflow(stages=[MyCohortStage])

    print(f'Checking result in {output_path}:')
    with output_path.open() as f:
        result = f.read()
        assert result.split() == ['CPGAA_done', 'CPGBB_done'], result


def test_path_walk():
    """
    tests the recursive path walk to find all stage outputs
    the recursive method can unpack any nested structure
    end result is a set of all Paths
    Note: Strings in this dict are not turned into Paths
    """

    exp = {
        'a': to_path('this.txt'),
        'b': [to_path('that.txt'), {'c': to_path('the_other.txt')}],
        'd': 'string.txt',
    }
    act = path_walk(exp)
    assert act == {to_path('this.txt'), to_path('that.txt'), to_path('the_other.txt')}
