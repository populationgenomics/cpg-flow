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
    ['new_dep', 'old_dep', 'error'],
    [
        pytest.param(None, None, 'No Target(s), cannot set depends_on relationships'),
        pytest.param(MockJob('job1'), None, 'No Tail, cannot set depends_on relationships or append'),
        pytest.param(None, MockJob('job1'), 'No Target(s), cannot set depends_on relationships'),
        pytest.param(None, [MockJob('job1')], 'No Target(s), cannot set depends_on relationships'),
    ],
)
def test_all_dependency_handlers_null(new_dep, old_dep, error: str, caplog):
    caplog.set_level(logging.DEBUG)

    dependency_handler(target=new_dep, tail=old_dep)
    assert error in caplog.text


@pytest.mark.parametrize(
    ['new_dep', 'old_dep', 'append_arg', 'expect_append'],
    [
        pytest.param(MockJob('job1'), [MockJob('job2'), MockJob('job3')], True, True),  # set and append
        pytest.param([MockJob('job1'), MockJob('job2')], [MockJob('job3')], True, True),  # set and append
        pytest.param([MockJob('job1'), MockJob('job2')], MockJob('job3'), False, False),  # set and don't append
        pytest.param([MockJob('job1'), MockJob('job2')], MockJob('job3'), True, True),  # set and fail to append
        pytest.param([MockJob('job1')], [], True, True),  # set and fail to append
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


def test_depends_on_none(caplog):
    caplog.set_level(logging.WARNING)
    with pytest.raises(AttributeError):
        dependency_handler(
            target=[MockJob('job1'), None], tail=[MockJob('job2'), MockJob('job3')], append_or_extend=False
        )

    assert 'Failure to set dependencies between target ' in caplog.text


def test_depends_on_only_last():
    # new behaviour - what if we only want to dependency set on the last in a job series
    target = MockJob('job1')
    tail = [MockJob('job2'), MockJob('job3'), MockJob('job4')]
    dependency_handler(target=target, tail=tail, only_last=True)

    assert target._dependencies == {MockJob('job4')}
    assert len(tail) == 4
