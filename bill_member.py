""" Calculates bill and usage and prints it."""

from calendar import monthrange
from datetime import datetime, timedelta

import load_readings
from tariff import BULB_TARIFF


def _get_days_in_month(bill_date):
    """Get days in month

    Process the bill_date (string ISO formatted) to get number of days in
    a calender month.
    :param str bill_date: ISO standard formatted date for UTC timezone.
    :returns number of days in month
    :rtype: int
    """
    datetime_object = datetime.strptime(bill_date, '%Y-%m-%d')
    _, days = monthrange(datetime_object.year, datetime_object.month)
    return days


def calculate_usage(account_data, bill_date, energy_type):
    """Calculates usage of account

    The usage is estimated based on previous meter readings of
    billing month. Assuming bill_date is always end of the month.
    :param dict account_data: reading data of account
    :param str bill_date: ISO date for bill generation
    :param str energy_type: 'gas' or 'electricity'
    :return: energy usage for `bill_date`
    :rtype: int
    :raises TypeError: if the user has no previous readings
    :raises ValueError: on no Previous reading of current month.
    """
    # assuming there will one item in the list for account data
    meter_data = account_data[0][energy_type]
    previous_month_reading = None
    usage_per_day = None

    bill_datetime = datetime.strptime(bill_date, '%Y-%m-%d')
    bill_month_days = _get_days_in_month(bill_date)

    # Finding nearest previous two meter reading for estimation
    for reading in meter_data:
        reading_datetime = reading['readingDate']
        # Sometimes json might return datetime object
        if isinstance(reading_datetime, str):
            reading_datetime = \
                datetime.strptime(
                    reading['readingDate'], '%Y-%m-%dT00:00:00.000Z')
        # Checking if reading month previous month of bill date
        if reading_datetime.month == \
                (bill_datetime.replace(day=1) - timedelta(days=1)).month:
            # previous month reading
            # datetime object is more useful than string
            reading['readingDate'] = reading_datetime
            previous_month_reading = reading

        elif reading_datetime.month == bill_datetime.month:
            # from assumption and linear list previous_month_reading
            # already loaded
            # pylint disable=unsubscriptable-object
            if previous_month_reading is None:
                raise ValueError("No previous reading")
            units_used = \
                reading['cumulative'] - previous_month_reading['cumulative']
            reading_window_days = \
                (reading_datetime - previous_month_reading['readingDate']).days
            usage_per_day = units_used / reading_window_days
            break

    # rounding off to zero decimal
    return int(usage_per_day * bill_month_days)


def calculate_tariff_bill(usage_units, energy_type, usage_days=30):
    """Calculates tariff for usage

    :param int usage_units: units of energy consumed
    :param str energy_type: 'gas' or 'electricity'
    :param int usage_days: days in a month to calculate standard rate.
    :return: bill for usage, in pounds (£)
    :rtype: float
    """
    unit_rate = BULB_TARIFF[energy_type]['unit_rate']
    standard_charges = BULB_TARIFF[energy_type]['standing_charge']

    bill_charged = usage_units * unit_rate
    bill_charged += standard_charges * usage_days
    bill_amount = bill_charged / 100
    return float(f'{bill_amount:.2f}')


def calculate_bill(member_id, account_id=None, bill_date=None):
    """Calculates energy bill for given bill_date

    :param str member_id: unique identity of customer/member to calculate bill
    :param str account_id: specific account id of customer, `ALL`/None will
    calculate bill for all the accounts of member
    :param str bill_date: date of which bill has be calculated
    :rtype tuple
    :returns bill amount (in pounds) and usage in kWh.

    :raises KeyError if not valid member_id or account_id
    """
    member_data = load_readings.get_readings()[member_id][0]
    electricity_usage = 0
    gas_usage = 0
    # calculating usage of electricity and gas
    if account_id == 'ALL' or account_id is None:
        # when no account id passed we calculate all accounts of member
        for _, account_data in member_data.items():
            electricity_usage += \
                calculate_usage(account_data, bill_date, 'electricity')
            # gas reading can be optional as many data doesn't have it.
            if 'gas' in account_data[0].keys():
                gas_usage += calculate_usage(account_data, bill_date, 'gas')

    else:
        electricity_usage = \
            calculate_usage(member_data[account_id], bill_date, 'electricity')
        # gas reading can be optional as many data doesn't have it.
        if 'gas' in member_data[account_id][0].keys():
            gas_usage = calculate_usage(
                member_data[account_id], bill_date, 'gas')

    days_in_month = _get_days_in_month(bill_date)

    # calculating electricity charges
    amount = calculate_tariff_bill(
        electricity_usage, 'electricity', days_in_month)
    if gas_usage:
        # calculating gas charges and added to electricity charges
        amount += calculate_tariff_bill(gas_usage, 'gas', days_in_month)
    # since we are not returning gas usage
    kwh = electricity_usage
    print(kwh, gas_usage, electricity_usage)
    return amount, kwh


def calculate_and_print_bill(member_id, account, bill_date):
    """Calculate the bill and then print it to screen.
    Account is an optional argument - I could bill for one account or many.
    There's no need to refactor this function."""
    member_id = member_id or 'member-123'
    bill_date = bill_date or '2017-08-31'
    account = account or 'ALL'
    amount, kwh = calculate_bill(member_id, account, bill_date)
    print('Hello {member}!'.format(member=member_id))
    print('Your bill for {account} on {date} is £{amount}'.format(
        account=account,
        date=bill_date,
        amount=amount))
    print('based on {kwh}kWh of usage in the last month'.format(kwh=kwh))
