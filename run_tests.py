from tests import test_parser, test_reader
import unittest
from types import ModuleType

def instantiate_test(module_name: ModuleType) -> None:
    """load tests from the passed module"""
    MODULE = unittest.TestLoader().loadTestsFromModule(module_name)
    unittest.TextTestRunner().run(MODULE)

instantiate_test(test_reader)
instantiate_test(test_parser)