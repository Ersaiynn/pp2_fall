from datetime import datetime

dt = datetime.now()
dt_without_microseconds = dt.replace(microsecond=0)

print("with microseconds:", dt)
print("without microseconds:", dt_without_microseconds)