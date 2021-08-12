from mining_company_lib import (
    Game, World, Government, Region, Bank, Asset, Product, Entity, 
    Autonomous_organization, Q_)



def main():
    
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
    company_1 = w.add_company('RosPromMining', 100_000)
    print()
    

    company_1.buy(assets['C'])
    # print(assets['C'].get_owner().get_name())
    
    assets['C'].start_asset()
    asset_c = assets['C']
    
    
    company_1.confirm_actions()
    
    shoping_list = {
        'Mining_equipment_class_C': Q_(4, 'count'), 
        'Preparation_line': Q_(1, 'count')
        }
    
    asset_c.equipment_fleet.amount_of_equipment_available_for_buy()
    asset_c.equipment_fleet.set_target_amount_of_equipment(shoping_list)
    
    company_1.confirm_actions()
    
    company_1.get_company_status()
    

if __name__ == "__main__":
    main()