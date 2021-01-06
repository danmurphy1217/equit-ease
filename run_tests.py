from tests import reader_only_equity
import unittest
from types import ModuleType

def instantiate_test(module_name: ModuleType) -> None:
    """load tests from the passed module"""
    MODULE = unittest.TestLoader().loadTestsFromModule(module_name)
    unittest.TextTestRunner().run(MODULE)

instantiate_test(reader_only_equity)