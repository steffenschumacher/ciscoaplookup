from unittest import TestCase, main
from ciscoaplookup import *


class TestCiscoAPLookup(TestCase):
    def test_positive_models(self):
        cases = [
            ('AIR-CAP1532I', 'Belgium', '-E'),
            ('AIR-AP1562I', 'Gibraltar', '-E'),
            ('AIR-CAP1532I', 'Japan', '-Q'),
            ('AIR-AP1572IC', 'Mexico', '-A'),
            ('AIR-AP1572IC', 'New Zealand', '-Z'),
            ('AIR-CAP1532I', 'Taiwan', '-T'),
            ('AIR-AP2802I', 'Denmark', '-E'),
            ('AIR-AP2802I', 'Nicaragua', '-W'),  # used when no matches are made.
        ]
        for c in cases:
            res = get_models_for(c[0], c[1])
            exp = [c[0]+c[2]+'-K9']
            self.assertEqual(exp, res, '{} doesn\'t match {} for {} / {}'.format(res, exp, c[0], c[1]))

    def test_fail_models(self):
        self.assertRaises(ValueError, get_models_for, 'gnyf', 'Denmark')  # invalid model
        self.assertRaises(ValueError, get_models_for, 'AIR-CAP1532I', 'Neverland')  # invalid country
        self.assertRaises(ValueError, get_models_for, 'AIR-CAP1552H', 'Vietnam')  # not possible

    def test_hest(self):
        self.assertTrue(len(get_models()) > 20)

    def test_countries(self):
        import pycountry
        lawless_countries = []

        for c in pycountry.countries:
            try:
                klaf = get_models_for('AIR-AP2802I', c.name)
            except ValueError as ve:
                print(ve)


if __name__ == '__main__':
    main()
