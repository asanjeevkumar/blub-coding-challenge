# Test the bill member calculate_bill

# pylint: disable=missing-docstring, E128
import pytest

from bill_member import calculate_bill

TEST_METER_READING_DATA = {'member-123': [{'account-abc': [{'electricity': [
    {'cumulative': 17580, 'readingDate': '2017-03-28T00:00:00.000Z',
     'unit': 'kWh'},
    {'cumulative': 17759, 'readingDate': '2017-04-15T00:00:00.000Z',
     'unit': 'kWh'},
    {'cumulative': 18002, 'readingDate': '2017-05-08T00:00:00.000Z',
     'unit': 'kWh'},
    {'cumulative': 18270, 'readingDate': '2017-06-18T00:00:00.000Z',
     'unit': 'kWh'},
    {'cumulative': 18453, 'readingDate': '2017-07-31T00:00:00.000Z',
     'unit': 'kWh'},
    {'cumulative': 18620, 'readingDate': '2017-08-31T00:00:00.000Z',
     'unit': 'kWh'},
    {'cumulative': 18682, 'readingDate': '2017-09-10T00:00:00.000Z',
     'unit': 'kWh'},
    {'cumulative': 18905, 'readingDate': '2017-10-27T00:00:00.000Z',
     'unit': 'kWh'},
    {'cumulative': 19150, 'readingDate': '2017-11-04T00:00:00.000Z',
     'unit': 'kWh'},
    {'cumulative': 19517, 'readingDate': '2017-12-31T00:00:00.000Z',
     'unit': 'kWh'},
    {'cumulative': 19757, 'readingDate': '2018-01-23T00:00:00.000Z',
     'unit': 'kWh'},
    {'cumulative': 20090, 'readingDate': '2018-02-19T00:00:00.000Z',
     'unit': 'kWh'},
    {'cumulative': 20276, 'readingDate': '2018-03-14T00:00:00.000Z',
     'unit': 'kWh'},
    {'cumulative': 20600, 'readingDate': '2018-04-29T00:00:00.000Z',
     'unit': 'kWh'},
    ]}], 'account-bbc': [{'electricity': [
      {'cumulative': 17580, 'readingDate': '2017-03-28T00:00:00.000Z',
       'unit': 'kWh'},
      {'cumulative': 17759, 'readingDate': '2017-04-15T00:00:00.000Z',
       'unit': 'kWh'},
      {'cumulative': 18002, 'readingDate': '2017-05-08T00:00:00.000Z',
       'unit': 'kWh'},
      {'cumulative': 18270, 'readingDate': '2017-06-18T00:00:00.000Z',
       'unit': 'kWh'},
      {'cumulative': 18453, 'readingDate': '2017-07-31T00:00:00.000Z',
       'unit': 'kWh'},
      {'cumulative': 18620, 'readingDate': '2017-08-31T00:00:00.000Z',
       'unit': 'kWh'},
      {'cumulative': 18682, 'readingDate': '2017-09-10T00:00:00.000Z',
       'unit': 'kWh'},
      {'cumulative': 18905, 'readingDate': '2017-10-27T00:00:00.000Z',
       'unit': 'kWh'},
      {'cumulative': 19150, 'readingDate': '2017-11-04T00:00:00.000Z',
       'unit': 'kWh'},
      {'cumulative': 19517, 'readingDate': '2017-12-31T00:00:00.000Z',
       'unit': 'kWh'},
      {'cumulative': 19757, 'readingDate': '2018-01-23T00:00:00.000Z',
       'unit': 'kWh'},
      {'cumulative': 20090, 'readingDate': '2018-02-19T00:00:00.000Z',
       'unit': 'kWh'},
      {'cumulative': 20276, 'readingDate': '2018-03-14T00:00:00.000Z',
       'unit': 'kWh'},
      {'cumulative': 20600, 'readingDate': '2018-04-29T00:00:00.000Z',
       'unit': 'kWh'},
    ]}]}],
        'member-236': [{'account-abc': [{'electricity': [
            {'cumulative': 20276,
             'readingDate': '2018-03-14T00:00:00.000Z',
             'unit': 'kWh'},
            {'cumulative': 20600,
             'readingDate': '2018-04-29T00:00:00.000Z',
             'unit': 'kWh'}],
          'gas': [
            {'cumulative': 20276,
             'readingDate': '2018-03-14T00:00:00.000Z',
             'unit': 'kWh'},
            {'cumulative': 20600,
             'readingDate': '2018-04-29T00:00:00.000Z',
             'unit': 'kWh'}]}],
          'account-bbc': [{'electricity': [
              {'cumulative': 17580,
               'readingDate': '2017-03-28T00:00:00.000Z',
               'unit': 'kWh'},
              {'cumulative': 17759,
               'readingDate': '2017-04-15T00:00:00.000Z',
               'unit': 'kWh'}],
            'gas': [{'cumulative': 17580,
                                         'readingDate': '2017-03-28T00:00:00.000Z',
                       'unit': 'kWh'}, {'cumulative': 17759,
                       'readingDate': '2017-04-15T00:00:00.000Z',
                       'unit': 'kWh'}]}]}]}


@pytest.mark.parametrize(
  'bill_date, member_id, account_id, expected_result', [
      ('2017-6-30', 'member-123', 'account-abc', (30.79, 196)),
      ('2017-08-31', 'member-123',  'account-bbc', (27.57, 167)),
      ('2017-08-10', 'member-123',  'account-bbc', (27.57, 167)),
      ('2017-9-30', 'member-123',  'ALL', (51.82, 372)),
      ('2017-10-31',  'member-123', 'account-bbc', (25.18, 147)),
      ('2017-11-30',  'member-123', 'account-abc', (117.06, 918)),
      ('2017-11-30',  'member-123', 'ALL', (226.75, 1836)),
      ('2018-1-31',  'member-123', 'account-abc', (46.21, 323)),
      ('2018-01-31', 'member-123', None, (84.8, 646)),
      ('2018-04-30', 'member-123', 'account-abc', (42.98, 298)),
      ('2018-04-30', 'member-123', 'ALL', (78.58, 596)),
      # checking multi accounts and gas/electricity combo
      ('2018-04-30', 'member-236', 'account-abc', (47.97, 211)),
      ('2018-04-30', 'member-236', 'ALL', (94.9, 509)),
  ])
def test_calculate_bill_for_month(
        mocker, bill_date, member_id, account_id, expected_result):
    mocker.patch(
      'load_readings.get_readings', return_value=TEST_METER_READING_DATA)
    amount, kwh = calculate_bill(member_id=member_id,
                                 account_id=account_id,
                                 bill_date=bill_date)
    assert amount == expected_result[0]
    assert kwh == expected_result[1]


@pytest.mark.parametrize('bill_date, member_id, account_id, expected_error', [
  ('2017-3-30', 'member-123', 'account-abc', TypeError),
  ('2017-3-30', 'member-123-invalid-member', 'account-abc', KeyError),
  ('2017-3-30', 'member-123', 'invalid-account-abc', KeyError),
])
def test_calculate_bill_exceptions(
        mocker, bill_date, member_id, account_id, expected_error):
    mocker.patch(
      'load_readings.get_readings', return_value=TEST_METER_READING_DATA)
    with pytest.raises(expected_error):
        calculate_bill(
          member_id=member_id, account_id=account_id, bill_date=bill_date)
