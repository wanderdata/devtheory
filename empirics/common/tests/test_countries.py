from empirics.common import countries as cc


def test_membership():
    assert len(cc.LAC33) == 33
    assert len(cc.CARIBBEAN16) == 16
    assert set(cc.CARIBBEAN16) <= set(cc.LAC33)
    assert len(cc.LATIN_AMERICA_REST) == 17


def test_codes_unique_and_complete():
    assert len(set(cc.M49.values())) == 33
    for iso in cc.LAC33:
        assert cc.OFFICIAL[iso] and cc.SHORT[iso]


def test_pool_exclusions_are_members():
    assert set(cc.POOL_EXCLUDE_LAC) <= set(cc.LAC33)
