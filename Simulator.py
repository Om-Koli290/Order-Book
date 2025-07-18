import random
import time

def simulate_random_orders(orderbook, n_orders=5, base_price=100, price_volatility=2, max_quantity=100):
    for _ in range(n_orders):
        side = random.choice(["buy", "sell"])
        price_fluctuation = random.uniform(-price_volatility, price_volatility)
        price = round(base_price + price_fluctuation, 2)
        quantity = random.randint(1, max_quantity)

        orderbook.place_limit_order(side, price, quantity)
