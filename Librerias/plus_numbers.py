import machine


def time_seconds(ds):
	day_seconds = int(ds.Day())*86400
	hour_seconds = int(ds.Hour())*3600
	minute_seconds = int(ds.Minute())*60
	seconds = int(ds.Second())
	seconds_total = day_seconds + hour_seconds + minute_seconds + seconds
	return seconds_total
