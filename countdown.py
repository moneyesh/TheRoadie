import datetime

trip_countdown = datetime.date(trip.leave_date) - datetime.date.today()
return(f"Your trip to {trip.to_dest} is in: {trip} days")
