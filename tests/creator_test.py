"""
Test Creator module.
This module contains tests for Creator objects.
"""

from datetime import date
from decimal import Decimal

import pytest

from esak import exceptions


def test_known_creator(talker):
    jason = talker.creator(11463)
    assert jason.first_name == "Jason"
    assert jason.last_name == "Aaron"
    assert jason.id == 11463
    assert jason.thumbnail == "http://i.annihil.us/u/prod/marvel/i/mg/7/10/5cd9c7870670e.jpg"

    assert 16450 in [s.id for s in jason.series]
    assert len(jason.series[:5]) == 5
    assert len(jason.series) == len([x for x in jason.series if x.id > 3])

    assert len(jason.stories) == 20
    assert jason.stories[0].id == 32907
    assert jason.stories[0].name == "Man In The Pit 1 of 1"
    assert jason.stories[0].type == "interiorStory"
    assert jason.stories[0].resource_uri == "http://gateway.marvel.com/v1/public/stories/32907"

    assert len(jason.comics) == 20
    assert jason.comics[0].id == 45762
    assert jason.comics[0].name == "A+X Vol. 1: = Awesome (Trade Paperback)"
    assert jason.comics[0].resource_uri == "http://gateway.marvel.com/v1/public/comics/45762"

    assert len(jason.series) == 20
    assert jason.series[11].id == 24229
    assert jason.series[11].name == "Avengers (2018 - Present)"
    assert jason.series[11].resource_uri == "http://gateway.marvel.com/v1/public/series/24229"


def test_bad_creator(talker):
    with pytest.raises(exceptions.ApiError):
        talker.creator(-1)


def test_pulls_verbose(talker):
    creators = talker.creators_list(
        {
            "orderBy": "modified",
        }
    )
    c_iter = iter(creators)
    assert next(c_iter).full_name == "Sean Cooke"
    assert next(c_iter).full_name, "Mark Shultz"
    assert next(c_iter).full_name, "Miles Lane"
    assert len(creators) > 0


def test_creator_comics(talker):
    jason = talker.creator_comics(11463)
    assert len(jason.comics) == 20
    val5 = jason.comics[7]
    assert val5.id == 93341
    assert val5.series.id == 31903
    assert val5.series.name == "The Mighty Valkyries (2021)"
    assert val5.series.resource_uri == "http://gateway.marvel.com/v1/public/series/31903"
    assert val5.title == "The Mighty Valkyries (2021) #5"
    assert val5.issue_number == 5
    assert val5.page_count == 32
    assert val5.upc == "75960620098600511"
    assert val5.diamond_code == "JUN210717"
    assert val5.format == "Comic"
    assert len(val5.characters) == 2
    assert len(val5.creators) == 5
    assert len(val5.events) == 0
    assert len(val5.stories) == 2
    assert val5.prices.digital is None
    assert val5.prices.print == Decimal("3.99")
    assert val5.dates.on_sale == date(2021, 9, 15)
    assert val5.dates.foc == date(2021, 8, 23)


def test_creator_events(talker):
    jason = talker.creator_events(11463)
    assert len(jason.events) == 10
    s = jason.events[5]
    assert s.id == 309
    assert s.title == "Shattered Heroes"
    assert s.thumbnail == "http://i.annihil.us/u/prod/marvel/i/mg/2/a0/511e8000770cd.jpg"
    assert s.resource_uri == "http://gateway.marvel.com/v1/public/events/309"
    assert len(s.characters) == 20
    assert len(s.comics) == 20
    assert len(s.creators) == 20
    assert len(s.series) == 10
    assert len(s.stories) == 20
    assert s.start == date(2011, 10, 19)
    assert s.end == date(2012, 4, 22)
