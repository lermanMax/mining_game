from __future__ import annotations
from pint import UnitRegistry
ureg = UnitRegistry()
Q_ = ureg.Quantity


class Game:
    """Создает новые миры 
    
    Добавляет игроков
    """

    def __init__(self):
        
        self.list_of_worlds = []
    
    
    def create_world(self, world_parameters: dict) -> World:
        
        new_world = World(world_parameters)
        self.list_of_worlds.append(new_world)
        print('New world was created')
        return new_world
        
    
    def destroy_world(self):
        pass
    
    
    def add_player(self):
        pass
    

class World:
    """Новая игра - новый мир
    
    Отвечает за смену раундов 
    """

    
    def __init__(self, world_parameters: dict):
        
        
        self.name = world_parameters['name']
        self._current_round = 0
        self.list_of_companies = set()
        self.list_of_regions = set()
        
        self.bank = Bank(name = 'Bank', world = self)
        self.government = Government(name = "Government", world = self)
        
        self._add_regions(world_parameters['regions'])
        
        
    
    def get_current_round(self) -> int:
        return self._current_round
    
    def add_company(self, name: str, balance: int) -> Company:
        new_company = Company(
            name=name, 
            world=self, 
            balance=balance)
        self.list_of_companies.add(new_company)
        print(f'Company "{new_company.name}" was added')
        return new_company
    
    
    def _add_regions(self, regions: list):
        
        for region in regions:
            new_region = Region(
                name = region['name'], 
                world = self, 
                balance = region['balance'])
            self.list_of_regions.add(new_region)
            self._add_assets(
                assets=region['assets'], 
                region=new_region)
    
    
    def _add_assets(self, assets: list, region: Region):
        
        for asset in assets:
            new_asset = Asset(
                name = asset['name'], 
                region = region,
                balance = asset['balance'], 
                price = asset['price'],
                initial_investment = asset['initial_investment'])
            
            region.list_of_assets.add(new_asset)
            
            
    def get_list_of_started_assets(self) -> set:
        started_list = set()
        for rigion in self.list_of_regions:
            for asset in rigion.list_of_assets:
                if asset.get_asset_status() != Asset.not_started_status:
                    started_list.add(asset)
                    
        return started_list
    
    
    def next_round(self):
        # проверка, что все компании готовы 
        for company in self.list_of_companies:
            if company.get_company_status() != Company.ready_status:
                return
        
        self._save_actions()
        
        # Все активы зарабатывают деньги
        for asset in self.get_list_of_started_assets():
            asset._make_money()
        # Все компании собирают прибыль с активов
        for company in self.list_of_companies:
            company._collect_profit_from_assets()
        
        
        print(f'Round {self._current_round} is finish')
        self._current_round += 1 
        print(f'Round {self._current_round} is start')
        
        # Все компании снова получают доступ к изменениям
        self._open_access_for_companies()
            
    
    def _save_actions(self):
        pass
    
    
    def _open_access_for_companies(self):
        for company in self.list_of_companies:
            company._change_company_status(Company.in_process_status)


class Bank:
    """
    Управляет транзакциями
    Выдает кредиты
    """

    
    def __init__(
            self, 
            name: str, 
            world: World, 
            balance: int = 0):
        
        self.name = name
        self.my_world = world
        self.balance = balance
        
        self.list_of_loan_offers = []
    
    
    def start_activities(self):
        pass
    
    
    def put_money(self, payee: Entity, amount_of_money: int) -> None:
        payee._balance += amount_of_money
    
    
    def get_money(self, payer: Entity, amount_of_money: int) -> None:
        if amount_of_money <= payer.get_balance():
            payer._balance -= amount_of_money
        else:
            print('Entity doesnt have enough money')
            raise ValueError('entity doesnt have enough money')
    
    def transaction(self, payer: Entity, payee: Entity, amount_of_money: int):
        try:
            self.get_money(payer, amount_of_money)
        except ValueError:
            print('the payer does not have enough money')
            return
        
        self.put_money(payee, amount_of_money)
        print(f'Transaction: "{payer.name}" paid to "{payee.name}" {amount_of_money}$')
        
    
    def trade_deal(self, buyer: Entity, product: Product):
        if not product.can_product_be_sold() :
            print(f'Product {product.name} is not for sale')
            return
        if buyer.get_balance() < product.get_price():
            print(f'Buyer {buyer.name} dont have enough money for deal')
            return
         
        self.transaction(
            payer=buyer, 
            payee=product.get_owner(), 
            amount_of_money=product.get_price())
        
        product._change_owner(buyer)
        print(f'Product "{product.name}" has been sold to Buyer "{buyer.name}"')
    
    
    def create_loan_offer(self):
        pass
   
    

class Entity:
    """Юридическое лицо, организация
    
    Имеет баланс
    Владеет имуществом
    """
    
    def __init__(
            self, 
            name, 
            world: World, 
            balance: int = 0):
        
        self.name = name
        self.my_world = world
        self.my_bank = world.bank
        self._balance = balance
        
        self._property_list = set()
    

    def get_balance(self) -> int:
        return self._balance
    
    def remove_property(self, property_: Product):
        self._property_list.remove(property_)
    
    def add_property(self, property_: Product):
        self._property_list.add(property_)
    
    def get_property_list(self) -> set:
        return self._property_list.copy()
    
    

class Government(Entity):
    """Правительство 
    
    Продает активы
    Штрафует
    Выделяет субсидии
    """
    
    
    def __init__(
            self, 
            name: str, 
            world: World,
            balance: int = 0):
        
        super().__init__(
            name = name, 
            world = world, 
            balance = balance)
        
        self.auction_list = []
    
    
    def start_activities(self):
        pass
    
    
    def add_auction(self):
        pass
    
    
    def add_asset_to_auction_list(self):
        pass
    


class Company(Entity):
    """компания = команда игроков
    """
    
    in_process_status = 'in_process'
    ready_status = 'ready'
    
    list_of_statuses = [in_process_status, ready_status]
    
    def __init__(
            self, 
            name: str, 
            world: World, 
            balance: int):
        
        super().__init__(
            name = name, 
            world = world,
            balance = balance)
        
        self.list_of_debts = set()
        self._company_status = Company.in_process_status # in_process, ready 
    
    
    def get_company_status(self):
        return self._company_status
    
    def can_make_changes(self) -> bool:
        if self.get_company_status() == Company.in_process_status:
            return True
        else:
            print(f'Company "{self.owner.name}" cant make changes now')
            return False
        
    def _change_company_status(self, new_status: str):
        if new_status in Company.list_of_statuses:
            self._company_status = new_status
        else:
            raise ValueError('wrong company_status')
    
    def confirm_actions(self):
        self._company_status = Company.ready_status
        print(f'Company "{self.name}" confirmed actions')
        self.my_world.next_round()
    
    
    def request_auction(self):
        pass
    
    
    def request_loan_offer(self):
        pass
    
    
    def take_loan(self):
        pass
    
    def buy(self, product: Product):
        if not self.can_make_changes: return
        
        try:
            self.my_bank.trade_deal(self, product)
        except:
            return
    
    def _collect_profit_from_assets(self):
        total_profit = 0
        asset_list = [p for p in self.get_property_list() if type(p) is Asset]
        for asset in asset_list:
            amount_of_profit = asset.get_balance()
            if amount_of_profit > 0:
                total_profit += amount_of_profit
                self.my_world.bank.transaction(
                    payer = asset, 
                    payee = self, 
                    amount_of_money = amount_of_profit)
        
        print(f'Company "{self.name}" made profit: {total_profit}$')
                
 
    def invest_money_to_asset(self):
        pass


class Region(Entity):
    """В регионах разные условия работы"""

    def __init__(
            self, 
            name: str, 
            world: World, 
            balance: int = 0,
            weather=None,
            coal_demand=None,
            income_tax=0.1,
            environmental_tax=None,
            average_coal_price=None):
        
        super().__init__(
            name = name, 
            world = world,
            balance = balance)
        
        self.income_tax = income_tax
        self.list_of_assets = set()
    
    
    def environmental_test(self):
        pass
    
    
    def add_labor_market(self):
        pass


class Product:
    """Все, что можно купить и продать
    
    Параметры:
        name: str
        world: World
        price: int - цена 
        quantity: Q_ - количество товара (2 тонны). None - 1шт 
        owner: Entity - текущий владелец
        status: str - "sale, not_for_sale" статус, продется или нет
    
    """
    
    sale_status = 'sale'
    not_for_sale_status = 'not_for_sale'
    
    list_of_statuses = [
        sale_status, 
        not_for_sale_status ]
    
    
    def __init__(
            self, 
            name: str, 
            world: World,
            owner: Entity,
            price: int = 0,
            quantity: Q_ = None,
            product_status: str = not_for_sale_status):
        
        self.name = name
        self.my_world = world
        self._price = price
        self.quantity = quantity
        self._owner = owner
        self._owner.add_property(self)
        self._product_status = product_status
    
    def can_owner_make_changes(self) -> bool:
        try:
            if self.owner.can_make_changes():
                return True
            else:
                print(f'Company {self.owner.name} cant make changes now')
                return False
        except:
            return False
    
    def get_price(self) -> int:
        return self._price
    
    def change_price(self, new_price: int):
        if not self.can_owner_make_changes(): return
        self._price = new_price
    
    def get_product_status(self):
        return self._product_status
    
    def change_product_status(self, new_status: str):
        if not self.can_owner_make_changes(): return
        
        if new_status in Product.list_of_statuses:
            self._product_status = new_status
            print(f'Product status has been changed to "{new_status}"')
        else:
            raise ValueError('wrong status')
    
    def get_owner(self) -> int:
        return self._owner
    
    def _change_owner(self, new_owner: Entity):
        self._owner.remove_property(self)
        self._owner = new_owner
        self._owner.add_property(self)
        self.change_product_status(Product.not_for_sale_status)
    
    def take_part(self, quantity: Q_ = None):
        if not self.can_owner_make_changes(): return
        pass
    
    def can_product_be_sold(self) -> bool:
        if self.get_product_status() == Product.sale_status:
            return True
        else:
            return False
        
    
    
class Asset(Product, Entity):
    """Актив
    
    и можно купить, и сам может покупать 
    """
    
    work_status = 'work'
    off_status = 'off'
    not_started_status = 'not_started'
    
    list_of_statuses = [work_status, off_status, not_started_status]
    
    def __init__(
            self, name: str, 
            region: Region, 
            balance: int = 0, 
            price: int = 0,
            initial_investment: int = 0):
        
        Product.__init__(
            self, 
            name = name,
            world = region.my_world,
            price = price,
            owner = region.my_world.government)
        
        Entity.__init__(
            self, 
            name = name, 
            world = region.my_world,
            balance = balance)
        
        self.initial_investment = initial_investment
        self.my_region = region
        self._asset_status = Asset.not_started_status

    
    def get_asset_status(self):
        return self._asset_status
    
    def change_asset_status(self, new_status: str):
        if new_status in Asset.list_of_statuses:
            self._asset_status = new_status
            print(f'Asset status has been changed to "{new_status}"')
        else:
            raise ValueError('wrong status')
    
    def start_asset(self):
        if not self.can_owner_make_changes(): return
        
        if self.get_asset_status() != Asset.not_started_status:
            print(f'Asset "{self.name}" is already started')
            return 
        try:
            self.my_bank.get_money(
                payer = self.get_owner(), 
                amount_of_money = self.initial_investment)
            
            print(f'Owner of asset "{self.name}" paid initial investment: {self.initial_investment}$')
            
            self.change_asset_status(Asset.work_status)
        except:
            print(f'Asset "{self.name}" failed to start ')
        
    
    def _make_money(self):
        profit = 5_000
        self.my_world.bank.put_money(
            payee = self, 
            amount_of_money = profit)
        print(f'Asset "{self.name}" made a profit: {profit}$')
        self._pay_income_tax(profit)
        print(f'Balance of asset "{self.name}": {self.get_balance()}$')
        
    
    def _pay_income_tax(self, profit):
        amount_of_income_tax = int(profit * self.my_region.income_tax)
        self.my_world.bank.transaction(
            payer = self, 
            payee = self.my_region, 
            amount_of_money = amount_of_income_tax)
        print(f'Asset "{self.name}" paid a income tax: {amount_of_income_tax}$')
    
    
    def invest_money(self, amount_of_money: int):
        if not self._can_owner_make_changes(): return
        pass
        
    
    
    

if __name__ == "__main__":
    
    world_parameters = {
        'name': 'Game_1',
        'regions':[
            {
                'name': 'North', 
                'balance': 10_000_000,
                'assets':[
                    {
                        'name': 'A', 
                        'balance': 0, 
                        'price': 70_000,
                        'initial_investment': 10_000},
                    {
                        'name': 'B', 
                        'balance': 0, 
                        'price': 45_000,
                        'initial_investment': 10_000}]
                },
            {
                'name': 'West_', 
                'balance': 30_000_000,
                'assets':[
                    {
                        'name': 'C', 
                        'balance': 0, 
                        'price': 20_000,
                        'initial_investment': 20_000}]
                }
            ]
        }

    Game_1 = Game()
    
    w = Game_1.create_world(world_parameters)
    
    print()
    
    assets = {}
    print('name    price status')
    for region in w.list_of_regions:
        for asset in region.list_of_assets:
            assets[asset.name] = asset
            print(asset.name, 
                  asset.my_region.name, 
                  asset.get_price(), 
                  asset.get_product_status())
        
    # print()
    # company_1 = w.add_company('RosPromMining', 100_000)
    # print()
    # assets['C'].change_product_status(Product.sale_status)

    
    # company_1.buy(assets['C'])
    
    # assets['C'].start_asset()
    
    # company_1.confirm_actions()
    
    # company_1.get_company_status()
    
    
    
    
    
    
    