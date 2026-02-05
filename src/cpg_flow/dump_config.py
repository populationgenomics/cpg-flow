"""
Helper to dump the current MultiCohort object to a JSON file.
"""

import json
from typing import Any

from cpg_flow.inputs import create_multicohort
from cpg_flow.targets import MultiCohort, SequencingGroup


def dump_multicohort_from_metamist(cohort_ids: list[str], output_path: str):
    """
    Creates a MultiCohort from Metamist and dumps it to a JSON file.
    """
    multicohort = create_multicohort(tuple(cohort_ids))
    data = serialize_multicohort(multicohort)
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)


def serialize_multicohort(multicohort: MultiCohort) -> dict[str, Any]:
    """
    Serializes a MultiCohort object to a dictionary.
    """
    return {
        'multicohort': {
            'hash': multicohort.get_alignment_inputs_hash(),
            'dataset': multicohort.analysis_dataset.name,
        },
        'sequencing_groups': [serialize_sequencing_group(sg) for sg in multicohort.get_sequencing_groups()],
        'cohorts': {
            cohort.id: {
                'dataset': cohort.dataset.name,
                'id': cohort.id,
                'name': cohort.name,
                'sequencing_group_ids': cohort.get_sequencing_group_ids(),
            }
            for cohort in multicohort.get_cohorts()
        },
        'datasets': {
            dataset.name: {
                'hash': dataset.get_alignment_inputs_hash(),
                'sequencing_group_ids': dataset.get_sequencing_group_ids(),
            }
            for dataset in multicohort.get_datasets()
        },
    }


def serialize_sequencing_group(sg: SequencingGroup) -> dict[str, Any]:
    """
    Serializes a SequencingGroup object to a dictionary.
    """
    data = {
        'id': sg.id,
        'dataset': sg.dataset.name,
        'external_id': sg.external_id,
        'participant_id': sg.participant_id,
        'meta': sg.meta,
        'sequencing_type': sg.sequencing_type,
        'sequencing_technology': sg.sequencing_technology,
        'sequencing_platform': sg.sequencing_platform,
        'pedigree': sg.pedigree.get_ped_dict(),
        'assays': [
            {
                'id': assay.id,
                'meta': assay.meta,
                'type': assay.assay_type,
            }
            for assay in (sg.assays or [])
        ],
    }

    if sg.alignment_input:
        # We need to handle different types of alignment inputs
        # For now, we'll just store the string representation or a simplified dict
        # Ideally, we should have a proper serialization for AlignmentInput
        pass  # TODO: Implement AlignmentInput serialization if needed for reconstruction

    # Analysis paths
    analysis = {}
    if sg.gvcf:
        analysis['gvcf'] = str(sg.gvcf.path)
    if sg.cram:
        analysis['cram'] = str(sg.cram.path)
        if sg.cram.index_path:
            analysis['cram_index'] = str(sg.cram.index_path)

    if analysis:
        data['analysis'] = analysis

    return data
