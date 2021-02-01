from tests import (
    test_parser,
    test_reader,
    test_quote_parser,
    test_chart_parser,
    test_user_config_parser,
    test_quote_displayer,
    test_displayer
)
import unittest
from types import ModuleType

def instantiate_test(module_name: ModuleType) -> None:
    """load tests from the passed module"""
    MODULE = unittest.TestLoader().loadTestsFromModule(module_name)
    unittest.TextTestRunner().run(MODULE)

instantiate_test(test_reader)
instantiate_test(test_parser)
instantiate_test(test_quote_parser)
instantiate_test(test_chart_parser)
instantiate_test(test_user_config_parser)
instantiate_test(test_quote_displayer)
instantiate_test(test_displayer)