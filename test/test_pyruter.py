import itertools

from .helpers_for_testing import *


def test_set_location(ruter):
    """Test the set_location function
    """
    location = 'My location'

    ruter.set_location(location)

    assert (ruter.location == location)


def test_get_validities(ruter):
    """Test the get_validities function
    """
    validities = ruter.get_validities()

    assert ('ValidFrom' in validities)
    assert ('ValidTo' in validities)


def test_get_heartbeat(ruter):
    """Test the get_heartbeat function
    """
    heartbeat = ruter.get_heartbeat()
    ensure_is_heartbeat(heartbeat)


def test_get_places(places):
    """Test the get_places function (it's called in the fixture for `places`)
    """
    # Check that there are any responses
    assert (len(places) > 0)
    assert (all('PlaceType' in place for place in places))

    # Check that the response has the right structure.
    # Some places are "Areas" or "Points of interest", in which case they
    # contain a list of stops with the expected structure
    for place in places:
        if place['PlaceType'] == 'Stop':
            ensure_is_stop(place)
        else:
            assert ('Stops' in place)
            for stop in place['Stops']:
                ensure_is_stop(stop)


def test_get_stop(ruter, places):
    """Test the get_stop function
    """
    # Get a place to test with
    testing_place = find_stop(places)
    assert (testing_place is not None)

    # Test that get_stop returns the same result
    stop_response = ruter.get_stop(testing_place['ID'])
    for key in testing_place:
        assert (key in stop_response)
        if key != 'Lines':
            assert (stop_response[key] == testing_place[key])


def test_get_lines_by_stop_id(ruter, places):
    """Test the get_lines_by_stop_id function
    """
    # Get a line to test with
    testing_place = find_stop(places, must_have_lines=True)
    assert (testing_place is not None)

    # Test that get_lines_by_stop_id returns the same result
    lines_response = ruter.get_lines_by_stop_id(testing_place['ID'])
    assert (lines_response == testing_place['Lines'])
    for line in lines_response:
        ensure_is_line(line)


def test_get_stops_ruter(ruter):
    """Test the get_stops_ruter function
    """
    stops_ruter = ruter.get_stops_ruter()

    assert (len(stops_ruter) > 0)

    for stop in stops_ruter:
        ensure_is_stop(stop)


def test_get_lines_and_get_stops_by_line_id_and_get_data_by_line_id(ruter):
    """Test:
        - the get_lines function
        - the get_stops_by_line_id function
        - the get_data_by_line_id function

    TODO: refactor this into 3 tests?
    """
    # Call the function with all possible combinations of input arguments
    argument_lists = [{
        'ruter_operated_only': args[0],
        'extended': args[1]
    } for args in itertools.product((True, False), repeat=2)]

    for argument_list in argument_lists:
        lines = ruter.get_lines(**argument_list)

        assert (len(lines) > 0)

        for line in lines:
            ensure_is_line(line)

        # Test get_stops_by_line_id
        testing_line = lines[0]
        stops_response = ruter.get_stops_by_line_id(testing_line['ID'])

        assert (len(stops_response) > 0)
        for stop in stops_response:
            ensure_is_stop(stop)

        # Test get_data_by_line_id
        line_data_response = ruter.get_data_by_line_id(testing_line['ID'])
        assert (line_data_response == testing_line)


def test_get_departures_and_get_next_departure(ruter, places):
    """Test:
        - the get_departures function
        - the get_next_departure function

    TODO: refactor this into 2 tests?
    """
    testing_place = find_stop(places, must_have_lines=True)
    departures = ruter.get_departures(testing_place['ID'])
    for departure in departures:
        ensure_is_departure(departure)
        ensure_is_journey(departure['MonitoredVehicleJourney'])


def test_get_next_departure(ruter, places):
    """TODO: Test the get_next_departure function
    """


def test_get_time_until_next_departure(ruter, places):
    """TODO: Test the get_time_until_next_deprature function
    """


def test_get_street(ruter, places):
    """TODO: Test the get_street function
    """
