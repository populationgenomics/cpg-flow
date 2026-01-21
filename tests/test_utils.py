import logging
from collections.abc import Iterable
from copy import deepcopy
from itertools import product

import pytest

from cpg_flow.utils import dependency_handler


class MockJob:
    """
    A mock class to simulate hailtop.batch.job.Job
    """

    def __init__(self, name: str):
        self.name = name
        self._dependencies: set[MockJob] = set()

    def depends_on(self, *jobs):
        """
        Simulate depends_on by adding jobs to a set
        """
        for job in jobs:
            self._dependencies.add(job)

    def __repr__(self):
        return f'MockJob({self.name})'

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __hash__(self) -> int:
        return int(self.name[-1])


@pytest.mark.parametrize(
    ['new_dep', 'old_dep', 'append_arg', 'expect_dep', 'expect_append'],
    [
        pytest.param(None, None, True, False, False),  # null case
        pytest.param(MockJob('job1'), None, True, False, False),  # null case
        pytest.param(None, MockJob('job1'), True, False, False),  # null case
        pytest.param([MockJob('job1')], None, True, False, False),  # null case
        pytest.param(None, [MockJob('job1')], True, False, False),  # null case
    ],
)
def test_all_dependency_handlers_null(new_dep, old_dep, append_arg, expect_dep: bool, expect_append: bool, caplog):
    caplog.set_level(logging.DEBUG)

    dependency_handler(target=new_dep, tail=old_dep, append_or_extend=append_arg)
    assert 'No target or tail provided' in caplog.text


@pytest.mark.parametrize(
    ['new_dep', 'old_dep', 'append_arg', 'expect_append'],
    [
        pytest.param(MockJob('job1'), [MockJob('job2'), MockJob('job3')], True, True),  # set and append
        pytest.param([MockJob('job1'), MockJob('job2')], [MockJob('job3')], True, True),  # set and append
        pytest.param([MockJob('job1'), MockJob('job2')], MockJob('job3'), False, False),  # set and don't append
        pytest.param([MockJob('job1'), MockJob('job2')], MockJob('job3'), True, True),  # set and fail to append
    ],
)
def test_all_dependency_handlers_real(new_dep, old_dep, append_arg, expect_append: bool, caplog):
    og_tail_list = deepcopy(old_dep if isinstance(old_dep, Iterable) else [old_dep])

    dependency_handler(target=new_dep, tail=old_dep, append_or_extend=append_arg)

    new_dep_list = new_dep if isinstance(new_dep, Iterable) else [new_dep]
    new_tail_list = old_dep if isinstance(old_dep, Iterable) else [old_dep]

    # dependency setting, we expect all the original tail list to be in the current target dependencies
    for each_new, each_old in product(new_dep_list, og_tail_list):
        assert each_old in each_new._dependencies

    # appending, we expect all the original targets to be in the new tail
    if expect_append:
        for each_new in new_dep_list:
            try:
                assert each_new in new_tail_list
            except AssertionError:
                assert 'Append requested, but tail is not an iterable:' in caplog.text
    else:
        for each_new in new_dep_list:
            assert each_new not in new_tail_list


# def test_dependency_handler_none():
#     """
#     Test that None inputs are handled gracefully
#     """
#     # Should not raise exception
#     dependency_handler(None, None)
#
#     job = MockJob('job1')
#     dependency_handler(job, None)
#     assert len(job._dependencies) == 0
#
#     dependency_handler(None, job)
#
#
# def test_dependency_handler_single_single():
#     """
#     Test 1:1 dependency
#     """
#     job1 = MockJob('source')
#     job2 = MockJob('dependency')
#
#     dependency_handler(job1, job2)
#     assert job2 in job1._dependencies
#
#
# def test_dependency_handler_list_single():
#     """
#     Test Many:1 dependency
#     """
#     job1 = MockJob('source1')
#     job2 = MockJob('source2')
#     dep = MockJob('dependency')
#
#     dependency_handler([job1, job2], dep)
#     assert dep in job1._dependencies
#     assert dep in job2._dependencies
#
#
# def test_dependency_handler_single_list():
#     """
#     Test 1:Many dependency
#     """
#     job = MockJob('source')
#     dep1 = MockJob('dependency1')
#     dep2 = MockJob('dependency2')
#
#     dependency_handler(job, [dep1, dep2])
#     assert dep1 in job._dependencies
#     assert dep2 in job._dependencies
#
#
# def test_dependency_handler_append_list():
#     """
#     Test appending to list
#     """
#     job = MockJob('new_job')
#     dep1 = MockJob('existing_job')
#     prior_jobs = [dep1]
#
#     dependency_handler(job, prior_jobs, append_or_extend=True)
#
#     # Check dependency set
#     assert dep1 in job._dependencies
#     # Check list extension
#     assert job in prior_jobs
#     assert len(prior_jobs) == 2
#
#
# def test_dependency_handler_no_append_list():
#     """
#     Test NOT appending to list
#     """
#     job = MockJob('new_job')
#     dep1 = MockJob('existing_job')
#     prior_jobs = [dep1]
#
#     dependency_handler(job, prior_jobs, append_or_extend=False)
#
#     # Check dependency set
#     assert dep1 in job._dependencies
#     # Check list NOT extended
#     assert job not in prior_jobs
#     assert len(prior_jobs) == 1
#
#
# def test_dependency_handler_update_set():
#     """
#     Test updating a set
#     """
#     job = MockJob('new_job')
#     dep1 = MockJob('existing_job')
#     prior_jobs = {dep1}
#
#     dependency_handler(job, prior_jobs, append_or_extend=True)
#
#     # Check dependency set
#     assert dep1 in job._dependencies
#     # Check set update
#     assert job in prior_jobs
#     assert len(prior_jobs) == 2
