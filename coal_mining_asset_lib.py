from mining_company_lib import (
    World, Entity, Region, Government, Bank, Q_, Asset)


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
            estimated_coal_supply: Q_ = 0,
            ):
        
        super().__init__(
            name=name, 
            region=region, 
            balance=balance , 
            price=price,
            initial_investment=initial_investment)
        
        self.estimated_coal_supply = estimated_coal_supply
    
    
    def _make_money(self):
        pass
    
    
    def proceeds() -> int:
        """Выручка"""
        pass

    
    def costs() -> int:
        """Расходы"""
        pass
    
    
    def coal_deposit_reserves() -> Q_:
        """Запасы месторождения"""
        pass
    
    
    def asset_work():
        pass


class Coal_mining:
    
    def __init__(self, my_asset: Coal_mining_asset):
        self.my_asset = my_asset
    
    
    def coal_mining_capacity(self):
        """Мощность добычи угля"""
        pass
    
    def set_amount_of_overtime(self):
        """Сверхурочная работа"""
        if not self.my_asset.can_owner_make_changes(): return
        pass
    
    def overtime_options(self):
        """Варианты сверхурочной работы"""
        pass
    

class Coal_preparation:
    
    def __init__(self, my_asset: Coal_mining_asset):
        self.my_asset = my_asset
    
    
    def coal_preparation_capacity(self):
        """Мощность обогащения угля"""
        pass
    
    def set_amount_of_overtime(self):
        """Сверхурочная работа"""
        if not self.my_asset.can_owner_make_changes(): return
        pass
    
    def overtime_options(self):
        """Варианты сверхурочной работы"""
        pass
   


class Mining_equipment:
    
    def __init__(self, my_asset: Coal_mining_asset):
        self.my_asset = my_asset
    
    
    def number_of_equipment(self) -> dict:
        """Количество оборудования"""
        pass
    
    def power_of_one_unit() -> dict:
        """Мощность оборудования"""
        pass
    
    def number_of_people_for_service() -> dict:
        """Необходимо персонала для обслуживания оборудования"""
        pass
    
    def set_target_amount_of_equipment(self, amount: int):
        """Целевое количество оборудования"""
        if not self.my_asset.can_owner_make_changes(): return
        pass
    
    def amount_of_equipment_available_for_buy() -> int:
        """Количество оборудования доступного для покупки"""
        pass


class Preparation_equipment:
    
    def __init__(self, my_asset: Coal_mining_asset):
        self.my_asset = my_asset
    
    
    def number_of_equipment(self) -> dict:
        """Количество оборудования"""
        pass
    
    def power_of_one_unit() -> dict:
        """Мощность оборудования"""
        pass
    
    def number_of_people_for_service() -> dict:
        """Необходимо персонала для обслуживания оборудования"""
        pass
    
    def set_target_amount_of_equipment(self, amount: int):
        """Целевое количество оборудования"""
        if not self.my_asset.can_owner_make_changes(): return
        pass
    
    def amount_of_equipment_available_for_buy() -> int:
        """Количество оборудования доступного для покупки"""
        pass


class Managers:
    
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
    
    def set_target_number_of_management(self):
        """ """
        if not self.my_asset.can_owner_make_changes(): return
        pass
    
    def limiting_target_number_of_management(self) -> dict:
        """ """
        pass
    
    def change_working_conditions_for_managers(self):
        """ """
        if not self.my_asset.can_owner_make_changes(): return
        pass
    
    def working_conditions_for_managers(self):
        """ """
        pass



class Staff:
    
    def __init__(self, my_asset: Coal_mining_asset):
        self.my_asset = my_asset
    
    
    def qualifications() -> dict:
        """ """
        pass
    
    def number_of_staff() -> dict:
        """ """
        pass
    
    def downtime_due_to_staff_errors(self):
        """"""
        pass
    
    def set_target_number_of_staff(self):
        """ """
        if not self.my_asset.can_owner_make_changes(): return
        pass
    
    def limiting_target_number_of_staff(self) -> dict:
        """ """
        pass
    
    

class HR:
    
    def __init__(self, my_asset: Coal_mining_asset):
        self.my_asset = my_asset
    
    
    def number_of_managers_available_for_hire():
        """ """
        pass
    
    def number_of_staff_available_for_hire():
        """ """
        pass
    
    