import pytest

from service_api.middleware import domain_match


class TestDomainMatch:

    @pytest.mark.parametrize(
        'sub_domain, origin, actual_match', [
            ('http://google.com', 'google.com', True),
            ('google.com', 'google.com', True),
            ('http://d1.google.com.d2', 'google.com', True),
            ('http://d1.google.com?', 'google.com', True),
            ('d1.google.com/', 'google.com', True),
            ('http://ddgoogle.com', 'google.com', False),
            ('http://google.com#', 'google.com', False),
        ]
    )
    def test_domain_match(self, sub_domain, origin, actual_match):
        result_match = domain_match(origin, sub_domain)
        assert bool(result_match) == actual_match
