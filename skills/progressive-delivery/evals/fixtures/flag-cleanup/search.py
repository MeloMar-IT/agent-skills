from flagclient import is_on


def fast_index(q):
    return ["fast:" + q]


def slow_index(q):
    return ["slow:" + q]


def search(q):
    if is_on("fast-search", default=True):
        return fast_index(q)
    return slow_index(q)
