import os
import unittest

import pm


def run_all_tests(test_dir: str, verbosity: int = 2):
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir)

    runner = unittest.TextTestRunner(verbosity=verbosity)
    runner.run(suite)


if __name__ == '__main__':
    cur_dir = pm.Settings.project_root_dir
    test_dir = os.path.join(cur_dir, "tests")
    print("Running all pm-prediction tests in {}".format(test_dir))
    run_all_tests(test_dir=test_dir, verbosity=2)
