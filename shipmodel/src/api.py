from shipmodel.src.baseshipmodel import BaseShipModel

class ShipModelAPI:
    def perform_calculation(self,data):

        actual_output_values = {}
        display_output_values = {}


        # user input should get from web request
        user_inputs = {}

        port_inputs = data['port_inputs']
        character_inputs = data['character_inputs']


        # TODO this has to be derived based on model going to initiate based on user input
        # getModelSpecificOptions(modelName)
        model_specific_options = {
                'A4':13.00 , 'B4':24.00,'C4':13.00, 'D4':27.00, 'E4':11.00, 'F4':None, 'G4':4.20
            }

        # TODO this has to be derived based on model going to initiate based on user input
        model_price_ifo = 554
        model_price_aux = 575

        model = BaseShipModel(model_specific_options,model_price_ifo,model_price_aux)

        steam_array = model.get_steam_array(port_inputs)
        arr_dates ,dept_dates = model.get_arr_dates_and_dep_dates(port_inputs,steam_array)
        ifo_array = model.get_ifo_array(port_inputs,steam_array)
        aux_array = model.get_aux_array(port_inputs,steam_array)

        calculated_steam_sum = model.get_calculated_value_of_steam(steam_array)
        add_on_value_of_steam =model.get_add_on_value_of_steam(calculated_steam_sum)

        est_days_array = [o['est_days'] for o in port_inputs]
        calculated_est_days_sum = model.get_calculated_value_of_est_days(est_days_array)

        # TO get this from Model class, most are empty
        add_on_value_of_est_days = 0

        calculated_total = calculated_steam_sum + add_on_value_of_steam + calculated_est_days_sum + add_on_value_of_est_days
        print(calculated_total)

        ifo_cons = model.get_IFO_cons_value(ifo_array,add_on_value_of_est_days,add_on_value_of_steam)
        display_ifo_cons = model.get_IFO_cons_value(ifo_array,add_on_value_of_est_days,add_on_value_of_steam,True)
        print('display_ifo_cons : ',display_ifo_cons)
        actual_output_values['ifo_cons'] = ifo_cons
        display_output_values['ifo_cons'] = display_ifo_cons

        mdo_cons = model.get_MDO_cons_value(aux_array,add_on_value_of_est_days,add_on_value_of_steam)
        display_mdo_cons = model.get_MDO_cons_value(aux_array,add_on_value_of_est_days,add_on_value_of_steam,True)
        print('display_mdo_cons : ',display_mdo_cons)
        actual_output_values['mdo_cons'] = mdo_cons
        display_output_values['mdo_cons'] = display_mdo_cons

        ifo_cost = model.get_IFO_cost_value(ifo_cons)
        display_ifo_cost = model.get_IFO_cost_value(ifo_cons,True)
        print('display_ifo_cost: ',display_ifo_cost)
        actual_output_values['ifo_cost'] = ifo_cost
        display_output_values['ifo_cost'] = display_ifo_cost

        mdo_cost = model.get_MDO_cost_value(mdo_cons)
        display_mdo_cost = model.get_MDO_cost_value(mdo_cons,True)
        print('display_mdo_cost: ', display_mdo_cost)
        actual_output_values['mdo_cost'] = mdo_cost
        display_output_values['mdo_cost'] = display_mdo_cost

        bunker_cost = model.get_bunker_cost(ifo_cost,mdo_cost)
        display_bunker_cost = model.get_bunker_cost(ifo_cost,mdo_cost,True)
        print('display_bunker_cost: ', display_bunker_cost)
        actual_output_values['bunker_cost'] = bunker_cost
        display_output_values['bunker_cost'] = display_bunker_cost

        quantity_array = [o['quantity'] for o in character_inputs]
        rate_array = [o['rate'] for o in character_inputs]
        ws_array = [o['ws'] for o in character_inputs]
        commission_array = [o['commission'] for o in character_inputs]
        gross_freight = model.get_gross_freight(quantity_array,rate_array,ws_array)
        display_gross_freight = round(gross_freight,0)
        print('display_gross_freight: ',display_gross_freight)
        actual_output_values['gross_freight'] = gross_freight
        display_output_values['gross_freight'] = display_gross_freight

        commission_vlaue = model.get_commision(quantity_array, rate_array, ws_array,commission_array)
        display_commission_vlaue = round(commission_vlaue, 0)
        print('display_commission_vlaue: ', display_commission_vlaue)
        actual_output_values['commission_vlaue'] = commission_vlaue
        display_output_values['commission_vlaue'] = display_commission_vlaue

        port_cost_array = [o['port_cost'] for o in port_inputs]
        port_cost = model.get_sum_of_port_cost(port_cost_array)
        display_port_cost = round(port_cost)
        print('display_port_cost: ', display_port_cost)
        actual_output_values['port_cost'] = port_cost
        display_output_values['port_cost'] = display_port_cost

        # TODO check whether this is model based value or not
        seca_bunker_loading = 20000
        canal_cost =0

        total_cost = model.get_total_cost(seca_bunker_loading,canal_cost,port_cost,bunker_cost)
        display_total_cost = round(total_cost,0)
        print('display_total_cost :',display_total_cost)
        actual_output_values['total_cost'] = total_cost
        display_output_values['total_cost'] = display_total_cost

        # TODO check whether this is model based value or not
        other_income = 0

        net_income = model.get_total_net_income(gross_freight,commission_vlaue,other_income,total_cost)
        display_net_income = round(net_income, 0)
        print('display_net_income :', display_net_income)
        actual_output_values['net_income'] = net_income
        display_output_values['net_income'] = display_net_income

        profit_loss = model.get_profit_loss_value(net_income,calculated_total)
        display_profit_loss = round(profit_loss,0)
        print('display_profit_loss: ',display_profit_loss)
        actual_output_values['profit_loss'] = profit_loss
        display_output_values['profit_loss'] = display_profit_loss

        net_daily = model.get_net_daily_value(net_income,calculated_total)
        display_net_daily = round(net_daily,0)
        print('display_net_daily :',display_net_daily)
        actual_output_values['net_daily'] = net_daily
        display_output_values['net_daily'] = display_net_daily

        json_output = {
            'actual_values': actual_output_values,
            'display_values': display_output_values
        }
        return json_output

    def post_test(self,data):
        print('red data',data['port'])
        return {'shipmode:':data['port']}

