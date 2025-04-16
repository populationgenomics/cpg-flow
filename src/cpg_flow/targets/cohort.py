"""
This module defines the `Cohort` class, which represents a cohort target in the workflow.
A cohort consists of all sequencing groups from a single CustomCohort, potentially spanning multiple datasets.

Classes:
    Cohort: Represents a cohort target in the workflow.

Usage:
    The `Cohort` class is used to manage and analyze sequencing groups within a cohort.
    It provides methods to add sequencing groups, retrieve sequencing groups, write PED files,
    and export cohort data to TSV files.

Example:
    cohort = Cohort(name="example_cohort")
    cohort.add_sequencing_group_object(sequencing_group)
    ped_file_path = cohort.write_ped_file()
    tsv_file_path = cohort.to_tsv()

"""

from typing import TYPE_CHECKING

import pandas as pd
from loguru import logger

from cpg_flow.targets import Dataset, Target
from cpg_utils import Path, to_path
from cpg_utils.config import config_retrieve

if TYPE_CHECKING:
    from cpg_flow.targets import SequencingGroup
    from cpg_flow.targets.multicohort import MultiCohort


class Cohort(Target):
    """
    Represents a "cohort" target - all sequencing groups from a single CustomCohort (potentially spanning multiple datasets) in the workflow.
    Analysis dataset name is required and will be used as the default name for the
    cohort.
    """

    def __init__(
        self,
        multicohort: 'MultiCohort',
        id: str | None = None,
        name: str | None = None,
        dataset: str | None = None,
    ) -> None:
        super().__init__()

        # This is the dataset name specified in the workflow config
        config_dataset = config_retrieve(['workflow', 'dataset'])

        self.id = id or config_dataset
        self.name = name or config_dataset

        # This value should be populated by the cohort_dataset parameter
        # which represents the dataset that the cohort is associated with
        # If no cohort dataset is provided it will default to the analysis dataset
        self.dataset = Dataset(name=dataset or config_dataset, multicohort=multicohort)

        self._sequencing_group_by_id: dict[str, SequencingGroup] = {}

    def __repr__(self):
        return f'Cohort("{self.id}", {len(self._sequencing_group_by_id)} SGs)'

    @property
    def target_id(self) -> str:
        """Unique target ID"""
        return self.id

    def get_cohort_id(self) -> str:
        """Get the cohort ID"""
        return self.id

    def write_ped_file(
        self,
        out_path: Path | None = None,
        use_participant_id: bool = False,
    ) -> Path:
        """
        Create a PED file for all samples in the whole cohort
        PED is written with no header line to be strict specification compliant
        """
        datas = []
        for sequencing_group in self.get_sequencing_groups():
            datas.append(
                sequencing_group.pedigree.get_ped_dict(
                    use_participant_id=use_participant_id,
                ),
            )
        if not datas:
            raise ValueError(f'No pedigree data found for {self.id}')
        df = pd.DataFrame(datas)

        if out_path is None:
            out_path = self.dataset.tmp_prefix() / 'ped' / f'{self.get_alignment_inputs_hash()}.ped'

        if not config_retrieve(['workflow', 'dry_run'], False):
            with out_path.open('w') as fp:
                df.to_csv(fp, sep='\t', index=False, header=False)
        return out_path

    def add_sequencing_group_object(
        self,
        s: 'SequencingGroup',
        allow_duplicates: bool = True,
    ):
        """
        Add a sequencing group object to the Cohort.
        Args:
            s: SequencingGroup object
            allow_duplicates: if True, allow adding the same object twice
        """
        if s.id in self._sequencing_group_by_id:
            if allow_duplicates:
                logger.debug(
                    f'SequencingGroup {s.id} already exists in the Cohort {self.name}',
                )
                return self._sequencing_group_by_id[s.id]
            raise ValueError(
                f'SequencingGroup {s.id} already exists in the Cohort {self.name}',
            )
        self._sequencing_group_by_id[s.id] = s

    def get_sequencing_groups(
        self,
        only_active: bool = True,
    ) -> list['SequencingGroup']:
        """
        Gets a flat list of all sequencing groups from all datasets.
        Include only "active" sequencing groups (unless only_active is False)
        """
        return [s for s in self._sequencing_group_by_id.values() if (s.active or not only_active)]

    def get_job_attrs(self) -> dict:
        """
        Attributes for Hail Batch job.
        Adding the list of all SGs is not scalable, and will break GCP label limits
        It's not completely clear what should live here
        """
        return {
            # 'sequencing_groups': self.get_sequencing_group_ids(),
        }

    def get_job_prefix(self) -> str:
        """
        Prefix job names.
        """
        return ''

    def to_tsv(self) -> str:
        """
        Export to a parsable TSV file
        """
        assert self.get_sequencing_groups()
        tsv_path = self.dataset.tmp_prefix() / 'samples.tsv'
        df = pd.DataFrame(
            {
                's': s.id,
                'gvcf': s.gvcf or '-',
                'sex': s.meta.get('sex') or '-',
                'continental_pop': s.meta.get('continental_pop') or '-',
                'subcontinental_pop': s.meta.get('subcontinental_pop') or '-',
            }
            for s in self.get_sequencing_groups()
        ).set_index('s', drop=False)
        with to_path(tsv_path).open('w') as f:
            df.to_csv(f, index=False, sep='\t', na_rep='NA')
        return tsv_path
