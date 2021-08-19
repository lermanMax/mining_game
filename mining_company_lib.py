from __future__ import annotations
from pint import UnitRegistry
ureg = UnitRegistry()
Q_ = ureg.Quantity

# power = Q_(10, 'hour')
# p_1 = Q_(2, 'hour')
# print(power / p_1)
# if not power: print('ok')
# power.magnitude
# power.units

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
        self._current_round = 1
        self._current_year = 1
        self._hours_per_round = Q_(
            world_parameters['hours_per_round'], 'hour') #(24*28*3 = 2016)
        self._working_hours_per_round = Q_(
            world_parameters['working_hours_per_round'], 'hour') #(8*20*3 = 480)
        self._overtime_hours_per_round = Q_(
            world_parameters['overtime_hours_per_round'], 'hour') #(8*16 = 128)
        self._rounds_per_year = world_parameters['rounds_per_year'] #( 4 )
        self.list_of_companies = set()
        self.list_of_regions = set()
        self._list_of_autonomous_organizations = set()
        
        self.bank = Bank(name = 'Bank', world = self)
        self.government = Government(name = "Government", world = self)
        
        self._add_regions(world_parameters['regions'])
        
    
    def get_current_round(self) -> int:
        return self._current_round
    
    def get_current_year(self) -> int:
        return self._current_year
    
    def get_rounds_per_year(self) -> int:
        return self._rounds_per_year
    
    def get_working_hours_per_round(self) -> Q_:
        return self._working_hours_per_round
    
    def get_overtime_hours_per_round(self) -> Q_:
        return self._overtime_hours_per_round
    
    def add_autonomous_organization_in_list(
            self, new_organization: Autonomous_organization): 
        self._list_of_autonomous_organizations.add(new_organization)
    
    def get_list_of_autonomous_organizatons(self):
        return self._list_of_autonomous_organizations.copy()
    
    def add_company(self, name: str, balance: int) -> Company:
        new_company = Company(
            name=name, 
            world=self, 
            balance=balance)
        self.list_of_companies.add(new_company)
        print(f'Company "{new_company.get_name()}" was added')
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
            new_asset = Coal_mining_asset(
                name = asset['name'], 
                region = region,
                balance = asset['balance'], 
                price = asset['price'],
                initial_investment = asset['initial_investment'],
                estimated_coal_supply = Q_(asset['estimated_coal_supply'], 'ton')
                )
            
            region.add_asset(new_asset)
            
            
    def get_list_of_started_assets(self) -> set:
        started_list = set()
        for rigion in self.list_of_regions:
            list_ = rigion.get_list_of_started_assets()
            started_list.update(list_)
                    
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
        
        
        print(f'Round {self.get_current_round()} is finish')
        if self.get_current_round() % self.get_rounds_per_year() == 0:
            self._current_year += 1
            print(f'New year {self.get_current_year()} is start')
        self._current_round += 1 
        print(f'Round {self.get_current_round()} is start')
        
        #Все автономные организации начинают свою активность
        for organizaton in self.get_list_of_autonomous_organizatons():
            organizaton.start_activities()
        
        # Все компании снова получают доступ к изменениям
        self._open_access_for_companies()
            
    
    def _save_actions(self):
        pass
    
    
    def _open_access_for_companies(self):
        for company in self.list_of_companies:
            company._change_company_status(Company.in_process_status)


class Autonomous_organization:
    
    def __init__(self, world: World):
        self.my_world = world
        self.my_world.add_autonomous_organization_in_list(self)
        
    def start_activities(self):
        pass
    

class Bank(Autonomous_organization):
    """
    Управляет транзакциями
    Выдает кредиты
    """

    
    def __init__(
            self, 
            name: str, 
            world: World, 
            balance: int = 0):
        super().__init__(world)
        
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
        print(f'Transaction: "{payer.get_name()}" paid to "{payee.get_name()}" {amount_of_money}$')
        
    
    def trade_deal(self, buyer: Entity, product: Product):
        if not product.can_product_be_sold() :
            raise Exception(f'Product {product.get_name()} is not for sale')

        if buyer.get_balance() < product.get_cost():
            raise ValueError(
                f'Buyer {buyer.get_name()} dont have enough money for deal')
         
        self.transaction(
            payer=buyer, 
            payee=product.get_owner(), 
            amount_of_money=product.get_cost())
        
        product._change_owner(buyer)
        print(f'Product "{product.get_name()}" has been sold to Buyer "{buyer.get_name()}"')
    
    
    def create_loan_offer(self):
        pass
    

class Entity:
    """Юридическое лицо, организация
    
    Имеет баланс
    Владеет имуществом
    Включает в себя участников
    """
    
    def __init__(
            self, 
            name: str, 
            world: World, 
            balance: int = 0):
        
        self._name = name
        self.my_world = world
        self.my_bank = world.bank
        self._balance = balance
        
        self._property_list = set()
        self._list_of_participants = set()
    
    def get_name(self) -> str:
        return self._name

    def get_balance(self) -> int:
        return self._balance
    
    def remove_property(self, property_: Product):
        self._property_list.remove(property_)
    
    def add_property(self, property_: Product):
        self._property_list.add(property_)
    
    def get_property_list(self) -> set:
        return self._property_list.copy()
    
    def remove_participant(self, participant: Person):
        self._list_of_participants.remove(participant)
    
    def add_participant(self, participant: Person):
        self._list_of_participants.add(participant)
    
    def get_list_of_participants(self) -> set:
        return self._list_of_participants.copy()
    

class Government(Entity, Autonomous_organization):
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
        
        Entity.__init__(
            self,
            name = name, 
            world = world, 
            balance = balance)
        
        Autonomous_organization.__init__(
            self, world = world)
        
        
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
            print(f'Company "{self.get_owner().get_name()}" cant make changes now')
            return False
        
    def _change_company_status(self, new_status: str):
        if new_status in Company.list_of_statuses:
            self._company_status = new_status
        else:
            raise ValueError('wrong company_status')
    
    def confirm_actions(self):
        self._company_status = Company.ready_status
        print(f'Company "{self.get_name()}" confirmed actions')
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
        property_list = self.get_property_list()
        asset_list = [p for p in property_list if issubclass(type(p), Asset)]
        for asset in asset_list:
            amount_of_profit = asset.get_last_profit()
            if amount_of_profit > 0:
                total_profit += amount_of_profit
                self.my_world.bank.transaction(
                    payer = asset, 
                    payee = self, 
                    amount_of_money = amount_of_profit)
        
        print(f'Company "{self.get_name()}" made profit: {total_profit}$')
                
 
    def invest_money_to_asset(self):
        pass


class Region(Entity, Autonomous_organization):
    """В регионах разные условия работы
    """
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
        
        Entity.__init__(
            self,
            name = name, 
            world = world,
            balance = balance)
        
        Autonomous_organization.__init__(
            self, world = world)
        
        self.income_tax = income_tax
        self._list_of_assets = set()
        
        self.equipment_market = Equipment_market('Equipment_market', self)
        self.labor_market = Labor_market('Labor_market', self)
    
    def get_list_of_assets(self):
        return self._list_of_assets.copy()
    
    def get_list_of_started_assets(self) -> set:
        started_list = set()
        for asset in self.get_list_of_assets():
            if asset.get_asset_status() != Asset.not_started_status:
                started_list.add(asset)
                    
        return started_list
    
    def add_asset(self, asset: Asset):
        self._list_of_assets.add(asset)
        
    
    def start_activities(self):
        pass
    
    def environmental_test(self):
        pass
    
    
    def add_labor_market(self):
        pass


class Product:
    """Все, что можно купить или продать
    
    Параметры:
        name: str
        world: World
        price: int - цена за 1 единицу измерения
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
            quantity: Q_ = Q_(1, 'count'),
            product_status: str = not_for_sale_status):
        
        self._name = name
        self.my_world = world
        self._price = price
        self._quantity = quantity
        self._owner = owner
        self._owner.add_property(self)
        self._product_status = product_status
    
    def can_owner_make_changes(self) -> bool:
        if issubclass(type(self.get_owner()), Autonomous_organization): return True
        
        try:
            if self.get_owner().can_make_changes():
                return True
            else:
                print(f'Company {self.get_owner().get_name()} cant make changes now')
                return False
        except:
            return False
        
        
    def get_name(self) -> str:
        return self._name
    
    def get_price(self) -> int:
        """Цена за единицу измерения"""
        return self._price
    
    def get_cost(self) -> int:
        """Стоимость = цена * количество"""
        quantity = self.get_quantity().magnitude
        price = self.get_price()
        return round(price * quantity)
    
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
    
    def get_quantity(self) -> Q_:
        return self._quantity
    
    def _change_quantity(self, new_quantity: Q_):
        self._quantity = new_quantity
    
    def get_all_params(self) -> dict:
        return {
            'name': self.get_name(), 
            'world': self.my_world,
            'owner': self.get_owner(),
            'price': self.get_price(),
            'quantity': self.get_quantity(),
            'product_status': self.get_product_status()
            }
    
    def take_part(self, quantity: Q_):
        if not self.can_owner_make_changes(): return
        if quantity.units != self.get_quantity().units:
            raise ValueError('wrong units')
        if not quantity < self.get_quantity(): 
            raise ValueError('quantity too much')
        if quantity.magnitude == 0: 
            raise ValueError('quantity cant be 0')
        
        params = self.get_all_params()
        params['quantity'] = quantity
        self._change_quantity(self.get_quantity() - quantity)
        copy = type(self)(**params)
        return copy
    
    def can_product_be_sold(self) -> bool:
        return self.get_product_status() == Product.sale_status
            
        
    
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
        
        self._last_profit = 0

    def can_be_changed(self) -> bool:
        return self.get_asset_status() == Asset.work_status
        
    def get_asset_status(self):
        return self._asset_status
    
    def _change_asset_status(self, new_status: str):
        if new_status in Asset.list_of_statuses:
            self._asset_status = new_status
            print(f'Asset status has been changed to "{new_status}"')
        else:
            raise ValueError('wrong status')
    
    def get_last_profit(self) -> int:
        return self._last_profit
    
    def start_asset(self):
        if not self.can_owner_make_changes(): return
        
        if self.get_asset_status() != Asset.not_started_status:
            print(f'Asset "{self.get_name()}" is already started')
            return 
        try:
            self.my_bank.get_money(
                payer = self.get_owner(), 
                amount_of_money = self.initial_investment)
            
            print(f'Owner of asset "{self.get_name()}" paid initial investment: {self.initial_investment}$')
            
            self._change_asset_status(Asset.work_status)
        except:
            print(f'Asset "{self.get_name()}" failed to start ')
        
    
    def _make_money(self):
        profit = 5_000
        self.my_world.bank.put_money(
            payee = self, 
            amount_of_money = profit)
        self._save_profit(profit)
    
    
    def _save_profit(self, profit):
        print(f'Asset "{self.get_name()}" made a profit: {profit}$')
        amount_of_income_tax = self._pay_income_tax(profit)
        print(f'Balance of asset "{self.get_name()}": {self.get_balance()}$')
        self._last_profit = profit - amount_of_income_tax
        
    
    def _pay_income_tax(self, profit) -> int:
        """Подаходный налог"""
        if profit <= 0: return 0
        
        amount_of_income_tax = int(profit * self.my_region.income_tax)
        self.my_world.bank.transaction(
            payer = self, 
            payee = self.my_region, 
            amount_of_money = amount_of_income_tax)
        print(f'Asset "{self.get_name()}" paid a income tax: {amount_of_income_tax}$')
        return amount_of_income_tax
    
    
    def invest_money(self, amount_of_money: int):
        if not self.can_owner_make_changes(): return
        if not self.can_be_changed(): return
        try:
            self.my_bank.transaction(
                payer = self.get_owner(), 
                payee = self, 
                amount_of_money = amount_of_money)
            print(f'Balance "{self.get_name()}": {self.get_balance()}$')
        except:
            print('Money was not invested')
        pass


class Coal(Product):
    """Уголь """
    
    def __init__(
            self, 
            name: str, 
            world: World,
            owner: Entity,
            price: int,
            quantity: Q_,
            ):
        
        super().__init__(
            name = name,
            world = world,
            owner = owner,
            price = price,
            quantity = quantity,
            product_status = Product.sale_status)
    
    def get_all_params(self) -> dict:
        return {
            'name': self.get_name(), 
            'world': self.my_world,
            'owner': self.get_owner(),
            'price': self.get_price(),
            'quantity': self.get_quantity()
            }
        
        
    
class Mining_machine(Product):
    """Угле добывающая машина
    
    power: Q_(x, 'kg/hour') - мощность добычи
    manhours_for_service: Q_(x, 'hour') - необходимо человек-часов 
        для 1 часа работы оборудования
    year_of_release: int - год выпуска
    """
    
    def __init__(
            self, 
            name: str, 
            world: World,
            owner: Entity,
            price: int,
            quantity: Q_,
            power: Q_,
            manhours_for_service: Q_,
            year_of_release: int
            ):
        
        super().__init__(
            name = name,
            world = world,
            owner = owner,
            price = price,
            quantity = quantity,
            product_status = Product.sale_status)
        
        self._power = power
        self._manhours_for_service = manhours_for_service
        self._year_of_release = year_of_release
        
    def get_power(self) -> Q_:
        return self._power
    
    def get_number_of_manhours_for_service(self) -> Q_:
        return self._manhours_for_service
    
    def get_year_of_release(self) -> int:
        return self._year_of_release
    
    def get_all_params(self) -> dict:
        return {
            'name': self.get_name(), 
            'world': self.my_world,
            'owner': self.get_owner(),
            'price': self.get_price(),
            'quantity': self.get_quantity(),
            'power': self.get_power(),
            'manhours_for_service': self.get_number_of_manhours_for_service(),
            'year_of_release': self.get_year_of_release()
            }


class Preparation_line(Product):
    """Обогатительная линия
    
    power: Q_(x, 'kg/hour') - мощность обогащения
    manhours_for_service: Q_(x, 'hour') - необходимо человек-часов 
        для 1 часа работы оборудования
    year_of_release: int - год выпуска
    """
    
    def __init__(
            self, 
            name: str, 
            world: World,
            owner: Entity,
            price: int,
            quantity: Q_,
            power: Q_,
            manhours_for_service: Q_,
            year_of_release: int
            ):
        
        super().__init__(
            name = name,
            world = world,
            owner = owner,
            price = price,
            quantity = quantity,
            product_status = Product.sale_status)
        
        self._power = power
        self._manhours_for_service = manhours_for_service
        self._year_of_release = year_of_release
        
    def get_power(self) -> Q_:
        return self._power
    
    def get_number_of_manhours_for_service(self) -> int:
        return self._manhours_for_service
    
    def get_year_of_release(self) -> int:
        return self._year_of_release
    
    def get_all_params(self) -> dict:
        return {
            'name': self.get_name(), 
            'world': self.my_world,
            'owner': self.get_owner(),
            'price': self.get_price(),
            'quantity': self.get_quantity(),
            'power': self.get_power(),
            'manhours_for_service': self.get_number_of_manhours_for_service(),
            'year_of_release': self.get_year_of_release()
            }
    

class Equipment_market(Entity, Autonomous_organization):
    """Рынок оборудования
    
    """
    def __init__(
            self, 
            name: str, 
            region: Region,
            balance: int = 0):
        
        Entity.__init__(
            self,
            name = name, 
            world = region.my_world, 
            balance = balance)
        Autonomous_organization.__init__(
            self, world=region.my_world)
        
        self.my_region = region
    
    def features_of_mining_equipment(self) -> dict:
        features_of_equipment  = {
            'Mining_equipment_class_C': {
                'power': Q_(50, 'kg/hour'),
                'manhours_for_service': Q_(2, 'hour'),
                'price': 14_000,
                'quantity': Q_(5, 'count')},
            'Mining_equipment_class_B': {
                'power': Q_(100, 'kg/hour'),
                'manhours_for_service': Q_(3, 'hour'),
                'price': 28_000,
                'quantity': Q_(3, 'count')},
            'Mining_equipment_class_A': {
                'power': Q_(200, 'kg/hour'),
                'manhours_for_service': Q_(2, 'hour'),
                'price': 70_000,
                'quantity': Q_(1, 'count')}
            }
        return features_of_equipment
    
    def features_of_preparation_equipment(self) -> dict:
        features_of_equipment  = {
            'Preparation_line': {
                'power': Q_(2500, 'kg/hour'),
                'manhours_for_service': Q_(20, 'hour'),
                'price': 60_000,
                'quantity': Q_(1, 'count')}
            }
        return features_of_equipment
    
    def start_activities(self):
        for name, features in self.features_of_mining_equipment().items():
            Mining_machine(
                name = name, 
                world = self.my_world, 
                owner = self, 
                price = features['price'], 
                quantity = features['quantity'], 
                power = features['power'], 
                manhours_for_service = features['manhours_for_service'], 
                year_of_release = self.my_world.get_current_year())
        
        for name, features in self.features_of_preparation_equipment().items():
            Preparation_line(
                name = name, 
                world = self.my_world, 
                owner = self, 
                price = features['price'], 
                quantity = features['quantity'], 
                power = features['power'], 
                manhours_for_service = features['manhours_for_service'], 
                year_of_release = self.my_world.get_current_year())
            
    
    def _amount_of_equipment(self) -> dict:
        """Сколько оборудовния имеется сейчас
        {
            'name': Q_(1, 'count')
            }
        """
        result = {}
        for equipment in self.get_property_list():
            name = equipment.get_name() 
            if name in result:
                result[name] += equipment.get_quantity()
            else:
                result[name] = equipment.get_quantity()
                    
        return result
    
    def amount_of_equipment_available_for_sale(self) -> dict:
        """Cколько готовы продать одному активу
        {
            'name': Q_(1, 'count')
            }
        """
        amount_of_assets = len(self.my_region.get_list_of_started_assets())
        result = {}
        for name, amount_of_equipment in self._amount_of_equipment().items():
            amount = amount_of_equipment//amount_of_assets
            if amount == 0: next 
            result[name] = Q_(amount.magnitude, amount_of_equipment.units) 
        return result
        
    
    def get_list_of_equipment_for_sale(
            self, purchase_name: str, amount: Q_) -> set:
        """Получить список оборудования, которое покупатель хочет купить. 
        Выдает объекты - оборудование, по списку наименований. 
        """
        result = set()
        how_much_more_is_needed = amount
        
        for equipment in self.get_property_list():
            if equipment.get_name() == purchase_name:
                quantity = equipment.get_quantity()
                if quantity <= how_much_more_is_needed:
                    result.add(equipment)
                    how_much_more_is_needed -= quantity
                else:
                    part_equip = equipment.take_part(how_much_more_is_needed)
                    result.add(part_equip)
                    break
                
                if not how_much_more_is_needed: break
        
        return result


class Person:
    
    vocation_education = 'vocation_education'
    higher_education = 'higher_education'
    list_of_types_of_education = (vocation_education, higher_education)
    
    mining_profession = 'miner'
    preparation_profession = 'line_worker' 
    manager_profession = 'manager'
    list_of_types_of_profession = (
            mining_profession,
            preparation_profession,
            manager_profession)
    
    def __init__(
            self,
            name: str,
            region: Region,
            organization: Entity):
        
        self._name = name
        self._place_of_birth = region
        self._place_of_residence = region
        self._age = 20
        
        self._work_experience = {}
        """
        _work_experience = {
                profession_name:{
                    'years_of_experience': 0,
                    'qualification': 0,
                    'education': ''
                    },
                
                }
        """
        self._my_organization = organization 
        
    def get_name(self):
        return self._name
    
    def change_organization(self, new_organization: Entity):
        self._my_organization.remove_participant(self)
        self._my_organization = new_organization
        self._my_organization.add_participant(self)
    
    def get_work_experience(self, profession_name: str):
        if not profession_name in self._work_experience:
            return None
        return self._work_experience[profession_name].copy()
    
    def add_work_experience(
            self, 
            profession_name: str, 
            new_years_of_experience: float = 0,
            new_poins_in_qualification: float = 0,
            education: str = ''):
        if not profession_name in Person.list_of_types_of_profession:
            raise ValueError(f'profession_name "{profession_name}" not exist')
        if not education in Person.list_of_types_of_education:
            raise ValueError(f'education "{education}" not exist')
        if not profession_name in self._work_experience:
            dict_of_exp = {
                    'years_of_experience': 0,
                    'qualification': 0,
                    'education': ''}
            self._work_experience[profession_name] = dict_of_exp
        
        self._work_experience[profession_name]['years_of_experience'] += (
                new_years_of_experience)
        self._work_experience[profession_name]['qualification'] += (
                new_poins_in_qualification)
        self._work_experience[profession_name]['education'] = education
    
    def change_organization(self, new_organization: Entity):
        self._my_organization.remove_participant(self)
        self._my_organization = new_organization
        self._my_organization.add_participant(self)
            
        

class Labor_market(Entity, Autonomous_organization):
    """Рынок труда
    
    """
    def __init__(
            self, 
            name: str, 
            region: Region,
            balance: int = 0):
        
        Entity.__init__(
            self,
            name = name, 
            world = region.my_world, 
            balance = balance)
        Autonomous_organization.__init__(
            self, world=region.my_world)
        
        self.my_region = region
        
    
    def features_of_new_persons(self) -> dict:
        features  = {
            Person.mining_profession: {
                'qualification': 0.5,
                'education': Person.vocation_education,
                'quantity': Q_(20, 'count')
                },
            Person.preparation_profession: {
                'qualification': 0.5,
                'education': Person.vocation_education,
                'quantity': Q_(20, 'count')
                },
            Person.manager_profession: {
                'qualification': 0.5,
                'education': Person.higher_education,
                'quantity': Q_(5, 'count')
                },
            
            }
        return features
    
    def start_activities(self):
        for profession_name, features in self.features_of_new_persons().items():
            quantity = features['quantity'].magnitude
            for _ in range(quantity):
                new_person = Person(
                        name='Ivan', 
                        region=self.my_region, 
                        organization=self)
                new_person.add_work_experience(
                        profession_name=profession_name,
                        new_poins_in_qualification=features['qualification'],
                        education=features['education'])
        
    
    def _number_of_candidates(self) -> dict:
        """Сколько человек ищут работу
        {
            'profession_name': Q_(1, 'count')
            }
        
        Если у человека есть опыт в нескольких проффессиях, 
        то он будет добавлен в списки по всем 
        """
        result = {}
        for profession in Person.list_of_types_of_profession:
            result[profession] = Q_(0,'count')
            
        for person in self.get_list_of_participants():
            for profession in Person.list_of_types_of_profession:
                if not person.get_work_experience(profession): 
                    next
                else:
                    result[profession] += Q_(1, 'count')           
        return result
    
    
    def number_of_candidates_available_for_hire(self) -> dict:
        """Cколько человек готовы идти в одну компанию
        {
            'name': Q_(1, 'count')
            }
        """
        amount_of_assets = len(self.my_region.get_list_of_started_assets())
        result = {}
        for name, number_of_candidates in self._number_of_candidates().items():
            number = number_of_candidates//amount_of_assets
            if number == 0: next 
            result[name] = Q_(number.magnitude, number_of_candidates.units) 
        return result
    
    
    def get_list_of_candidates_for_hiring(
            self, 
            profession_name: str, 
            number: Q_) -> set:
    
        result = set()
        how_much_more_is_needed = number
        
        for person in self.get_list_of_participants():
            if not person.get_work_experience(profession_name): 
                next
            else:
                result.add(person)
                how_much_more_is_needed -= Q_(1,'count')
                if how_much_more_is_needed == Q_(0,'count'):
                    break
        
        return result
                
        
    
                
            
class Coal_mining_asset(Asset):
    """ Угледобывающий актив
    
    estimated_coal_supply: Q_ количество угля в месторождении 
    """
    
    
    def __init__(
            self, name: str, 
            region: Region, 
            balance: int = 0, 
            price: int = 0,
            initial_investment: int = 0,
            estimated_coal_supply: Q_ = Q_(0, 'ton'),
            ):
        
        super().__init__(
            name=name, 
            region=region, 
            balance=balance , 
            price=price,
            initial_investment=initial_investment)
        
        self._estimated_coal_supply = estimated_coal_supply
        self._mined_for_all_time = Q_(0,'ton')
        
        self.coal_mining = Coal_mining(self)
        self.coal_preparation = Coal_preparation(self)
        self.equipment_fleet = Equipment_fleet(self)
        self.staff = Staff(self)
        self.managers = Specialists(self)
        self.hr = HR(self)
        self.werehouse = Werehouse(self)
        self.transport_infrastructure = Transport_infrastructure(self)
        self.sales_department = Sales_department(self)
        
        self._amount_of_coal_that_can_be_sold = None
    
    
    def _make_money(self):
        #закупка
        purchase_costs = self._purchase()
        
        #работа актива 
        amount_of_coal_that_was_delivered = self.asset_work()
        
        #выручка 
        proceeds = self._proceeds(amount_of_coal_that_was_delivered)
        
        #расходы
        costs = self._costs(purchase_costs) 
        
        
        #прибыль
        profit = proceeds - costs
        self._save_profit(profit)    
    
    
    def _proceeds(self, amount_of_coal_that_was_delivered: Q_) -> int:
        """Выручка"""
        new_coal_price = self.get_coal_price()
        for coal in self.get_coal_list():
            coal.change_price(new_coal_price)
            
        proceeds_from_coal = self._sell_coal(amount_of_coal_that_was_delivered)
        proceeds_from_sale_of_equipment = self.equipment_fleet.sale_of_equipment()
        
        return proceeds_from_coal + proceeds_from_sale_of_equipment

    
    def _costs(self, purchase_costs: dict) -> int:
        """Расходы"""
        costs = 0
        for name, amount in purchase_costs.items():
            print(f'Costs of "{name}": {amount}$')
            costs += amount
        
        return costs
    
    def _purchase(self) -> dict:
        """Закупки для всех отделов актива
        
        purchase_costs = {
            'name': 10
            }
        """
        purchase_costs = {}
        purchase_costs['equipment_fleet'] = self.equipment_fleet._purchase()
        
        return purchase_costs
    
    def coal_deposit_reserves(self) -> Q_:
        """Запасы месторождения"""
        coal_supply = self._estimated_coal_supply
        additional_coal_supply = 0
        
        coal_supply = coal_supply * (1+additional_coal_supply)
        mined_for_all_time = self._mined_for_all_time
        
        return coal_supply - mined_for_all_time
    
    def set_amount_of_coal_that_can_be_sold(self, amount: Q_):
        pass
    
    def get_amount_of_coal_that_can_be_sold(self):
        if not self._amount_of_coal_that_can_be_sold: 
            return self.sales_department.capacity()
        else:
            return self._amount_of_coal_that_can_be_sold
    
    
    def get_coal_price(self) -> int:
        return 47
    
    def _add_coal(self, amount: Q_):
        if amount.magnitude == 0: return
        
        self._mined_for_all_time -= amount
        Coal(
            name = f'Coal_from_{self.get_name()}', 
            world = self.my_world, 
            owner = self, 
            price = self.get_coal_price(), 
            quantity = amount)
    
    def get_coal_list(self) -> set:
        result = set()
        
        for property_ in self.get_property_list():
            if type(property_) is Coal:
                result.add(property_)
        return result
        
    def _sell_coal(self, amount: Q_) -> int:
        list_for_sale = set()
        how_much_more_is_needed = amount

        for coal in self.get_coal_list():
            quantity = coal.get_quantity()
            if quantity <= how_much_more_is_needed:
                list_for_sale.add(coal)
                how_much_more_is_needed -= quantity
            else:
                part_coal = coal.take_part(how_much_more_is_needed)
                list_for_sale.add(part_coal)
                break
                
            if not how_much_more_is_needed: break
        
        proceed_from_coal = 0
        for item in list_for_sale:
            proceed_from_coal += item.get_cost()
            self.my_bank.trade_deal(
                buyer = self.my_region, 
                product = item)
            
        return proceed_from_coal
        
        
    def asset_work(self) -> Q_:  
        """работа актива
        
        возвращает количество доставленного угля Q_(10, 'ton')
        """
        mining_capacity = self.coal_mining.capacity()
        preparation_capacity = self.coal_preparation.capacity()
        downtime = 0.01
        useful_raw_material_ratio = 0.99
        coal_deposit_reserves = self.coal_deposit_reserves()
        
        #мощность производства по узкому месту
        production_capacity = min(mining_capacity, preparation_capacity)
        #мощность производства с учетом простоев
        production_capacity = production_capacity * (1-downtime)
        #мощность производства с учетом коэфийиента полезного сырья
        production_capacity = production_capacity * useful_raw_material_ratio
        #мощность производства с учетом запасов месторождения
        production_capacity = min(production_capacity, coal_deposit_reserves)
        
        amount_of_coal_in_werehouse = self.werehouse.amount_of_coal()
        free_werehouse_capacity = self.werehouse.free_capacity()
        transport_infrastructure_capacity = self.transport_infrastructure.capacity()
        amount_of_coal_that_can_be_sold = self.get_amount_of_coal_that_can_be_sold()
        
        #узкое место в транспорте и продажах
        delivery_capacity = min(
            transport_infrastructure_capacity, 
            amount_of_coal_that_can_be_sold)
        #предел для производства(добычи-обагощения)
        limit_for_production = delivery_capacity + free_werehouse_capacity
        
        #удалось добыть угля
        amount_of_coal_that_was_mined = min(
            production_capacity, limit_for_production)
        print(f'Asset "{self.get_name()}" produced coal: {amount_of_coal_that_was_mined} ')
        self._add_coal(amount_of_coal_that_was_mined)
        #Всего угля в наличии
        amount_of_coal_available = (
            amount_of_coal_that_was_mined + amount_of_coal_in_werehouse)
        #удалось проадть и доставить
        amount_of_coal_that_was_delivered = min(
            delivery_capacity, amount_of_coal_available)
        return amount_of_coal_that_was_delivered
        
        

class Coal_mining:
    
    def __init__(self, my_asset: Coal_mining_asset):
        self.my_asset = my_asset
    
    
    def capacity(self) -> Q_:
        """Мощность добычи угля 
        Q_(0,'ton')
        """
        working_hours = self.my_asset.my_world.get_working_hours_per_round()
        # overtime_hours = self.my_asset.my_world.get_overtime_hours_per_round()
        
        equipment_fleet = self.my_asset.equipment_fleet
        mining_equipment = equipment_fleet.get_list_of_mining_equipment()
        
        #потенциальная мощность добычи
        potential_capacity = Q_(0,'ton')
        # необходимо человекочасов для обеспечения максимальной мощности
        required_number_of_manhours = Q_(0.01,'hour')
        
        for machine in mining_equipment:
            quantity = machine.get_quantity().magnitude
            capacity = machine.get_power() * working_hours #ton/hour * hour
            potential_capacity += capacity * quantity 
            
            manhours = machine.get_number_of_manhours_for_service().magnitude
            required_number_of_manhours += manhours * working_hours * quantity
        
        #доступно человекочасов
        available_manhours=self.my_asset.staff.get_number_of_manhours_for_mining()
        #доступно человекочасов с учтетом сверхурочки
        #доступно человекочасов с учетом травм
        
        percentage_of_equipment_use = min(1,
            available_manhours.magnitude
            /required_number_of_manhours.magnitude)
        
        #мощность добычи с учетом наличия персонала
        capacity = potential_capacity * percentage_of_equipment_use
        # мощность добычи с учетом простоев из-за погоды
        # capacity = capacity * (1- )
            
        return capacity
    
    def set_amount_of_overtime(self):
        """Сверхурочная работа"""
        if not self.my_asset.can_owner_make_changes(): return
        if not self.my_asset.can_be_changed(): return
        pass
    
    def overtime_options(self):
        """Варианты сверхурочной работы"""
        pass
    

class Coal_preparation:
    
    def __init__(self, my_asset: Coal_mining_asset):
        self.my_asset = my_asset
    
    
    def capacity(self):
        """Мощность обогащения угля"""
        working_hours = self.my_asset.my_world.get_working_hours_per_round()
        # overtime_hours = self.my_asset.my_world.get_overtime_hours_per_round()
        
        equipment_fleet = self.my_asset.equipment_fleet
        mining_equipment = equipment_fleet.get_list_of_preparation_equipment()
        
        #потенциальная мощность
        potential_capacity = Q_(0,'ton')
        # необходимо человекочасов для обеспечения максимальной мощности
        required_number_of_manhours = Q_(0.01,'hour')
        # эффект увеличени мощности е
        power_increase_effect = 1
        
        for line in mining_equipment:
            quantity = line.get_quantity().magnitude
            capacity = line.get_power() * working_hours * power_increase_effect
            potential_capacity += capacity * quantity 
            
            manhours = line.get_number_of_manhours_for_service().magnitude
            required_number_of_manhours += manhours * working_hours * quantity
        
        #доступно человекочасов
        available_manhours=self.my_asset.staff.get_number_of_manhours_for_preparation()
        #доступно человекочасов с учтетом сверхурочки
        #доступно человекочасов с учетом травм
        
        percentage_of_equipment_use = min(1,
            available_manhours.magnitude
            /required_number_of_manhours.magnitude)
        
        #мощность добычи с учетом наличия персонала
        capacity = potential_capacity * percentage_of_equipment_use
            
        return capacity
    
    def set_amount_of_overtime(self):
        """Сверхурочная работа"""
        if not self.my_asset.can_owner_make_changes(): return
        if not self.my_asset.can_be_changed(): return
        pass
    
    def overtime_options(self):
        """Варианты сверхурочной работы"""
        pass
   


class Equipment_fleet:
    
    def __init__(self, my_asset: Coal_mining_asset):
        self.my_asset = my_asset
        
        self._target_amount_of_equipment = {
            'Mining_equipment_class_C': Q_(0,'count'),
            'Mining_equipment_class_B': Q_(0,'count'),
            'Mining_equipment_class_A': Q_(0,'count'), 
            'Preparation_line': Q_(0,'count')
            }
    
    
    def get_list_of_mining_equipment(self) -> set:
        list_of_mining_equipment = set()
        for product in self.my_asset.get_property_list():
            if type(product) is Mining_machine:
                list_of_mining_equipment.add(product)
                
        return list_of_mining_equipment
    
    def get_list_of_preparation_equipment(self) -> set:
        list_of_preparation_equipment = set()
        for product in self.my_asset.get_property_list():
            if type(product) is Preparation_line:
                list_of_preparation_equipment.add(product)
                
        return list_of_preparation_equipment
    
    
    def get_amount_of_equipment(self) -> dict:
        """Количество оборудования"""
        result = {}
        all_equipment = set()
        all_equipment.update(self.get_list_of_mining_equipment())
        all_equipment.update(self.get_list_of_preparation_equipment())
        for equipment in all_equipment:
            name = equipment.get_name()
            if name in result:
                result[name] += equipment.get_quantity()
            else:
                result[name] = equipment.get_quantity()
                
        return result
    
    
    def get_target_amount_of_equipment(self) -> dict:
        return self._target_amount_of_equipment.copy()
    
    
    def limiting_target_amount_of_equipment(self) -> dict:
        """Ограничение для целевого числа оборудования"""
        result = {}
        
        available_for_buy = self.amount_of_equipment_available_for_buy()
        amount_of_equipment = self.get_amount_of_equipment()
        
        set_of_names = set() 
        set_of_names.update(
            set(amount_of_equipment),
            set(available_for_buy))
        
        for name in set_of_names:
            limit_dict = {'min_limit': Q_(0,'count')}
            if (name in amount_of_equipment
                and name in available_for_buy):
                limit_dict['max_limit'] = (available_for_buy[name]
                                           + amount_of_equipment[name])
            elif name in available_for_buy:
                limit_dict['max_limit'] = available_for_buy[name]
            else:
                limit_dict['max_limit'] = amount_of_equipment[name]
            result[name] = limit_dict
        return result
    
    
    def set_target_amount_of_equipment(self, target_amount: dict):
        """Целевое количество оборудования
        
        target_amount ={
            'name': Q_(1, 'count')
            }
        """
        if not self.my_asset.can_owner_make_changes(): return
        if not self.my_asset.can_be_changed(): return
        
        limit = self.limiting_target_amount_of_equipment()
        try:
            for name, amount in target_amount.items():
                if not (limit[name]['max_limit'] 
                        >= amount 
                        >= limit[name]['min_limit']):
                    raise ValueError(
                        'target_amount_of_equipment out of limits')
        except:
            return
        
        for name, amount in target_amount.items():
            self._target_amount_of_equipment[name] = amount
    
    
    def additional_amount_of_equipment_for_buy(self) -> dict:
        """Дополнительное оборудование для покупки"""
        result = {
            'Mining_equipment_class_C': Q_(0, 'count'),
            'Mining_equipment_class_B': Q_(0, 'count'),
            'Mining_equipment_class_A': Q_(0, 'count')}
        return result
        
    
    def amount_of_equipment_available_for_buy(self) -> dict:
        """Количество оборудования доступного для покупки"""
        my_market = self.my_asset.my_region.equipment_market
            
        on_market = my_market.amount_of_equipment_available_for_sale()
        additional = self.additional_amount_of_equipment_for_buy()
        
        result = {}
        for equip_dict in [on_market, additional]:
            for name, amount in equip_dict.items():
                if name in result:
                    result[name] += amount
                else:
                    result[name] = amount
                    
        return result
    
    
    def list_of_equipment_need_to_buy(self) -> dict:
        """Список покупок
        
        list_to_buy = {
            'name': Q_(1, 'count')
            }
        """
        list_to_buy = {}
        
        amount_of_equipment = self.get_amount_of_equipment()
        for name,target_amount in self.get_target_amount_of_equipment().items():
            if name in amount_of_equipment:
                amount_of_that_equipment = amount_of_equipment[name]
            else:
                amount_of_that_equipment = Q_(0, 'count')
                
            difference = target_amount - amount_of_that_equipment
            if difference > Q_(0,'count'): 
                list_to_buy[name] = difference
                
        return list_to_buy
    
    def list_of_equipment_need_to_sale(self) -> dict:
        """Список на продажу
        
        list_to_sale = {
            'name': Q_(1, 'count')
            }
        """
        list_to_sale = {}
        
        amount_of_equipment = self.get_amount_of_equipment()
        for name, target_amount in self.get_target_amount_of_equipment():
            if name in amount_of_equipment:
                difference = target_amount - amount_of_equipment[name]
                list_to_sale[name] = min(difference, 0) * -1
            else:
                list_to_sale[name] = target_amount
        
        return list_to_sale
    
    def _purchase(self) -> int:
        """Закупка оборудования
        
        Возвращает сумму затрат на закупку (purchase_costs)
        """
        market = self.my_asset.my_region.equipment_market
        purchase_costs = 0
        for name, amount in self.list_of_equipment_need_to_buy().items():
            shopping_list = market.get_list_of_equipment_for_sale(
                purchase_name = name, 
                amount = amount)
            for position in shopping_list:
                try:
                    self.my_asset.my_bank.trade_deal(
                        buyer = self.my_asset, 
                        product = position)
                    purchase_costs += position.get_cost()
                except:
                    print(f'"{position.get_name()}" was not bought ')
                
        return purchase_costs
    
    def sale_of_equipment(self) -> int:
        """Продажа техники
        Возвращает велечину выручки с продаж
        """
        return 0


class Werehouse:
    
    def __init__(self, my_asset: Coal_mining_asset):
        self.my_asset = my_asset
    
    def amount_of_coal(self) -> Q_:
        coal_list = self.my_asset.get_coal_list()
        amount = Q_(0,'ton')
        for coal in coal_list:
            amount += coal.get_quantity()
        return amount
        
    def free_capacity(self) -> Q_:
        return Q_(100_000,'ton')

class Transport_infrastructure:
    
    def __init__(self, my_asset: Coal_mining_asset):
        self.my_asset = my_asset
    
    def capacity(self) -> Q_:
        return Q_(100_000, 'ton')


class Sales_department:
    
    def __init__(self, my_asset: Coal_mining_asset):
        self.my_asset = my_asset
    
    def capacity(self) -> Q_:
        return Q_(200_000, 'ton')


class Specialists:
    
    def __init__(self, my_asset: Coal_mining_asset):
        self.my_asset = my_asset
    
    
    def qualifications() -> dict:
        """ """
        pass
    
    def number_of_staff() -> dict:
        """ """
        pass
    
    def increasing_efficiency_of_managers(self):
        """Повышение эффективности менеджеров"""
        if not self.my_asset.can_owner_make_changes(): return
        pass
    
    def downtime_due_to_management_errors(self):
        """Простоии из за ошибок управления"""
        pass
    
    def set_target_number_of_specialists(self):
        """ """
        if not self.my_asset.can_owner_make_changes(): return
        pass
    
    def limiting_target_number_of_specialist(self) -> dict:
        """ """
        pass
    
    def change_working_conditions_for_specialists(self):
        """ """
        if not self.my_asset.can_owner_make_changes(): return
        pass
    
    def working_conditions_for_specialist(self):
        """ """
        pass



class Staff:
    
    base_wc = 'base'
    medium_wc = 'medium'
    comfort_wc = 'comfort'
    
    dict_of_working_conditions_factor = {
        base_wc: 0.15,
        medium_wc: 0.07,
        comfort_wc: 0.03}
    
    dict_of_working_conditions_price = {
        base_wc: 10,
        medium_wc: 20,
        comfort_wc: 35}
    
    def __init__(self, my_asset: Coal_mining_asset):
        self.my_asset = my_asset
        
        self._number_of_staff = {
            'mining_staff': Q_(0, 'count'),
            'preparation_staff': Q_(0, 'count')}
        
        self._qualification_of_staff = {
            'mining_staff': 0.5,
            'preparation_staff': 0.5}
        
        self._target_number_of_staff = {}
        
        self._working_conditions = Staff.base_wc
        self._working_conditions_of_last_round = Staff.base_wc 
        
    
    def qualifications(self) -> dict:
        """ """
        return self._qualification_of_staff.copy()
    
    def get_number_of_staff(self) -> dict:
        """ """
        return self._namber_of_staff.copy()
    
    def get_number_of_manhours_for_mining(self) -> Q_:
        working_hours = self.my_asset.my_world.get_working_hours_per_round()
        number_of_staff = self._number_of_staff['mining_staff'].magnitude
        return number_of_staff * working_hours 
    
    def get_number_of_manhours_for_preparation(self) -> Q_:
        working_hours = self.my_asset.my_world.get_working_hours_per_round()
        number_of_staff = self._number_of_staff['preparation_staff'].magnitude 
        return number_of_staff * working_hours 
    
    def end_of_round_actions(self):
        """Действия в конце раунда, перед началом следующего
        
        1. Убыль персонала
        """
        wc = self._working_conditions
        factor = Staff.dict_of_working_conditions_factor[wc]
        for name, number in self._number_of_staff.items():
            loss = round(number * factor)
            self._number_of_staff[name] = max(number - loss,0)
        
    
    def downtime_due_to_staff_errors(self):
        """"""
        pass
        
    
    def set_target_number_of_staff(self, target_number: dict):
        """ Установить целевое число персонала
        
        target_nambers ={
            'name': Q_(1, 'count')
            }
        """
        if not self.my_asset.can_owner_make_changes(): return
        if not self.my_asset.can_be_changed(): return
        
        limit = self.limiting_target_number_of_staff()
        try:
            for name, amount in target_number.items():
                if not (limit[name]['max_limit'] 
                        >= amount 
                        >= limit[name]['min_limit']):
                    raise ValueError(
                        'target_number_of_staff out of limits')
        except:
            return
        
        for name, amount in target_number.items():
            self._target_namber_of_staff[name] = amount
    
    
    def limiting_target_number_of_staff(self) -> dict:
        """ """
        result = {}
        
        hr = self.my_asset.hr
        
        available_for_hiring = hr.number_of_staff_available_for_hiring()
        number_of_staff = self.get_number_of_staff()
        
        set_of_names = set() 
        set_of_names.update(
            set(available_for_hiring),
            set(number_of_staff))
        
        for name in set_of_names:
            limit_dict = {'min_limit': Q_(0,'count')}
            if (name in number_of_staff
                and name in available_for_hiring):
                limit_dict['max_limit'] = (available_for_hiring[name]
                                           + number_of_staff[name])
            elif name in available_for_hiring:
                limit_dict['max_limit'] = available_for_hiring[name]
            else:
                limit_dict['max_limit'] = number_of_staff[name]
            result[name] = limit_dict
        return result
    
    
    def set_working_conditions(self, new_wc: str):
        """Установить уровень условий труда"""
        if not self.my_asset.can_owner_make_changes(): return
        if not self.my_asset.can_be_changed(): return
        if not new_wc in Staff.dict_of_working_conditions_factor: return
        self._working_conditions = new_wc
    
    def _purchase(self) -> int:
        """Затраты на условия труда"""
        full_number_of_staff = Q_(0,'count')
        for name, number in self.get_number_of_staff.items():
            full_number_of_staff += number
        
        wc_price = Staff.dict_of_working_conditions_price[self._working_conditions]
        wc_costs = full_number_of_staff.magnitude * wc_price
        self.my_asset.my_bank.transaction(
                payer = self.my_asset,
                payee = self.my_asset.my_region,
                amount_of_money = wc_costs)
        
        return wc_costs
    
    
    def hiring(self):
        
        hr = self.my_asset.hr
        number_of_staff = self.get_number_of_staff()
        for name, target_num in self._target_number_of_staff.items():
            if target_num > number_of_staff[name]:
                hr.hiring()
                
                
        
        
        
    

class HR:
    
    def __init__(self, my_asset: Coal_mining_asset):
        self.my_asset = my_asset
    
    
    def number_of_specialists_available_for_hiring():
        """ """
        
        pass
    
    def number_of_staff_available_for_hiring(self):
        """ """
        market = self.my_asset.my_region.labor_market
        staff = market.number_of_candidates_available_for_hire()
        return staff
    
    def hiring(self, name: str, number: Q_):
        """Найм персонала и специалистов
        
        Вычитает людей с рынка труда и добавляет в актив 
        """
        
    

