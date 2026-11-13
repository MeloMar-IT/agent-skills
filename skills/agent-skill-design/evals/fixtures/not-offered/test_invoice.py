import invoice


def test_total():
    assert invoice.total([(2, 9.5), (1, 20.0)]) == 39.0


def test_render():
    assert invoice.render([(1, 5.0)]) == "Total: 5.00"
