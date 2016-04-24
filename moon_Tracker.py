import ephem
import time
from datetime import datetime
import urllib2
import json
import numpy as np
from astral import Astral



astral = Astral()
date = datetime.utcnow()
data_final = []
fileWriteData = open('YOUR_HOME_PATH_HERE/moon_data_JSON.json','w+')
moon_phases = ["New Moon","First Quarter","Full Moon","Long Quarter"]

def moon_phase_data():
    moon_phase = astral.moon_phase(date)
    print "Moon phase raw: " + str(moon_phase)
    if(moon_phase > 0 and moon_phase < 7):
        return moon_phases[0]
    elif(moon_phase >= 7 and moon_phase < 14):
        return moon_phases[1]
    elif(moon_phase >= 14 and moon_phase < 21):
        return moon_phases[2]
    elif(moon_phase >= 21):
        return moon_phases[3]
    else:
        print "Out of range"
def takeData():
    try:
        response_client = json.loads(urllib2.urlopen('http://ip-api.com/json').read())
        cityCli = response_client['city']
        cityLatitude = response_client['lat']
        cityLongitude = response_client['lon']
        print "#####IP tracking#####"
        print ""
        print "City client: "+str(cityCli)
        print "City latitude: "+str(cityLatitude)
        print "City longitude: "+str(cityLongitude)
        return cityCli, cityLatitude, cityLongitude
    except urllib2.HTTPError, e:
        checksLogger.error('HTTPError = ' + str(e.code))
    except urllib2.URLError, e:
        checksLogger.error('URLError = ' + str(e.reason))
    except httplib.HTTPException, e:
        checksLogger.error('HTTPException')

cityCli, cityLat, cityLon = takeData()
print ""
print "#####SKY DATA#####"
print ""
moon_phase_data = moon_phase_data()

print "Moon_phase: " + moon_phase_data

print "RAW DATA"
print "Date: " + str(date)
print ""

obs = ephem.Observer()
obs.lat = np.deg2rad(cityLat)
obs.lon = np.deg2rad(cityLon)
obs.date = date

moon = ephem.Moon()
sun = ephem.Sun()

sun.compute(obs)
moon.compute(obs)

print "Sun"
azRad, altRad = map(np.rad2deg, (sun.az, sun.alt))
print "Altitude raw: " + str(sun.alt) +" "+ "Azimuth raw: "+ str(sun.az)
print "Altitude rad: " + str(altRad) +" "+ "Azimuth rad: "+ str(azRad)

print "Moon"
azRad, altRad = map(np.rad2deg, (moon.az, moon.alt))
print "Altitude raw: " + str(moon.alt) +" "+ "Azimuth raw: "+ str(moon.az)
print "Altitude rad: " + str(altRad) +" "+ "Azimuth rad: "+ str(azRad)

#JSON STUFF
data_final.append({'phase': moon_phase_data, 'altitude' : altRad, 'azimuth' : azRad})
final_data_json = json.dumps(data_final)
fileWriteData.write(final_data_json)
fileWriteData.close()
print ("          ")
print final_data_json
