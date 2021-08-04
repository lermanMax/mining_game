from mining_company_lib import (
    Entity, Region, Q_, Asset, Product, 
    Mining_machine, Preparation_line)


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
   


class Equipment:
    
    def __init__(self, my_asset: Coal_mining_asset):
        self.my_asset = my_asset
        
        self._target_amount_of_equipment = {
            'Mining_equipment_class_C': 0,
            'Mining_equipment_class_B': 0,
            'Mining_equipment_class_A': 0, 
            'Preparation_line': 0
            }
    
    
    def get_list_of_mining_equipment(self) -> set:
        list_of_mining_equipment = set()
        for product in self.my_asset.get_property_list():
            if product is Mining_machine:
                list_of_mining_equipment.add(product)
                
        return list_of_mining_equipment
    
    def get_list_of_preparation_equipment(self) -> set:
        list_of_preparation_equipment = set()
        for product in self.my_asset.get_property_list():
            if product is Preparation_line:
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
        result = {
            'Mining_equipment_class_C': {'max_limit': 0, 'min_limit': 0},
            'Mining_equipment_class_B': {'max_limit': 0, 'min_limit': 0},
            'Mining_equipment_class_A': {'max_limit': 0, 'min_limit': 0} }
        
        available_for_buy = self.amount_of_equipment_available_for_buy()
        amount_of_equipment = self.get_amount_of_equipment()
        
        for name, limit_dict in result.items():
            limit_dict['max_limit'] = (available_for_buy[name]
                                       + amount_of_equipment[name])
        return result
    
    
    def set_target_amount_of_equipment(self, target_amount: dict):
        """Целевое количество оборудования
        
        target_amount ={
            'name': Q_(1, 'count')
            }
        """
        if not self.my_asset.can_owner_make_changes(): return
        
        limit = self.limiting_target_amount_of_equipment()
        try:
            for name, amount in target_amount.items():
                if not (limit[name]['max_limit'] 
                        <= amount 
                        <= limit[name]['min_limit']):
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
            
        on_market = my_market.amount_of_mining_equipment_available_for_sale()
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
        for name, target_amount in self.get_target_amount_of_equipment():
            if name in amount_of_equipment:
                difference = target_amount - amount_of_equipment[name]
                list_to_buy[name] = max(difference, 0)
            else:
                list_to_buy[name] = target_amount
        
        return list_to_buy
    
    def list_of_equipment_need_to_sale(self) -> dict:
        """Списко на продажу
        
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
    
    def purchase(self):
        """Закупка оборудования"""
        
        
            


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
    
    