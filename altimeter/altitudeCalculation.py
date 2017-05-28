def altitudeCalc(pressure, temperature):
	height = 44330.77*(1-pow(pascals/101325.00, 0.1902632))	
	return height	
