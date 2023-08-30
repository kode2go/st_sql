import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Get the option from the user
default_option = input("Do you want to use the last 6 months as default? (yes/no): ").lower()

if default_option == "yes":
    # Use the last 6 months as default
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=6*30)
else:
    # Get input for start date
    start_date_str = input("Enter the start date (YYYY-MM-DD): ")
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()

    # Get input for end date
    end_date_str = input("Enter the end date (YYYY-MM-DD): ")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

daterange = pd.date_range(start_date, end_date)
form = [single_day.strftime("%Y%m%d") for single_day in daterange]

# Write out the dates to a file called dates
with open("dates", "w") as fdate:
    for day in form:
        fdate.write(str(day) + "\n")

print("Dates have been written to the 'dates' file.")
