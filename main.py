fakeXacc = [0.1, 0.2, 0.3, 0.4, 0.5]
fakeYacc = [0.05, 0.1, 0.15, 0.2, 0.25]
fakeZacc = [1, 2, 3, 4, 5]
fakeTime = [0.1, 0.2, 0.3, 0.4, 0.5]

for i in range(0, 5):
    vx = 
= (fakeY[i+1]-fakeY[i])/(fakeTime[i+1]-fakeTime[i])
    vz = (fakeZ[i+1]-fakeZ[i])/(fakeTime[i+1]-fakeTime[i])
    
    print (vx, vy, vz)

