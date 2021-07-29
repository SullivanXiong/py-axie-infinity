import requests


AXS = [0, 4, 4, 4, 4, 4, 4, 4]
SLP = [0, 300, 600, 900, 1500, 2400, 3900, 6300]
number_of_possible_breeds = 7
"""
number_of_transactions comes from destructuring the flow of the breeding process

Alternative 1:
    Buy ETH -> Transfer ETH to MetaMask (1) -> Buy AXS from Uniswap (2) ->
      Buy SLP from Uniswap (3) -> Transfer ETH to Ronin (4) -> Transfer AXS to Ronin (5) ->
      Transfer SLP to Ronin (6)

Alternative 2:
    Transfer Earned WETH from Ronin to MetaMask (1) -> Buy AXS from Uniswap (2) ->
      Buy SLP from Uniswap (3) -> Transfer AXS to Ronin (4) -> Transfer SLP to Ronin (5)

Alternative 3:
   Transfer Earned WETH from Ronin to MetaMask (1) -> Buy AXS from Uniswap (2) ->
     Transfer AXS to Ronin (3)
"""
number_of_transactions = (6 + 5 + 3) / 3

def wrapped_input(message):
    loop = True
    while loop:
        inp = input(message)
        try:
            inp = round(float(inp), 2)
            loop = False
        except:
            print('incorrect input type\n')
            loop = True
    return inp

def cost_to_breed(breed_num, axs_p, slp_p):
    return (AXS[breed_num] * axs_p) + (SLP[breed_num] * slp_p)

def gen_costs(axs_p, slp_p):
    return [cost_to_breed(i, axs_p, slp_p) for i in range(number_of_possible_breeds + 1)]

def max_of_profit(breeding_profits):
    max_idx = 0
    max_val = 0
    for idx, profit in enumerate(breeding_profits):
        if profit >= max_val:
            max_val = profit
            max_idx = idx

    return max_idx + 1, max_val

def get_token_price():
    PRICES = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=smooth-love-potion,axie-infinity&vs_currencies=usd').json()
    AXS_PRICE = PRICES['axie-infinity']['usd']
    SLP_PRICE = PRICES['smooth-love-potion']['usd']
    return AXS_PRICE, SLP_PRICE

def sum_axs(breed_count):
    return sum(AXS[:breed_count + 1])

def sum_slp(breed_count):
    return sum(SLP[:breed_count + 1])

def generate_profits(AXS_PRICE, SLP_PRICE, min_sale_price, eth_gas_fees):
    breeding_profits = []
    breeding_costs = []

    prev_cost = 0
    for breed_count, cost in enumerate(gen_costs(AXS_PRICE, SLP_PRICE)):
        if breed_count != 0:
            revenue = (breed_count * min_sale_price)
            cost_tx = round(prev_cost + (cost + (eth_gas_fees * number_of_transactions)), 2)
            breeding_costs.append(cost_tx)
            profit = round(revenue - cost_tx, 2)
            breeding_profits.append(profit)
            print(f'breed #{breed_count} profit:{profit}\t\tTOTAL_COST: {cost_tx}\t\tAXS: {sum_axs(breed_count)}\t\tSLP: {sum_slp(breed_count)}')
        prev_cost += cost

    return breeding_profits, breeding_costs

def breed_main():
    AXS_PRICE, SLP_PRICE = get_token_price()
    min_sale_price = wrapped_input('Minimum sale price (regardless of breed count): ')
    eth_gas_fees = wrapped_input('Average ethereum gas fee right now: ')
    print(f'Average number of transactions: {number_of_transactions}')
    print(f'\nAXS_PRICE: {AXS_PRICE}')
    print(f'SLP_PRICE: {SLP_PRICE}\n')

    breeding_profits, breeding_costs = generate_profits(AXS_PRICE, SLP_PRICE, min_sale_price, eth_gas_fees)  

    max_profit_idx, max_profit = max_of_profit(breeding_profits)
    max_profit_cost = breeding_costs[max_profit_idx - 1]
    print(f'Most profits at {max_profit_idx} breeds, with {max_profit} profits.\t\tTOTAL_COST: {max_profit_cost}\t\tAXS: {sum_axs(max_profit_idx)}\t\tSLP: {sum_slp(max_profit_idx)}')
    return min_sale_price, max_profit_idx, breeding_costs, sum_axs(max_profit_idx), sum_slp(max_profit_idx)

if __name__ == '__main__':
    breed_main()
