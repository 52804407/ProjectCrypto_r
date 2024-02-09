import click
import re
from datetime import datetime, timedelta

#Validation function for start_date
def validate_start_date(ctx, param, value):
    # Regular expression to match the format and extract parts
    match = re.match(r"(\d+)([DWMY])$", value.upper())
    if not match:
        raise click.BadParameter("Start date must be in the format of <number><D/W/M/Y> (e.g., 31D, 12W, 6M, 1Y)")
    
    number, unit = int(match.group(1)), match.group(2)
    # Validate the number based on the unit
    if unit == "D" and not (1 <= number <= 365):
        raise click.BadParameter("Days must be between 1 and 365")
    elif unit == "W" and not (1 <= number <= 52):
        raise click.BadParameter("Weeks must be between 1 and 52")
    elif unit == "M" and not (1 <= number <= 12):
        raise click.BadParameter("Months must be between 1 and 12")
    elif unit == "Y" and not (1 <= number <= 3):
        raise click.BadParameter("Years must be between 1 and 5")
    
    return value.upper()

#Function to extract start date from period
def get_start_date_from_period(period):
    unit = period[-1]
    quantity = int(period[:-1])
    if unit == "D":
        return datetime.now() - timedelta(days=quantity)
    elif unit == "W":
        return datetime.now() - timedelta(weeks=quantity)
    elif unit == "M":
        return datetime.now() - timedelta(days=30*quantity)
    elif unit == "Y":
        return datetime.now() - timedelta(days=365*quantity)
