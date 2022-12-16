import datetime


# Let's get all the days make one playlist per
def saturday():
    # Set the start and end dates for the range of years you want
    start_date = datetime.date(2012, 12, 15)
    end_date = datetime.date(2022, 12, 15)
    saturdays = []

    # Loop through each year in the range
    for year in range(start_date.year, end_date.year + 1):

        # Loop through each month in the year
        for month in range(1, 13):
            # Get the first Monday of the month
            first_saturday = datetime.date(year, month, 1)
            while first_saturday.weekday() != 5:
                first_saturday += datetime.timedelta(1)

            # Append the first Monday of the month
            saturdays.append(first_saturday.strftime('%Y-%m-%d'))

    return saturdays

# honestly why did i grab mondays thats such a weird day maybe i'll fix it later
