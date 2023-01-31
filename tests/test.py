import pytest
from app.calc import Calculator

class TestCalc:
 def setup(self):
    self.calc = Calculator
 def test_adding_success(self):
     assert self.calc.adding(self, 1 , 1)  == 2

 def test_adding_unsuccess(self):
     assert self.calc.adding(self, 1 , 1) == 3

 def test_zero_devision(self):
     with pytest.raises(ZeroDivisionError):
         self.calc.division(self, 1 , 0)

 def multiply_test(self):
     assert self.calc.multiply(self, 1, 2 ) == 2

 def subtraction_test(self):
     assert  self.calc.subtraction(self, 4, 2 ) == 1

 def vstepen_test(self):
     assert self.calc.vstepen(self, 2 , 2) == 4




 def teardown(self):
     print('Выполнение метода teardown')