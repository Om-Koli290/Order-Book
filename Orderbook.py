from sortedcontainers import SortedDict
from collections import deque
import uuid
import time

class Order:
    def __init__(self, side, price, quantity):
        self.id = str(uuid.uuid4())[:8]
        self.side = side  # 'buy' or 'sell'
        self.price = price
        self.quantity = quantity
        self.timestamp = time.time()

class OrderBook:
    def __init__(self):
        self.bids = SortedDict(lambda x: -x)  # Descending prices for bids
        self.asks = SortedDict()               # Ascending prices for asks
        self.trade_log = []

    def _add_to_book(self, book, order):
        if order.price not in book:
            book[order.price] = deque()
        book[order.price].append(order)

    def place_limit_order(self, side, price, quantity):
        order = Order(side, price, quantity)
        print(f"New {side.upper()} order: {quantity}@{price}")
        trades = []

        if side == "buy":
            trades = self._match_order(order, self.asks, self.bids)
        else:
            trades = self._match_order(order, self.bids, self.asks)

        self.trade_log.extend(trades)
        return order.id, trades

    def _match_order(self, incoming, opposite_book, same_book):
        trades = []
        while incoming.quantity > 0 and len(opposite_book) > 0:
            best_price = next(iter(opposite_book))
            if (incoming.side == "buy" and incoming.price < best_price) or \
               (incoming.side == "sell" and incoming.price > best_price):
                break  # No price match possible

            queue = opposite_book[best_price]
            while queue and incoming.quantity > 0:
                resting_order = queue[0]
                trade_qty = min(incoming.quantity, resting_order.quantity)

                trades.append({
                    "buy_order": incoming.id if incoming.side == "buy" else resting_order.id,
                    "sell_order": resting_order.id if incoming.side == "buy" else incoming.id,
                    "price": best_price,
                    "quantity": trade_qty,
                    "timestamp": time.time()
                })

                resting_order.quantity -= trade_qty
                incoming.quantity -= trade_qty

                if resting_order.quantity == 0:
                    queue.popleft()
                if incoming.quantity == 0:
                    break

            if not queue:
                del opposite_book[best_price]

        if incoming.quantity > 0:
            self._add_to_book(same_book, incoming)

        return trades

    def get_book_snapshot(self, depth=5):
        top_bids = [(p, sum(o.quantity for o in q)) for p, q in list(self.bids.items())[:depth]]
        top_asks = [(p, sum(o.quantity for o in q)) for p, q in list(self.asks.items())[:depth]]
        return top_bids, top_asks

    def get_trade_log(self):
        return self.trade_log[-20:]  # Last 20 trades
