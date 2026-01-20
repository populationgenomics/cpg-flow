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


def test_dependency_handler_none():
    """
    Test that None inputs are handled gracefully
    """
    # Should not raise exception
    dependency_handler(None, None)

    job = MockJob('job1')
    dependency_handler(job, None)
    assert len(job._dependencies) == 0

    dependency_handler(None, job)


def test_dependency_handler_single_single():
    """
    Test 1:1 dependency
    """
    job1 = MockJob('source')
    job2 = MockJob('dependency')

    dependency_handler(job1, job2)
    assert job2 in job1._dependencies


def test_dependency_handler_list_single():
    """
    Test Many:1 dependency
    """
    job1 = MockJob('source1')
    job2 = MockJob('source2')
    dep = MockJob('dependency')

    dependency_handler([job1, job2], dep)
    assert dep in job1._dependencies
    assert dep in job2._dependencies


def test_dependency_handler_single_list():
    """
    Test 1:Many dependency
    """
    job = MockJob('source')
    dep1 = MockJob('dependency1')
    dep2 = MockJob('dependency2')

    dependency_handler(job, [dep1, dep2])
    assert dep1 in job._dependencies
    assert dep2 in job._dependencies


def test_dependency_handler_append_list():
    """
    Test appending to list
    """
    job = MockJob('new_job')
    dep1 = MockJob('existing_job')
    prior_jobs = [dep1]

    dependency_handler(job, prior_jobs, append_or_extend=True)

    # Check dependency set
    assert dep1 in job._dependencies
    # Check list extension
    assert job in prior_jobs
    assert len(prior_jobs) == 2


def test_dependency_handler_no_append_list():
    """
    Test NOT appending to list
    """
    job = MockJob('new_job')
    dep1 = MockJob('existing_job')
    prior_jobs = [dep1]

    dependency_handler(job, prior_jobs, append_or_extend=False)

    # Check dependency set
    assert dep1 in job._dependencies
    # Check list NOT extended
    assert job not in prior_jobs
    assert len(prior_jobs) == 1


def test_dependency_handler_update_set():
    """
    Test updating a set
    """
    job = MockJob('new_job')
    dep1 = MockJob('existing_job')
    prior_jobs = {dep1}

    dependency_handler(job, prior_jobs, append_or_extend=True)

    # Check dependency set
    assert dep1 in job._dependencies
    # Check set update
    assert job in prior_jobs
    assert len(prior_jobs) == 2
