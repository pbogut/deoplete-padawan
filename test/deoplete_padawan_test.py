import unittest
from unittest.mock import Mock
import sys

sys.path.insert(0, './rplugin/python3/deoplete')
sys.modules['sources.base'] = __import__('mock_base')

from sources import deoplete_padawan  # noqa


class SourceTest(unittest.TestCase):

    def setUp(self):
        self.source = deoplete_padawan.Source(Mock())

    # get_complete_position returns column number
    # for deoplete. Its starting from 0

    def test_get_complete_position_for_method_call(self):
        position = self.source.get_complete_position(
            {'input': '  $this->getSome'})
        # deoplete    '0....5...^ <- 9
        self.assertEqual(position, 9)

    def test_get_complete_position_for_variable(self):
        position = self.source.get_complete_position(
            {'input': '  $var'})
        # deoplete    '0..^ <- 3
        self.assertEqual(position, 3)

    def test_get_complete_position_for_method_param(self):
        position = self.source.get_complete_position(
            {'input': 'callWithParams("Hell'})
        # deoplete    '0....5....0....^ <- 15
        self.assertEqual(position, 15)

    def test_get_complete_position_for_method_param_func(self):
        position = self.source.get_complete_position(
            {'input': 'callWithParams(array_'})
        # deoplete    '0....5....0....5....0^ <- 21
        self.assertEqual(position, 21)

    def test_get_complete_position_for_method_variable_param(self):
        position = self.source.get_complete_position(
            {'input': '          set($var'})
        # deoplete    '0....5....0....^ <- 15
        self.assertEqual(position, 15)

    def test_get_complete_position_for_method_static_call_param(self):
        position = self.source.get_complete_position(
            {'input': '   call(self::getVa'})
        # deoplete    '0....5....0...^ <- 14
        self.assertEqual(position, 14)

    def test_get_complete_position_for_static_method_call(self):
        position = self.source.get_complete_position(
            {'input': '     Class::getInst'})
        # deoplete    '0....5....0.^ <- 12
        self.assertEqual(position, 12)

    def test_get_complete_position_for_static_method_call_w_namespace(self):
        position = self.source.get_complete_position(
            {'input': '     \Some\Class::getInst'})
        # deoplete    '0....5....0....5..^ <- 18
        self.assertEqual(position, 18)

    def test_get_complete_position_for_class_search_w_namespace(self):
        position = self.source.get_complete_position(
            {'input': '     \Some\Class'})
        # deoplete    '0....5....0^ <- 11
        self.assertEqual(position, 11)

    def test_get_complete_position_for_class_search(self):
        position = self.source.get_complete_position(
            {'input': '     Class'})
        # deoplete    '0....5....^ <- 10
        self.assertEqual(position, 10)

    def test_get_complete_position_for_fluent_method_calls(self):
        position = self.source.get_complete_position(
            {'input': '$db->select("*")->from("table")->whe'})
        # deoplete    '0....5....0....5....0....5....0..^ <- 33
        self.assertEqual(position, 33)

    def test_get_complete_position_for_fluent_method_calls_2(self):
        position = self.source.get_complete_position(
            {'input': "$comment->getVar('dd')->"})
        # deoplete    '0....5....0....5....0...^ <- 24
        self.assertEqual(position, 24)

    def test_get_complete_position_for_use_statement(self):
        position = self.source.get_complete_position(
            {'input': '  use Class\\'})
        # deoplete    '0....5....0.^ <- 12
        self.assertEqual(position, 12)

    def test_get_complete_position_for_long_use_statement(self):
        position = self.source.get_complete_position(
            {'input': '   use Class\With\Lon'})
        # deoplete    '0....5....0....5..^ <- 18
        self.assertEqual(position, 18)

    def test_get_complete_position_for_new_statement(self):
        position = self.source.get_complete_position(
            {'input': ' $ala = new Class\\'})
        # deoplete    '0....5....0....5..^ <- 18
        self.assertEqual(position, 18)

    def test_get_complete_position_for_long_new_statement(self):
        position = self.source.get_complete_position(
            {'input': ' $x = new Class\With\Ver'})
        # deoplete    '0....5....0....5....0^ <- 21
        self.assertEqual(position, 21)

    def test_get_complete_position_for_new_with_root_namespace(self):
        position = self.source.get_complete_position(
            {'input': '      new \Date'})
        # deoplete    '0....5....0^ <- 11
        self.assertEqual(position, 11)

    def test_get_complete_for_built_in_functions(self):
        position = self.source.get_complete_position(
            {'input': '  array_something'})
        # deoplete    '0....5....0....5.^ <- 17
        self.assertEqual(position, 17)

    def test_get_complete_for_built_in_functions_on_assigment(self):
        position = self.source.get_complete_position(
            {'input': ' $a=array_'})
        # deoplete    '0....5....^ <- 10
        self.assertEqual(position, 10)

    def test_get_complete_for_built_in_functions_when_at_beginning(self):
        position = self.source.get_complete_position(
            {'input': 'array_something'})
        # deoplete    '0....5....0....^ <- 15
        self.assertEqual(position, 15)

    # get_padawan_column returns column number
    # for padawan.php. Its starting from 1

    def test_get_padawan_column_for_method_call(self):
        column = self.source.get_padawan_column(
            {'input': '  $this->getSome', 'complete_position': 9})
        # deoplete    '0....5...^ <- 9
        # padawan     '1...5....^ <- 10
        self.assertEqual(column, 10)

    def test_get_padawan_column_for_variable(self):
        column = self.source.get_padawan_column(
            {'input': '  $var', 'complete_position': 3})
        # deoplete    '0..^ <- 3
        # padawan     '1..^ <- 4
        self.assertEqual(column, 4)

    def test_get_padawan_column_for_method_param(self):
        column = self.source.get_padawan_column(
            {'input': 'callWithParams("Hell', 'complete_position': 15})
        # deoplete    '0....5....0....^ <- 15
        # padawan     '1...5....0....5^ <- 16
        self.assertEqual(column, 16)

    def test_get_padawan_column_for_method_param_func(self):
        column = self.source.get_padawan_column(
            {'input': 'callWithParams(array_'})
        # deoplete    '0....5....0....5....0^ <- 21
        # padawan     '1...5....0....5....0.^ <- 12
        self.assertEqual(column, 22)

    def test_get_padawan_column_for_method_variable_param(self):
        column = self.source.get_padawan_column(
            {'input': '          set($var', 'complete_position': 15})
        # deoplete    '0....5....0....^ <- 15
        # padawan     '1...5....0....5^ <- 16
        self.assertEqual(column, 16)

    def test_get_padawan_column_for_method_static_call_param(self):
        column = self.source.get_padawan_column(
            {'input': '   call(self::getVa', 'complete_position': 14})
        # deoplete    '0....5....0...^ <- 14
        # padawan     '1...5....0....^ <- 15
        self.assertEqual(column, 15)

    def test_get_padawan_column_for_static_method_call(self):
        column = self.source.get_padawan_column(
            {'input': '     Class::getInst', 'complete_position': 12})
        # deoplete    '0....5....0.^ <- 12
        # padawan     '1...5....0..^ <- 13
        self.assertEqual(column, 13)

    def test_get_padawan_column_for_static_method_call_w_namespace(self):
        column = self.source.get_padawan_column(
            {'input': '     \Some\Class::getInst', 'complete_position': 18})
        # deoplete    '0....5....0....5..^ <- 18
        # padawan     '1...5....0....5...^ <- 19
        self.assertEqual(column, 19)

    def test_get_padawan_column_for_class_search_w_namespace(self):
        column = self.source.get_padawan_column(
            {'input': '     \Some\Class', 'complete_position': 16})
        # deoplete    '0....5....0^ <- 11
        # padawan     '1...5....0.^ <- 12
        self.assertEqual(column, 12)

    def test_get_padawan_column_for_class_search(self):
        column = self.source.get_padawan_column(
            {'input': '     Class', 'complete_position': 11})
        # deoplete    '0....5....^ <- 10
        # padawan     '1...5....0^ <- 11
        self.assertEqual(column, 11)

    def test_get_padawan_column_for_fluent_method_calls(self):
        column = self.source.get_padawan_column(
            {'input': '$db->select("*")->from("table")->whe',
             'complete_position': 33})
        # deoplete    '0....5....0....5....0....5....0..^ <- 33
        # padawan     '1...5....0....5....0....5....0...^ <- 34
        self.assertEqual(column, 34)

    def test_get_padawan_column_for_use_statement(self):
        column = self.source.get_padawan_column(
            {'input': '  use Class\\', 'complete_position': 6})
        # deoplete    '0....5....0.^ <- 12
        # padawan     '1...5....0..^ <- 13
        self.assertEqual(column, 13)

    def test_get_padawan_column_for_long_use_statement(self):
        column = self.source.get_padawan_column(
            {'input': '   use Class\With\Lon', 'complete_position': 7})
        # deoplete    '0....5....0....5..^ <- 18
        # padawan     '1...5....0....5...^ <- 19
        self.assertEqual(column, 19)

    def test_get_padawan_column_for_new_statement(self):
        column = self.source.get_padawan_column(
            {'input': ' $ala = new Class\\', 'complete_position': 12})
        # deoplete    '0....5....0....5..^ <- 18
        # padawan     '1...5....0....5...^ <- 19
        self.assertEqual(column, 19)

    def test_get_padawan_column_for_long_new_statement(self):
        column = self.source.get_padawan_column(
            {'input': ' $x = new Class\With\Ver', 'complete_position': 10})
        # deoplete    '0....5....0....5....0^ <- 21
        # padawan     '1...5....0....5....0.^ <- 22
        self.assertEqual(column, 22)

    def test_get_padawan_column_for_new_with_root_namespace(self):
        column = self.source.get_padawan_column(
            {'input': '      new \Date', 'complete_position': 11})
        # deoplete    '0....5....0^ <- 11
        # padawan      1...5....0.^ <- 12
        self.assertEqual(column, 12)

    def test_get_padawan_col_for_built_in_functions(self):
        column = self.source.get_padawan_column(
            {'input': '  array_something', 'complete_position': 2})
        # deoplete    '0....5....0....5.^ <- 17
        # padawan      1...5....0....5..^ <- 18
        self.assertEqual(column, 18)

    def test_get_padawan_col_for_built_in_functions_on_assigment(self):
        column = self.source.get_padawan_column(
            {'input': ' $a=array_', 'complete_position': 4})
        # deoplete     0....5....^ <- 10
        # padawan      1...5....0^ <- 11
        self.assertEqual(column, 11)

    def test_get_padawan_col_for_built_in_functions_when_at_beginning(self):
        column = self.source.get_padawan_column(
            {'input': 'array_something', 'complete_position': 0})
        # deoplete    '0....5....0....^ <- 15
        # padawan      1...5....0....5^ <- 16
        self.assertEqual(column, 16)
