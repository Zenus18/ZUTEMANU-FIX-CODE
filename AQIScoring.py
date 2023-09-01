AQI_score = 0
hum_reference = 40
gas_reference = 25000

def humidity_score(humidity_value):
    if humidity_value >=38 and humidity_value <= 42:
        hum_score = 0.25 * 100
    else:
        if humidity_value < 38:
            hum_score = 0.25/hum_reference*humidity_value*100
        else:
            hum_score = ((-0.25/(100-hum_reference)*humidity_value)+0.416666)*100
    return hum_score

#calculate gas score 
gas_lower_limit = 5000  
gas_upper_limit = 50000 

def get_gas_reference(gas_resistance):
    global gas_reference
    readings = 10
    for i in range(1, readings):  # read gas for 10 x 0.150mS = 1.5secs
        gas_reference += gas_resistance
    gas_reference = gas_reference / readings
    #print("Gas Reference =", round(gas_reference, 3))
    return gas_reference

def get_gas_score():
    # Calculate gas contribution to IAQ index
    gas_score = (0.75 / (gas_upper_limit - gas_lower_limit) * gas_reference - (gas_lower_limit * (0.75 / (gas_upper_limit - gas_lower_limit)))) * 100.00
    if gas_score > 75:  # Sometimes gas readings can go outside of the expected scale maximum
        gas_score = 75
    if gas_score < 0:  # Sometimes gas readings can go outside of the expected scale minimum
        gas_score = 0

    return gas_score