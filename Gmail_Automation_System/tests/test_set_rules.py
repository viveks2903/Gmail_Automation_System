from unittest.mock import patch
from set_rules import create_rule

class TestSetRules:

  @patch('builtins.input')  # Mocking built-in input function
  def test_create_rule(self, mock_input):
      # Provide mock inputs to simulate user responses for rule creation
      mock_input.side_effect = [
          '1',                # for "Should all conditions match, or any one condition?" (choosing 'All')
          '1',                # for "Choose the field for condition" (choosing 'from')
          '1',                # for "Choose the operator" (choosing 'contains')
          'test@example.com', # for "Enter the value"
          '1',                # for "Do you want to add more conditions?" (choosing 'Yes')
          '1',                # for next condition "Choose the field for condition" (choosing 'from') 
          '2',                # for next condition "Choose the operator" (choosing 'does_not_equal')  
          'example.com',      # for next condition value
          '2',                # for ending input (choosing 'No')
          '1',                # for "Select the actions" (choosing 'mark_as_read')
          '0',                # for "Done selecting"
      ]

      # Call the create_rule function 
      create_rule()



