import pytest
from src.engine.calculator import CarbonCalculator

def test_calculation_logic():
    calc = CarbonCalculator()
    
    # Test Electricity calculation
    # Factor for 'Electricity - Grid' is 0.37 kg/kWh
    # Quantity: 1000 kWh
    # Expected: (1000 * 0.37) / 1000 = 0.37 tCO2e
    scope, t_co2e = calc.calculate_emissions('Electricity - Grid', 1000)
    assert scope == 2
    assert t_co2e == 0.37

def test_invalid_activity():
    calc = CarbonCalculator()
    scope, t_co2e = calc.calculate_emissions('Unknown Activity', 100)
    assert scope == 0
    assert t_co2e == 0
