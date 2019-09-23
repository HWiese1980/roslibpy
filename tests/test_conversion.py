from roslibpy.conversions import from_epoch, to_epoch


def test_conversions():
    test_eps = 1e-4
    stamp = 1000.9876
    header_stamp = from_epoch(stamp)
    assert (abs(header_stamp["secs"] - 1000.) < test_eps)
    assert (abs(header_stamp["nsecs"] - 987.6 * 1e6) < test_eps)

    newstamp = to_epoch(header_stamp)
    assert abs(newstamp - stamp) < test_eps


if __name__ == '__main__':
    import logging

    logging.basicConfig(
        level=logging.INFO, format='[%(thread)03d] %(asctime)-15s [%(levelname)s] %(message)s')
    LOGGER = logging.getLogger('test')

    test_conversions()
