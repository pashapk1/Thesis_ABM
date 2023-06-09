from AgentBasedModel.simulator import SimulatorInfo
import AgentBasedModel.utils.math as math
import matplotlib.pyplot as plt


def plot_price(info: SimulatorInfo, spread=False, rolling: int = 1, figsize=(6, 6), save_path: str = None):
    plt.figure(figsize=figsize)
    plt.title(f'Stock Price {info.exchange.id}') if rolling == 1 else plt.title(
        f'Stock Price {info.exchange.id} (MA {rolling})')
    plt.xlabel('Iterations')
    plt.ylabel('Price')
    plt.plot(range(rolling - 1, len(info.prices)), math.rolling(info.prices, rolling), color='black')
    if spread:
        v1 = [el['bid'] for el in info.spreads]
        v2 = [el['ask'] for el in info.spreads]
        plt.plot(range(rolling - 1, len(v1)), math.rolling(v1, rolling), label='bid', color='green')
        plt.plot(range(rolling - 1, len(v2)), math.rolling(v2, rolling), label='ask', color='red')
    # plt.show()
    plt.savefig(save_path) if save_path else plt.show()


def plot_price_fundamental(info: SimulatorInfo, spread=False, access: int = 1, rolling: int = 1,
                           figsize=(6, 6), save_path: str = None):
    plt.figure(figsize=figsize)
    if rolling == 1:
        plt.title(f'Stock {info.exchange.id} Fundamental and Market value')
    else:
        plt.title(f'Stock {info.exchange.id} Fundamental and Market value (MA {rolling})')
    plt.xlabel('Iterations')
    plt.ylabel('Present value')
    if spread:
        v1 = [el['bid'] for el in info.spreads]
        v2 = [el['ask'] for el in info.spreads]
        plt.plot(range(rolling - 1, len(v1)), math.rolling(v1, rolling), label='bid', color='green')
        plt.plot(range(rolling - 1, len(v2)), math.rolling(v2, rolling), label='ask', color='red')
    plt.plot(range(rolling - 1, len(info.prices)), math.rolling(info.prices, rolling), label='market value',
             color='black')
    plt.plot(range(rolling - 1, len(info.prices)), math.rolling(info.fundamental_value(access), rolling),
             label='fundamental value')

    # add vertical lines at each event iteration where stock_id equals exchange.id
    for event in info.events:
        if event.stock_id == info.exchange.id:
            plt.axvline(x=event.it, color=event.color, linestyle='--', label=event.__class__.__name__)
    plt.legend()
    # plt.show()
    plt.savefig(save_path) if save_path else plt.show()


def plot_arbitrage(info: SimulatorInfo, access: int = 1, rolling: int = 1, figsize=(6, 6), save_path: str = None):
    plt.figure(figsize=figsize)
    if rolling == 1:
        plt.title(f'Stock {info.exchange.id} Fundamental and Market value difference %')
    else:
        plt.title(f'Stock {info.exchange.id} Fundamental and Market value difference % (MA {rolling})')
    plt.xlabel('Iterations')
    plt.ylabel('Present value')
    market = info.prices
    fundamental = info.fundamental_value(access)
    arbitrage = [(fundamental[i] - market[i]) / fundamental[i] for i in range(len(market))]
    plt.plot(range(rolling, len(arbitrage) + 1), math.rolling(arbitrage, rolling), color='black')
    # plt.show()
    plt.savefig(save_path) if save_path else plt.show()


def plot_dividend(info: SimulatorInfo, rolling: int = 1, figsize=(6, 6), save_path: str = None):
    plt.figure(figsize=figsize)
    plt.title(f'Stock {info.exchange.id} Dividend') if rolling == 1 else plt.title(
        f'Stock {info.exchange.id} Dividend (MA {rolling})')
    plt.xlabel('Iterations')
    plt.ylabel('Dividend')
    plt.plot(range(rolling, len(info.dividends) + 1), math.rolling(info.dividends, rolling), color='black')
    # plt.show()
    plt.savefig(save_path) if save_path else plt.show()


def plot_orders(info: SimulatorInfo, stat: str = 'quantity', rolling: int = 1, figsize=(6, 6), save_path: str = None):
    plt.figure(figsize=figsize)
    plt.title(f'Book {info.exchange.id} Orders') if rolling == 1 else plt.title(
        f'Book {info.exchange.id} Orders (MA {rolling})')
    plt.xlabel('Iterations')
    plt.ylabel(stat)
    v1 = [v[stat]['bid'] for v in info.orders]
    v2 = [v[stat]['ask'] for v in info.orders]
    plt.plot(range(rolling, len(v1) + 1), math.rolling(v1, rolling), label='bid', color='green')
    plt.plot(range(rolling, len(v2) + 1), math.rolling(v2, rolling), label='ask', color='red')
    plt.legend()
    # plt.show()
    plt.savefig(save_path) if save_path else plt.show()


def plot_volatility_price(info: SimulatorInfo, window: int = 5, figsize=(6, 6), save_path: str = None):
    plt.figure(figsize=figsize)
    plt.title(f'Stock {info.exchange.id} Price Volatility (window {window})')
    plt.xlabel('Iterations')
    plt.ylabel('Price Volatility')
    volatility = info.price_volatility(window)
    plt.plot(range(window, len(volatility) + window), volatility, color='black')
    # plt.show()
    plt.savefig(save_path) if save_path else plt.show()


def plot_volatility_return(info: SimulatorInfo, window: int = 5, figsize=(6, 6), save_path: str = None):
    plt.figure(figsize=figsize)
    plt.title(f'Stock {info.exchange.id} Return Volatility (window {window})')
    plt.xlabel('Iterations')
    plt.ylabel('Return Volatility')
    volatility = info.return_volatility(window)
    plt.plot(range(window, len(volatility) + window), volatility, color='black')
    # plt.show()
    plt.savefig(save_path) if save_path else plt.show()


def plot_liquidity(info: SimulatorInfo, rolling: int = 1, figsize=(6, 6), save_path: str = None):
    plt.figure(figsize=figsize)
    plt.title(f'Liquidity {info.exchange.id}') if rolling == 1 else plt.title(
        f'Liquidity {info.exchange.id} (MA {rolling})')
    plt.xlabel('Iterations')
    plt.ylabel('Spread / avg. Price')
    plt.plot(info.liquidity(rolling), color='black')
    # plt.show()
    plt.savefig(save_path) if save_path else plt.show()
