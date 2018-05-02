import pytest

from ruter import Ruter

# Any place with a lot of Ruter activity should work here
TESTING_PLACE = 'Majorstuen'

# In each of these dicts, the key is expected to be in the response. The values
# are allowed types that each field in the response is allowed to have.
# type(None) corresponds to null in the JSON response.
EXPECTED_KEYS_IN_HEARTBEAT = {
    'OtpVersion': (str, ),
    'Otp': (bool, ),
    'TransitServiceStarts': (str, ),
    'TransitServiceEnds': (str, ),
    'ReisVersion': (str, ),
    'OtpResponseTime': (int, ),
    'Sql': (bool, ),
    'SqlResponseTime': (int, ),
    'Els': (bool, ),
    'ElsVersion': (str, ),
    'ElseResponsetime': (int, ),  # [sic]
}

EXPECTED_KEYS_IN_STOP = {
    'X': (int, ),
    'Y': (int, ),
    'Zone': (str, ),
    'ShortName': (str, ),
    'IsHub': (bool, ),
    'ID': (int, ),
    'Name': (str, ),
    'District': (str, ),
    'DistrictID': (str, type(None)),
}

EXPECTED_KEYS_IN_LINE = {
    'ID': (int, ),
    'Name': (str, ),
    'Transportation': (int, ),
    'LineColour': (str, ),
}

EXPECTED_KEYS_IN_DEPARTURE = {
    "RecordedAtTime": (str, ),
    "MonitoringRef": (str, ),
    "MonitoredVehicleJourney": (dict, ),
    "Extensions": (dict, ),
    "StopVisitNote": (list, ),
}

EXPECTED_KEYS_IN_JOURNEY = {
    "LineRef": (str, ),
    "DirectionRef": (str, type(None)),
    "FramedVehicleJourneyRef": (dict, type(None)),
    "PublishedLineName": (str, ),
    "DirectionName": (str, type(None)),
    "OperatorRef": (str, type(None)),
    "OriginName": (str, ),
    "OriginRef": (str, ),
    "DestinationRef": (str, ),
    "DestinationName": (str, ),
    "OriginAimedDepartureTime": (str, ),
    "DestinationAimedArrivalTime": (str, ),
    "Monitored": (bool, ),
    "InCongestion": (bool, ),
    "Delay": (
        str,
        type(None),
    ),
    "TrainBlockPart": (
        dict,
        type(None),
    ),
    "BlockRef": (
        str,
        type(None),
    ),
    "VehicleRef": (
        str,
        type(None),
    ),
    "VehicleMode": (int, ),
    "VehicleJourneyName": (str, ),
    "MonitoredCall": (dict, ),
    "VehicleFeatureRef": (
        str,
        type(None),
    )
}


def ensure_is(data, reference):
    """Ensure the data has the structure given by the reference dictionary
    """
    for key, datatypes in reference.items():
        assert (key in data)
        assert (type(data[key]) in datatypes)


def ensure_is_stop(data):
    """Ensure the data is a dict corresponding to a stop
    """
    return ensure_is(data, EXPECTED_KEYS_IN_STOP)


def ensure_is_line(data):
    """Ensure the data is a dict corresponding to a line
    """
    return ensure_is(data, EXPECTED_KEYS_IN_LINE)


def ensure_is_departure(data):
    """Ensure the data is a dict corresponding to a departure
    """
    return ensure_is(data, EXPECTED_KEYS_IN_DEPARTURE)


def ensure_is_journey(data):
    """Ensure the data is a dict corresponding to a journey
    (it's called "MonitoredVehicleJourney" in departure fields)
    """
    return ensure_is(data, EXPECTED_KEYS_IN_JOURNEY)


def ensure_is_heartbeat(data):
    """Ensure the data is a dict corresponding to a heartbeat
    """
    return ensure_is(data, EXPECTED_KEYS_IN_HEARTBEAT)


def find_stop(places, must_have_lines=False):
    """Find a stop in the given list of places, optionally only choosing those
    stops which have more than one line going to them
    """
    for place in places:
        if place['PlaceType'] == 'Stop':
            if must_have_lines:
                if 'Lines' in place and len(place['Lines']) > 0:
                    return place
            else:
                return place
    return None


@pytest.fixture
def ruter():
    """Return a Ruter object
    """
    return Ruter()


_test_places = None


@pytest.fixture
def places():
    """Return a list of places (cached to avoid doing more API requests than
    needed
    """
    global _test_places
    if _test_places is None:
        ruter = Ruter()
        _test_places = ruter.get_places(TESTING_PLACE)
    return _test_places
