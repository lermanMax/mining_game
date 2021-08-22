from mining_company_lib import (
    Game, World, Government, Region, Bank, Asset, Product, Entity, 
    Autonomous_organization, Q_)

from collections import Mapping, Container
from sys import getsizeof

 
def deep_getsizeof(o, ids):
    """Find the memory footprint of a Python object
 
    This is a recursive function that drills down a Python object graph
    like a dictionary holding nested dictionaries with lists of lists
    and tuples and sets.
 
    The sys.getsizeof function does a shallow size of only. It counts each
    object inside a container as pointer only regardless of how big it
    really is.
 
    :param o: the object
    :param ids:
    :return:
    """
    d = deep_getsizeof
    if id(o) in ids:
        return 0
 
    r = getsizeof(o)
    ids.add(id(o))
 
    if isinstance(o, str) or isinstance(0, str):
        return r
 
    if isinstance(o, Mapping):
        return r + sum(d(k, ids) + d(v, ids) for k, v in o.iteritems())
 
    if isinstance(o, Container):
        return r + sum(d(x, ids) for x in o)
 
    return r


if __name__ == "__main__":
    
    world_parameters = {
        'name': 'Game_1',
        'hours_per_round': 2016,
        'working_hours_per_round': 480,
        'overtime_hours_per_round': 128,
        'rounds_per_year': 4,
        'regions':[
            {
                'name': 'North', 
                'balance': 10_000_000,
                'assets':[
                    {
                        'name': 'A', 
                        'balance': 0, 
                        'price': 70_000,
                        'initial_investment': 10_000,
                        'estimated_coal_supply': 1_000_000_000},
                    {
                        'name': 'B', 
                        'balance': 0, 
                        'price': 45_000,
                        'initial_investment': 10_000,
                        'estimated_coal_supply': 700_000_000}]
                },
            {
                'name': 'West_', 
                'balance': 30_000_000,
                'assets':[
                    {
                        'name': 'C', 
                        'balance': 0, 
                        'price': 20_000,
                        'initial_investment': 20_000,
                        'estimated_coal_supply': 600_000_000}]
                }
            ]
        }

    Game_1 = Game()
    
    w = Game_1.create_world(world_parameters)
    
    print()
    
    assets = {}
    
    for region in w.list_of_regions:
        for asset in region.get_list_of_assets():
            asset.change_product_status(Product.sale_status)
    print('\nname    price status')
    for region in w.list_of_regions:
        for asset in region.get_list_of_assets():
            assets[asset.get_name()] = asset
            print(asset.get_name(), 
                  asset.my_region.get_name(), 
                  asset.get_price(), 
                  asset.get_product_status())
        
    print()
    company_1 = w.add_company('RosPromMining', 1_000_000)
    print()
    

    company_1.buy(assets['C'])
    # print(assets['C'].get_owner().get_name())
    
    assets['C'].start_asset()
    asset_c = assets['C']
    
    
    company_1.confirm_actions()
    
    target_list = {
        'Mining_equipment_class_C': Q_(4, 'count'), 
        'Preparation_line': Q_(1, 'count')
        }
    
    input()
    
    # asset_c.equipment_fleet.get_amount_of_equipment()
    # asset_c.equipment_fleet.amount_of_equipment_available_for_buy()
    # asset_c.my_region.equipment_market.amount_of_equipment_available_for_sale()
    
    # asset_c.equipment_fleet.set_target_amount_of_equipment(target_list)
    # asset_c.invest_money(200_000)
    
    # company_1.confirm_actions()
    
    # company_1.get_company_status()