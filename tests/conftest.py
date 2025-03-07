import os
from unittest import mock

import pytest
from google.auth import environment_vars

import cpg_flow.inputs
import cpg_flow.metamist
import cpg_flow.workflow
import cpg_utils.config
import cpg_utils.hail_batch


@pytest.fixture(autouse=True, scope='function')
def pre_and_post_test():
    # Set a dummy google cloud project to avoid errors when running tests for tests
    # that use the google cloud.
    with mock.patch.dict(
        os.environ,
        {environment_vars.PROJECT: 'dummy-project-for-tests'},
    ):
        yield

    # Reset config paths to defaults
    cpg_utils.config.set_config_paths([])

    # Clear pre-existing state before running a new workflow. Must use setattr
    # for this to work so ignore flake8 B010.
    setattr(cpg_utils.config, '_config_paths', None)  # noqa: B010
    setattr(cpg_utils.config, '_config', None)  # noqa: B010
    setattr(cpg_utils.hail_batch, '_batch', None)  # noqa: B010
    setattr(cpg_flow.workflow, '_workflow', None)  # noqa: B010
    setattr(cpg_flow.inputs, '_cohort', None)  # noqa: B010
    setattr(cpg_flow.metamist, '_metamist', None)  # noqa: B010
    setattr(cpg_flow.inputs, '_multicohort', None)  # noqa: B010
