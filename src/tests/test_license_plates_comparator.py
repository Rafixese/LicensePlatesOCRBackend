from unittest import TestCase
from src.utils.license_plates_comparator import LicensePlatesComparator


class Test(TestCase):
    def test_generate_similar_license_plates_strings(self):
        comparator = LicensePlatesComparator()
        license_plate = "TOS 49270"
        expected_result = ["TOS 4927O", "TOS 4927Q", "TOS 49270",
                           "T0S 4927O", "T0S 4927Q", "T0S 49270",
                           "TQS 4927O", "TQS 4927Q", "TQS 49270"]
        result = comparator.generate_similar_license_plates_strings(license_plate)
        self.assertEqual(sorted(expected_result), sorted(result))

    def test_compare_license_plates_string(self):
        comparator = LicensePlatesComparator()
        self.assertFalse(comparator.compare_license_plates_strings("TOS 55555", "TOS 21212"))
        self.assertTrue(comparator.compare_license_plates_strings("LU 21370", "LU 2137O"))
