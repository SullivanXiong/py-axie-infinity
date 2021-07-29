from axie_breed import breed_main, wrapped_input, cost_to_breed, gen_costs, max_of_profit, get_token_price, generate_profits

def bool_wrapped_input(message):
    mode = int(wrapped_input(message))
    while (mode != 0 and mode != 1):
        mode = int(wrapped_input(message))
    if mode == 1:
        return True
    return False

def infinite_loop_chain(chain_length, num_of_breeds_per_pair, num_of_generations):
    num_of_breeding_pairs = num_of_generations - 1
    num_of_total_axies = (num_of_breeds_per_pair * num_of_breeding_pairs) + chain_length
    num_of_non_virgins = num_of_breeding_pairs * 2
    num_of_virgins = num_of_total_axies - num_of_non_virgins
    return num_of_breeding_pairs, num_of_non_virgins, num_of_virgins

def breed_after(plan, num_of_virgins, chain_length):
    if plan:
        return num_of_virgins - chain_length
    return num_of_virgins

def chain_main():
    num_of_generations = int(wrapped_input('Number of generations you\'re aiming for: '))
    plan_to_breed_after = bool_wrapped_input(f'Do you plan to breed more after {num_of_generations} generations? [1]-Yes [0]-No: ')
    min_sale_price_virgin = wrapped_input('Minimum sale price of virgin axie: ')
    
    min_sale_price_non_virgin, max_profit_breed_count, breeding_costs_lst, breeding_axs_cost, breeding_slp_cost = breed_main()
    breeding_costs = breeding_costs_lst[max_profit_breed_count]
    
    print('\n\n\n\n------------------------INFINITE-BREED-CHAINING------------------------')

    for i in range(2, 5):
        if i > 2:
            can_infinite_chain = '~~CAN INFINITE CHAIN~~'
        else:
            can_infinite_chain = '~~CAN\'T INFINITE CHAIN~~'

        print(f'\n{can_infinite_chain}\nCHAIN LENGTH: {i}\n\t', end='')
        num_of_breeding_pairs, num_of_non_virgins, num_of_virgins = infinite_loop_chain(i, max_profit_breed_count, num_of_generations)
        
        num_of_virgins = breed_after(plan_to_breed_after, num_of_virgins, i)
        print(f'Number of VIRGINS: {num_of_virgins}\t\tNumber of NON-VIRGINS: {num_of_non_virgins}')

        revenue = (min_sale_price_non_virgin * num_of_non_virgins) + (min_sale_price_virgin * num_of_virgins)
        # only use if not breeding more
        # axie_init_cost = min_sale_price_virgin * num_of_non_virgins
        axie_additional_init_cost = i - 2
        cost = (num_of_breeding_pairs * breeding_costs) + (axie_additional_init_cost * min_sale_price_virgin)
        cost = round(cost, 2)
        profit = round(revenue - cost, 2)
        
        total_axs = num_of_breeding_pairs * breeding_axs_cost
        total_slp = num_of_breeding_pairs * breeding_slp_cost
        print(f'\tProfit: {profit}\t\tCost: {cost}\t\tAXS: {total_axs}\t\tSLP: {total_slp}')

if __name__ == '__main__':
    chain_main()
