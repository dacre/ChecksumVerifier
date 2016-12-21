#!/usr/bin/python
# -*- coding: UTF-8 -*-

# This script checks if a file matches a checksum for md5 or sha256.
# It can also check current directory for any file matching the checksum
import sys
import hashlib


# compares checksum input to file checksum calculation. Checks both md5 and sha256
def check_file(checksum, filename):
    hash_to_check = hashlib.md5()
    if digest(filename, hash_to_check) == checksum:
        return "md5"
    hash_to_check = hashlib.sha256()
    if digest(filename, hash_to_check) == checksum:
        return "sha256"
    return


# Checks current directory for if any file matches the checksum
def check_files(checksum, test):
    from os import listdir
    from os.path import isfile, join, getmtime
    only_files = [f for f in listdir(".") if isfile(join(".", f))]
    only_files_in_order_of_last_modified = sorted(only_files, key=getmtime, reverse=True)
    print "Looking for file with checksum matching: " + checksum
    for idx, file_to_check in enumerate(only_files_in_order_of_last_modified):
        if idx > 0 and idx % 10 == 0 and not test:
            decision_taken = False
            while not decision_taken:
                user_input = raw_input("Checked 10 files, do you want to continue (Y/N)?")
                if user_input.lower() == "n" or user_input == "y":
                    decision_taken = True
                    if user_input == "n":
                        quit(-1)
        print "Analyzing file: " + file_to_check
        checksum_type = check_file(checksum, file_to_check)

        if checksum_type is not None:
            print "File checksum match was found for: " + file_to_check + " (" + checksum_type + ")"
            return checksum_type, checksum, file_to_check
    return


# Calculates the digest.
def digest(filename, hash_to_check):
    with open(filename, "rb") as f:
        # According to stackoverflow update is maxed out at 4096 bytes
        for chunk in iter(lambda: f.read(4096), b""):
            hash_to_check.update(chunk)
        return hash_to_check.hexdigest()


# checks if user input is 2 arguments (checksum and file) or 1 (checksum) and verifies the checksum accordingly
if __name__ == '__main__':
    if len(sys.argv) == 2:
        result = check_files(sys.argv[1], False)
        if result is None:
            print "NOT OK!"
        elif len(result) > 0:
            print "### OK ###"
    elif len(sys.argv) == 3:
        result = check_file(sys.argv[1], sys.argv[2])
        if result is None:
            print "NOT OK!"
        elif len(result) > 0:
            print "OK (" + result + ")"
    else:
        print "Wrong command line arguments supplied. Either supply a checksum or a checksum and a filename"
