from main import mac_return_valid
from main import mac_from_file
import unittest

valid_macs = ['3D:F2:C9:A6:B3:4F',
              '4D:F5:C6:A8:B1:43',
              '06-00-00-00-00-00',
              '00-B0-D0-63-C2-26',
              '05-00-9b-00-00-10']

invalid_macs = ['3D:F2:C9:A6:B3-4F',
                'AAAAAAAAAAAAAAAAA',
                '06-00-00-a0-00-b_',
                '',
                '123456677788']


class TestMACs(unittest.TestCase):
    def test_valid(self):
        for i in valid_macs:
            self.assertTrue(mac_return_valid(i))

    def test_invalid(self):
        for i in invalid_macs:
            self.assertFalse(mac_return_valid(i))

    def test_valid_file(self):
        self.assertEqual(mac_from_file('lab2/unit_macs.txt'), valid_macs)


if __name__ == '__main__':
    unittest.main()
