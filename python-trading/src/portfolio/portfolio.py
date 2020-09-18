import enum
import logging

# give the local logger this module name so that it can be identified
logger = logging.getLogger(__name__)


class Direction(enum.Enum):
    """Static enum class to determine the direction of a trade"""
    BUY = 1
    SELL = 2


class Asset():
    """Atomic stock asset class"""

    def __init__(self, name: str, price=0.0):
        """Initializer with name only - minimum initializer that works"""
        self.name = name
        self.price = price

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        """Set the name attribute

        N.B. name must be provided"""
        if (name is None) or (len(name) < 1):
            raise ValueError("Asset must have a name provided")

        self._name = name

    @property
    def price(self) -> float:
        """Get the price of the asset"""
        return self._price

    @price.setter
    def price(self, price: float):
        """Set the price of the asset

        N.B. must be a non-negative, non-zero price"""
        if price < 0:
            raise ValueError(f"Stock price must be non-negative: price = {price}")

        self._price = price


class Order():
    """Definition of Order, which contains instructions of trades"""
    def __init__(self, asset: Asset, direction: Direction, qty: int):
        """Default initialization"""
        self.asset = asset
        self.direction = direction
        self.quantity = qty

    @property
    def direction(self) -> Direction:
        """Return order direction (BUY/SELL)"""
        return self._direction

    @direction.setter
    def direction(self, direction: Direction):
        """Set the trade direction (BUY/SELL)"""
        if not isinstance(direction, enum.Enum):
            raise TypeError(f"Direction given is invalid type: {type(direction)}")

        self._direction = direction

    @property
    def quantity(self) -> int:
        """Return the quantity of this order"""
        return self._quantity

    @quantity.setter
    def quantity(self, quantity: int):
        """Set the quantity of this order (must be > 0)"""
        if quantity < 1:
            raise ValueError("Quantity must be greater than 0")

        self._quantity = quantity

    @property
    def asset(self) -> Asset:
        """Return the asset associated with order"""
        return self._asset

    @asset.setter
    def asset(self, asset: Asset):
        """Set the asset associated with this order"""
        if asset is None:
            raise ValueError("Asset must be valid")

        self._asset = asset

    def value(self) -> float:
        """Determines the value of the order"""
        return self.asset.price * self.quantity

    def __str__(self) -> str:
        """Convert the order to a string"""
        return f"Order details: ({self.asset.name}, Qty: {self.quantity}, Value: {self.value()})"


class Portfolio():
    """Class which performs trader's portfolio operations, and tracks total assets"""
    def __init__(self, name: str, balance: float):
        """Default initialization. N.B. initial assets are empty"""
        self.name = name
        self.balance = balance
        self._assets = []

    @property
    def name(self) -> str:
        """Get the portfolio name"""
        return self._name

    @name.setter
    def name(self, name: str):
        """Set the portfolio name attribute

        N.B. must be a valid name"""
        if (name is None) or (len(name) < 1):
            raise ValueError("Portfolio name must be valid")

        self._name = name

    @property
    def assets(self):
        """Return the list of assets"""
        return self._assets

    @property
    def balance(self) -> float:
        """Get current balance of the portfolio (only initial setting)"""
        return self._balance

    @balance.setter
    def balance(self, balance: float):
        """Set the balance"""
        if balance < 0:
            raise ValueError("Balance cannot go negative")

        self._balance = balance

    def buy(self, asset: Asset, qty: int):
        """Add stocks to the portfolio

        N.B. balance check must be done prior"""

        # add each stock individually
        for i in range(qty):
            self._assets.append(asset)
            self._balance -= asset.price

    def sell(self, asset: Asset, qty: int):
        """Sell stock from the portfolio, receiving current price into balance

        N.B. check for existing stocks must be done prior"""

        # remove each stock individually
        # TODO: refactor this
        sold = 0
        while sold < qty:
            j = 0
            for a in self._assets:
                if a.name == asset.name:
                    self._assets.remove(a)
                    self._balance += asset.price
                    sold = sold + 1
                    break

    def invest(self, investment: float):
        """Invest additional funds to purchase more stocks"""
        if investment <= 0:
            raise ValueError("Investment of funds must be > 0")

        self._balance += investment

        logger.info(f"Invested funds: {investment}. New balance = {self._balance}")

    def placeOrder(self, order: Order):
        """Place a trade, and update portfolio

        N.B. assumes that the order has been deemed valid already"""
        if not isinstance(order, Order):
            raise TypeError(f"order must be an Order instance, not {type(order)}")

        logger.info(f"Current balance: {self.balance}")

        # make the trade
        if order.direction == Direction.BUY:
            # check if you can buy this many stocks
            if self.balance < order.value():
                raise InsufficientFundsException(self, order)

            self.buy(order.asset, order.quantity)
        elif order.direction == Direction.SELL:
            # check if you can sell this many stocks
            portfolio_qty = 0
            for a in self._assets:
                if a.name == order.asset.name:
                    portfolio_qty += 1

            if portfolio_qty < order.quantity:
                raise AssetNotPresentException(self, order.asset)

            self.sell(order.asset, order.quantity)

        logger.info(f"New balance: {self.balance}")


class InsufficientFundsException(Exception):
    """Exceptions for handling buying"""
    def __init__(self, p: Portfolio, o: Order):
        self._portfolio = p
        self._order = o
        self._message = "Insufficient funds.\n"
        self._message += f"Portfolio: {p.name}, balance: {p.balance}\n"
        self._message += f"Order: {o.asset.name}, qty: {o.quantity}, value: {o.value()}"

        super().__init__(self._message)


class AssetNotPresentException(Exception):
    """Exception for handling selling"""
    def __init__(self, p: Portfolio, a: Asset):
        self._asset = a
        self._portfolio = p

        self._message = "Asset not present to sell.\n"
        self._message += f"Portfolio: {p.name}.\n"
        self._message += f"Asset: {a.name}"

        super().__init__(self._message)
