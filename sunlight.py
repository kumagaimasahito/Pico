import math
import datetime

class Sunlight(object):
    def __init__(self, julian_date, longitude, latitude):
        self.julian_date = julian_date
        self.longitude = longitude
        self.latitude = latitude
    
    def calc_current_julian_day(self):
        self.n = self.julian_date - 2451545.0 + 0.0008
        return self.n

    def calc_mean_solar_time(self):
        self.mean_solar_time = self.n - self.longitude/360
        return self.mean_solar_time
    
    def calc_solar_mean_anomaly(self):
        self.solar_mean_anomaly = (357.5291 + 0.98560028*self.mean_solar_time)%360
        return self.solar_mean_anomaly

    def calc_equation_of_the_center(self):
        self.equation_of_the_center = 1.9148*math.sin(math.radians(self.solar_mean_anomaly)) \
                                    + 0.0200*math.sin(math.radians(2*self.solar_mean_anomaly)) \
                                    + 0.0003*math.sin(math.radians(3*self.solar_mean_anomaly))
        return self.equation_of_the_center

    def calc_ecliptic_longitude(self):
        self.ecliptic_longitude = (self.solar_mean_anomaly + self.equation_of_the_center + 180 + 102.9372)%360
        return self.ecliptic_longitude

    def calc_solar_transit(self):
        self.solar_transit = 2451545.0 + self.mean_solar_time \
                           + 0.0053*math.sin(math.radians(self.solar_mean_anomaly)) \
                           - 0.0069*math.sin(math.radians(2*self.ecliptic_longitude))
        return self.solar_transit

    def calc_declination_of_the_sun(self):
        sin_declination_of_the_sun = math.sin(math.radians(self.ecliptic_longitude))*math.sin(math.radians(23.44))
        self.declination_of_the_sun = math.degrees(math.asin(sin_declination_of_the_sun))
        return self.declination_of_the_sun

    def calc_hour_angle(self):
        numerator = math.sin(math.radians(-0.83)) \
                    - math.sin(math.radians(self.latitude))*math.sin(math.radians(self.declination_of_the_sun))
        denominator = math.cos(math.radians(self.latitude))*math.cos(math.radians(self.declination_of_the_sun))
        cos_hour_angle = numerator/denominator
        self.hour_angle = math.degrees(math.acos(cos_hour_angle))
        return self.hour_angle

    def calc_sunrise(self):
        self.julian_date_of_sunrise = self.solar_transit - self.hour_angle/360
        return self.julian_date_of_sunrise

    def calc_sunset(self):
        self.julian_date_of_sunset = self.solar_transit + self.hour_angle/360
        return self.julian_date_of_sunset

    def run(self):
        self.calc_current_julian_day()
        self.calc_mean_solar_time()
        self.calc_solar_mean_anomaly()
        self.calc_equation_of_the_center()
        self.calc_ecliptic_longitude()
        self.calc_solar_transit()
        self.calc_declination_of_the_sun()
        self.calc_hour_angle()
        self.calc_sunrise()
        self.calc_sunset()
        return self.julian_date_of_sunrise, self.julian_date_of_sunset

class Time(object):
    def __init__(self):
        self.update()
    
    def update(self):
        self.date = datetime.datetime.now(datetime.timezone.utc)
        self.year = self.date.year
        self.month = self.date.month
        self.day = self.date.day
        self.hour = self.date.hour
        self.minute = self.date.minute
        self.second = self.date.second
        self.fix_year_and_month()

    def fix_year_and_month(self):
        if self.month == 1 or self.month == 2:
            self.month += 12
            self.year -= 1

    def julian(self):
        self.julian_date = int(365.25*self.year) \
                         + int(self.year/400) \
                         - int(self.year/100) \
                         + int(30.59*(self.month-2)) \
                         + self.day \
                         + 1721088.5 \
                         + self.hour/24 \
                         + self.minute/1440 \
                         + self.second/86400
        return self.julian_date

def main():
    julian_date = Time().julian()
    print(julian_date)

    sunlight = Sunlight(julian_date, 135, 34.39)
    sunlight.run()
    print(sunlight.julian_date_of_sunrise)
    print(sunlight.julian_date_of_sunset)

if __name__ == "__main__":
    main()