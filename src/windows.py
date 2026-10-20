"""Franjas horarias más baratas y más caras dentro de un día."""
from math import fsum


def _windows(prices, length):
    for i in range(len(prices) - length + 1):
        yield i, fsum(prices[i:i + length]) / length


def cheapest(prices, length):
    """(índice de inicio, precio medio) de la franja contigua más barata.

    En caso de empate gana la que empieza antes. None si no caben `length` horas.
    """
    best = None
    for i, avg in _windows(prices, length):
        if best is None or round(avg, 9) < round(best[1], 9):
            best = (i, avg)
    return best


def priciest(prices, length):
    worst = None
    for i, avg in _windows(prices, length):
        if worst is None or round(avg, 9) > round(worst[1], 9):
            worst = (i, avg)
    return worst


def summary(prices):
    if not prices:
        return None
    lo = min(range(len(prices)), key=lambda i: (prices[i], i))
    hi = max(range(len(prices)), key=lambda i: (prices[i], -i))
    return {"avg": fsum(prices) / len(prices), "min": prices[lo], "min_i": lo,
            "max": prices[hi], "max_i": hi}


def tiers(prices):
    """0 = barata, 1 = media, 2 = cara, por terciles del propio día."""
    order = sorted(range(len(prices)), key=lambda i: (prices[i], i))
    n = len(prices)
    out = [0] * n
    for rank, i in enumerate(order):
        out[i] = min(2, rank * 3 // n)
    return out


def plan_appliance(prices, hours, kwh):
    """Mejor franja para un aparato que dura `hours` horas y gasta `kwh`.

    Devuelve inicio, coste en € en la franja más barata y ahorro frente a la
    más cara (los precios vienen en €/MWh).
    """
    best = cheapest(prices, hours)
    if best is None:
        return None
    worst = priciest(prices, hours)
    cost = best[1] / 1000 * kwh
    return {"start": best[0], "hours": hours, "cost": cost,
            "saving": worst[1] / 1000 * kwh - cost}
