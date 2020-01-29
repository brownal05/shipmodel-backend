from datetime import datetime
from datetime import timedelta
from shipmodel.models import Vsl

class BaseShipModel:

    def __init__(self,ship_name,price_ifo,price_aux):
        self.vsl = {}
        # pass this as a parameter, since these values are based on other sheets
        self.options = self.__getModelSpecificOptions(ship_name)
        self.formatted_options = self.__get_formatted_self_options(self.options)

        # TODO this values should be derived
        self.price_ifo = price_ifo
        self.price_aux = price_aux
        self.run_cost = self.__get_run_cost()


    def get_steam_value(self,distance,port_type,display=False):

        if distance == None or distance=='':
            distance = 0
        denominator = self.options['C4'] if port_type=='L' else self.options['A4']
        return distance/denominator/24  if display==False else round(distance/denominator/24,2)

    def get_arr_date(self,steam,dept_date):
        # add steam days to dept_date
        if steam == None:
            steam = 0
        arr_date = datetime.strptime(dept_date,'%d/%m/%y %H%M') + timedelta(hours=steam*24)
        return datetime.strftime(arr_date,'%d/%m/%y %H%M')

    def get_dep_date(self,est_days,arr_date):
        # add est days to arr_date
        if est_days == None:
            est_days = 0
        dep_date = datetime.strptime(arr_date,'%d/%m/%y %H%M') + timedelta(days=est_days)
        return datetime.strftime(dep_date,'%d/%m/%y %H%M')

    def get_IFO_value(self,est_days,steam,port_type,display=False):
        if est_days==None or est_days=='':
            est_days = 0
        ifo_value = ((est_days*self.options['E4'])+(steam*(self.options['D4'] if port_type=="L" else self.options['B4'])))
        return ifo_value if display ==False else round(ifo_value,2)

    def get_AUX_value(self,est_days,steam,display=False):

        left_part = 0
        right_part = 0
        if est_days ==None or est_days =='':
            est_days =0
        if self.options['F4'] != None and self.options['F4'] != '':
            right_part = (steam*self.options['F4'])
        if self.options['G4'] != None and self.options['G4'] != '':
            left_part = (est_days*self.options['G4'])
        aux_value = left_part + right_part

        return aux_value if display == False else round(aux_value,2)

    def get_calculated_value_of_steam(self,steam_array,display=False):
        calculate_value_of_sum = sum(steam_array)
        return calculate_value_of_sum if display==False else round(calculate_value_of_sum,2)

    def get_add_on_value_of_steam(self,calculate_value_of_steam,display=False):
        add_on_value_of_steam  =calculate_value_of_steam*7.5/100
        return add_on_value_of_steam if display==False else round(add_on_value_of_steam,2)

    def get_calculated_value_of_est_days(self,est_days_array):
        calculated_value_of_est_days = sum(est_days_array)
        return calculated_value_of_est_days

    def get_sum_of_steam_and_est_days(self,calculated_value_of_steam,calculated_value_of_est_days):
        total_value = calculated_value_of_steam + calculated_value_of_est_days
        return round(total_value,2)

    def get_IFO_cons_value(self,ifo_value_array,add_on_port,add_on_steam,display=False):

        if add_on_port == None or add_on_port == '':
            add_on_port = 0
        if add_on_steam == None or add_on_steam == '':
            add_on_steam = 0
        ifs_cons_value = sum(ifo_value_array)+(add_on_port * self.formatted_options['E4']) + (add_on_steam * self.formatted_options['D4'])
        return ifs_cons_value if display == False else round(ifs_cons_value,2)

    def get_MDO_cons_value(self,aux_value_array,add_on_port,add_on_steam,display=False):
        if add_on_port == None or add_on_port == '':
            add_on_port = 0
        if add_on_steam == None or add_on_steam == '':
            add_on_steam = 0

        mdo_cons_value =  sum(aux_value_array)+(add_on_port*self.formatted_options['G4'])+(add_on_steam*self.formatted_options['F4'])
        return mdo_cons_value if display == False else round(mdo_cons_value,2)

    def get_IFO_cost_value(self,ifo_cons,display=False):
        ifo_cons = ifo_cons*self.price_ifo
        return ifo_cons if display == False else round(ifo_cons, 2)

    def get_MDO_cost_value(self,mdo_cons, display =False):
        mdo_cost = mdo_cons*self.price_aux
        return mdo_cost if display == False else round(mdo_cost, 2)

    def get_bunker_cost(self,ifo_cost,mdo_cost,display=False):
        bunker_cost = ifo_cost+mdo_cost;
        return bunker_cost if display == False else round(bunker_cost, 2)

    def get_gross_freight(self,quantity_array,rate_array,ws_array,display=False):
        gross_freight = 0
        for i in range(len(quantity_array)):

            if ws_array[i] ==None or ws_array[i] =='':
                ws_array[i] = 0
            if quantity_array[i] ==None or quantity_array[i] =='':
                quantity_array[i] = 0
            if rate_array[i] ==None or rate_array[i] =='':
                rate_array[i] = 0


            if ws_array[i] <=0:
                gross_freight += rate_array[i]
            else:
                gross_freight += quantity_array[i]*rate_array[i]*ws_array[i]/100

        return gross_freight if display==False else round(gross_freight,2)

    def get_commision(self,quantity_array,rate_array,ws_array,commision_array,display=False):
        gross_freight = 0
        for i in range(len(quantity_array)):

            if ws_array[i] ==None or ws_array[i] =='':
                ws_array[i] = 0
            if quantity_array[i] ==None or quantity_array[i] =='':
                quantity_array[i] = 0
            if rate_array[i] ==None or rate_array[i] =='':
                rate_array[i] = 0
            if commision_array[i] ==None or commision_array[i]=='':
                commision_array[i] =0

            if ws_array[i] <=0:
                gross_freight += rate_array[i]
            else:
                gross_freight += (quantity_array[i]*rate_array[i]*ws_array[i]/100)*commision_array[i]/100

        return gross_freight if display==False else round(gross_freight,2)

    def get_sum_of_port_cost(self,port_cost_array,display=False):
        sum_of_port_cost = 0
        for i in range(len(port_cost_array)):
            if port_cost_array[i] ==None or port_cost_array[i] == '':
                continue
            sum_of_port_cost = sum_of_port_cost+ port_cost_array[i]

        return sum_of_port_cost if display==False else round(sum_of_port_cost,2)

    def get_total_cost(self,seca_bunker_loading,canal_cost,port_cost,bunker_cost,display=False):
        total_cost = 0
        if seca_bunker_loading != None:
            total_cost += seca_bunker_loading
        if canal_cost != None:
            total_cost += canal_cost
        if port_cost != None:
            total_cost += port_cost
        if bunker_cost != None:
            total_cost += bunker_cost

        return total_cost if display==False else round(total_cost,2)

    def get_total_net_income(self,gross_freight,commision,other_income,total_cost, display=False):
        net_income = 0
        if gross_freight != None and gross_freight != '':
            net_income = net_income+ gross_freight
        if other_income != None and other_income != '':
            net_income = net_income+ other_income
        if commision != None and commision != '':
            net_income = net_income- commision
        if total_cost != None and total_cost != '':
            net_income = net_income - total_cost

        return net_income if display==False else round(net_income,2)

    def get_profit_loss_value(self,net_income,calculated_total,display=False):
        deduct_value = 0
        if self.run_cost!=None and self.run_cost !='':
            deduct_value = calculated_total * self.run_cost
        profit_loss = net_income-deduct_value

        return profit_loss if display == False else round(profit_loss, 2)

    def get_net_daily_value(self,net_income,calculated_toal,display=False):
        net_daily = net_income/calculated_toal

        return net_daily if display == False else round(net_daily, 0)

    # helper functions
    def get_steam_array(self,port_inputs):
        steam_array = []
        for index in range(len(port_inputs)-1):
            current_port_input = port_inputs[index]
            next_port_input = port_inputs[index+1]

            steam_value = self.get_steam_value(next_port_input['distance'],current_port_input['port_type'])
            display_steam_value = self.get_steam_value(next_port_input['distance'],current_port_input['port_type'],True)
            print('actual steam value:',steam_value)
            print('display steam value:',display_steam_value)
            steam_array.append(steam_value)

        return steam_array

    def get_arr_dates_and_dep_dates(self,port_inputs,steam_array):
        dept_dates = []
        arr_dates = []
        for index in range(len(port_inputs) - 1):
            if index==0:
                previous_dep_date = '30/12/99 0000'
            else:
                previous_dep_date = dept_dates[index-1]

            arr_date = self.get_arr_date(steam_array[index],previous_dep_date)
            dept_date = self.get_dep_date(port_inputs[index+1]['est_days'],arr_date)
            print('arr_date :',arr_date)
            print('dept_date :',dept_date)

            arr_dates.append(arr_date)
            dept_dates.append(dept_date)

        return arr_dates,dept_dates

    def get_ifo_array(self,port_inputs,steam_array):

        ifo_array = []
        for index in range(len(port_inputs)):
            if index != 0:
                ifo_value = self.get_IFO_value(port_inputs[index]['est_days'],steam_array[index-1],port_inputs[index]['port_type'])
                display_ifo_value = self.get_IFO_value(port_inputs[index]['est_days'],steam_array[index-1],port_inputs[index]['port_type'],True)
                print('ifo value:',ifo_value)
                print('display_ifo_value:',display_ifo_value)
                ifo_array.append(ifo_value)
        return ifo_array

    def get_aux_array(self,port_inputs,steam_array):

        aux_array = []
        for index in range(len(port_inputs)):
            if index != 0:
                aux_value = self.get_AUX_value(port_inputs[index]['est_days'],steam_array[index-1])
                display_aux_value = self.get_AUX_value(port_inputs[index]['est_days'],steam_array[index-1],True)
                print('aux value:',aux_value)
                print('display_aux_value:',display_aux_value)
                aux_array.append(aux_value)
        return aux_array

    def __get_formatted_self_options(self,options):
        temp_options = {}
        for key in options:
            temp_options[key] = options[key]
            if temp_options[key] == None or temp_options == '':
                temp_options[key] = 0
        return temp_options

    def __getModelSpecificOptions(self,ship_name):
        result = Vsl.objects.filter(vessel__contains=ship_name).values()
        if len(result)==0:
             raise Exception('No ship found with given name')

        model_specific_options = {
            'A4': 0, 'B4': 0, 'C4': 0, 'D4': 0, 'E4': 0, 'F4': 0, 'G4': 0
        }
        for vsl in result:
            model_specific_options['A4'] =  float(vsl['speedB'])
            model_specific_options['B4'] =  float(vsl['consB'])
            model_specific_options['C4'] =  float(vsl['speedL'])
            model_specific_options['D4'] =  float(vsl['consL'])
            model_specific_options['E4'] =  float(vsl['ifo_port'])
            model_specific_options['F4'] =  float(vsl['aux_steam'])
            model_specific_options['G4'] =  float(vsl['aux_port'])

            break
        return model_specific_options

    def __get_run_cost(self):
        return None
