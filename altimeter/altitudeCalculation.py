def altitudeCalc(pressure):
	height = 44330.77*(1-pow(pressure/101325.00, 0.1902632))	
	return height	