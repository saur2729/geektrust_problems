import os
import argparse

class Traffic:
  def __init__(self, test_file):
    self.test_file = test_file
    # constant factors
    self.orbit_data = {
      "ORBIT1": [18, 20], # orbitTag : [megamile, no of craters to cross]
      "ORBIT2": [20, 10]
    }
    self.vehicle_data = {
      "BIKE": [10, 2, 3], # [speed in megamiles/hour, time taken in mins to cross 1 crater, (priority 3 > 2 > 1) ]
      "TUKTUK": [12, 1, 2], # 12 mm/hour & takes 1 min to cross 1 crater, priority
      "CAR": [20, 3, 1]
    }
    self.weather_data = {
      "SUNNY" : [-10, ["BIKE", "CAR", "TUKTUK"]], # [craters reduce by 10%. Car, bike and tuktuk can be used in this weather.]
      "RAINY" : [20, ["CAR", "TUKTUK"]],# craters increase by 20%. Car and tuktuk can be used in this weather.
      "WINDY" : [0, ["BIKE", "CAR"]]
    }

  def find_priority(self, vech1, vech2):
    # returns True is first vehicle priority is greater than second else false
    return True if self.vehicle_data[vech1][2] > self.vehicle_data[vech2][2] else False

  def find_time(self, weather, orbit, orb_maxspd, vech):
    # orbit_len / vehcle_max_speed + (orbit_craters + (orbit_craters * weather[0])) * vehicle[1]
    normal_orbit_time = (self.orbit_data[orbit][0] / orb_maxspd) * 60 # convert to mins
    total_crater = self.orbit_data[orbit][1] + (self.orbit_data[orbit][1] * (self.weather_data[weather][0]/100))
    crater_time = total_crater * self.vehicle_data[vech][1]
    total_time = normal_orbit_time + crater_time
    return [total_time, vech, orbit]

  def get_fastest(self, weather, orb1_trfc_spd, orb2_trfc_spd):
    min_time = []
    for orbit in self.orbit_data:
      for vech in self.weather_data[weather][1]:
        # check the max speed of vehicle here
        if orbit == "ORBIT1":
          orb_maxspd = orb1_trfc_spd if orb1_trfc_spd < self.vehicle_data[vech][0] else self.vehicle_data[vech][0]
        elif orbit == "ORBIT2":
          orb_maxspd = orb2_trfc_spd if orb2_trfc_spd < self.vehicle_data[vech][0] else self.vehicle_data[vech][0]

        time_stats = self.find_time(weather, orbit, orb_maxspd, vech)

        # print(" -- ", time_stats)
        if not min_time:
          min_time = time_stats
        elif time_stats[0] < min_time[0]:
          min_time = time_stats
        elif time_stats[0] == min_time[0]:
          min_time = time_stats if self.find_priority(time_stats[1], min_time[1]) else min_time
    return min_time

  def fastest_path(self):
    with open(self.test_file) as fp:
      for line in fp.readlines():
        if line.strip().startswith("#") or not line.strip(): # ignore the comments and empty lines
          continue
        try:
          weather, orb1_trfc_spd, orb2_trfc_spd = line.strip().split()
        except ValueError:
          continue # continue if number of input params != 3

        # print(line.strip(), self.get_fastest(weather, float(orb1_trfc_spd), float(orb2_trfc_spd)))

        fastest_way = self.get_fastest(weather, float(orb1_trfc_spd), float(orb2_trfc_spd))
        print(" ".join(fastest_way[1:]))


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("test_file")
  args = parser.parse_args()

  # Check if input file exists and size is not zero
  assert os.path.exists(args.test_file), "Missing input file"
  assert os.stat(args.test_file).st_size > 0, "Input File is empty"

  traffic_sol = Traffic(args.test_file)
  traffic_sol.fastest_path()

