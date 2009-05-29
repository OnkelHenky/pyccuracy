#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.opensource.org/licenses/osl-3.0.php

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pmock import *;

from pyccuracy.result import Result
from pyccuracy.pyccuracy_core import Settings
from pyccuracy.fixture import Fixture
from pyccuracy.fixture_items import Story, Scenario, Action

summary_template = """================
Test Run Summary
================

Status: $run_status

Test Data Stats
---------------
Successful Stories......$successful_stories/$total_stories ($successful_story_percentage%)
Failed Stories..........$failed_stories/$total_stories ($failed_story_percentage%)
Successful Scenarios....$successful_scenarios/$total_scenarios ($successful_scenario_percentage%)
Failed Scenarios........$failed_scenarios/$total_scenarios ($failed_scenario_percentage%)"""

summary_template_failed_stories = """#if($has_failed_scenarios)


Failed Stories / Scenarios
--------------------------
TBW.
#end"""

def some_action():
    story = Story(as_a="Someone", i_want_to="Do Something", so_that="I'm Happy")
    scenario = story.append_scenario("1", "Something")
    return scenario.add_given(action_description="Some Action", execute_function=lambda: None, args=["s"], kwargs={"a":"b"})

def test_empty_result_returns_result():
    result = Result.empty()
    assert result is not None

def test_empty_result_returns_none_fixture():
    result = Result.empty()
    assert result.fixture is None

def test_see_summary_for_fixture():
    template_loader_mock = Mock()
    template_loader_mock.expects(once()) \
                        .load(eq("summary")) \
                        .will(return_value(summary_template))
    settings = Settings()
    fixture = Fixture()
    action = some_action()
    fixture.append_story(action.scenario.story)
    action.mark_as_successful()
    result = Result(fixture=fixture, template_loader=template_loader_mock)

    summary = result.summary_for(settings.default_culture)
    assert summary is not None

def test_see_summary_for_fixture_returns_proper_string():
    expected = """================
Test Run Summary
================

Status: SUCCESSFUL

Test Data Stats
---------------
Successful Stories......1/1 (100.00%)
Failed Stories..........0/1 (0.00%)
Successful Scenarios....1/1 (100.00%)
Failed Scenarios........0/1 (0.00%)"""

    template_loader_mock = Mock()
    template_loader_mock.expects(once()) \
                        .load(eq("summary")) \
                        .will(return_value(summary_template))
    settings = Settings()
    fixture = Fixture()
    action = some_action()
    fixture.append_story(action.scenario.story)
    action.mark_as_successful()
    result = Result(fixture=fixture, template_loader=template_loader_mock)

    summary = result.summary_for(settings.default_culture)
    assert summary == expected

def test_see_summary_for_fixture_returns_proper_string_for_failed_tests():
    expected = """================
Test Run Summary
================

Status: FAILED

Test Data Stats
---------------
Successful Stories......0/1 (0.00%)
Failed Stories..........1/1 (100.00%)
Successful Scenarios....0/1 (0.00%)
Failed Scenarios........1/1 (100.00%)"""

    template_loader_mock = Mock()
    template_loader_mock.expects(once()) \
                        .load(eq("summary")) \
                        .will(return_value(summary_template))
    settings = Settings()
    fixture = Fixture()
    action = some_action()
    fixture.append_story(action.scenario.story)
    action.mark_as_failed()
    result = Result(fixture=fixture, template_loader=template_loader_mock)

    summary = result.summary_for(settings.default_culture)
    assert summary == expected

def test_see_summary_for_fixture_returns_proper_string_for_no_tests():
    expected = """================
Test Run Summary
================

Status: UNKNOWN

Test Data Stats
---------------
Successful Stories......0/0 (0.00%)
Failed Stories..........0/0 (0.00%)
Successful Scenarios....0/0 (0.00%)
Failed Scenarios........0/0 (0.00%)"""

    template_loader_mock = Mock()
    template_loader_mock.expects(once()) \
                        .load(eq("summary")) \
                        .will(return_value(summary_template))
    settings = Settings()
    fixture = Fixture()
    result = Result(fixture=fixture, template_loader=template_loader_mock)

    summary = result.summary_for(settings.default_culture)
    assert summary == expected

def test_see_summary_for_fixture_returns_proper_failed_scenarios_string():
    expected = """================
Test Run Summary
================

Status: FAILED

Test Data Stats
---------------
Successful Stories......0/1 (0.00%)
Failed Stories..........1/1 (100.00%)
Successful Scenarios....0/1 (0.00%)
Failed Scenarios........1/1 (100.00%)

Failed Stories / Scenarios
--------------------------
TBW.
"""

    template_loader_mock = Mock()
    template_loader_mock.expects(once()) \
                        .load(eq("summary")) \
                        .will(return_value(summary_template + summary_template_failed_stories))
    settings = Settings()
    fixture = Fixture()
    result = Result(fixture=fixture, template_loader=template_loader_mock)
    action = some_action()
    fixture.append_story(action.scenario.story)
    action.mark_as_failed()

    summary = result.summary_for(settings.default_culture)
    assert summary == expected
