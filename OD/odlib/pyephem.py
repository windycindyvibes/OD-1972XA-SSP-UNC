import ephem

obs = ephem.Observer()
obs.lon = "-81:24:52.9" #longitude of obs.
obs.lat = "36:15:09.7" #lat of obs.
obs.elev = 922. #elevation of obs, in meters (not a string!)
obs.date = "2020/07/05 07:08:00" #(UTC date/time of observation)
line = "2003GE42,e,27.8543085,165.6469288,101.353156,2.63408,,0.375418379,8.4377868,07/05.29722/2020,2000,,"
asteroid = ephem.readdb(line)
asteroid.compute(obs)
#print(asteroid.a_ra, asteroid.a_dec)
