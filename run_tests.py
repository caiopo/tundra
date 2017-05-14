import unittest

loader = unittest.TestLoader()
tests = loader.discover('test')

testRunner = unittest.runner.TextTestRunner()
result = testRunner.run(tests)

exit(not result.wasSuccessful())
