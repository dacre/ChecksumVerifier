import unittest
import cv


class TestHashMethods(unittest.TestCase):

    def setUp(self):
        pass

    def test_sha256(self):
        result = cv.check_file("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "test_file")
        self.assertEqual("sha256", result)

    def test_md5(self):
        result = cv.check_file("d41d8cd98f00b204e9800998ecf8427e", "test_file")
        self.assertEqual("md5", result)

    def test_folder_search(self):
        result = cv.check_files("d41d8cd98f00b204e9800998ecf8427e", True)
        self.assertEqual("md5", result[0])

    def test_large_folder(self):
        from os import chdir, getcwd
        current_directory = getcwd()
        chdir("./large_directory/")
        result = cv.check_files("596c5b567ddb90bfe8110c71d6a5f564b921583098367a4f87e8c4c9cd8335a2", True)
        self.assertEqual("sha256", result[0])
        chdir(current_directory)

if __name__ == '__main__':
    unittest.main()
