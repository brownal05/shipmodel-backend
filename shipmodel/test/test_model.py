import unittest

from shipmodel.src.baseshipmodel import BaseShipModel

class TestBasicFunction(unittest.TestCase):
    def setUp(self):
        model_specific_options = {
            'A4':13.00 , 'B4':17.70,'C4':13.00, 'D4':21.20, 'E4':8.75, 'F4':None, 'G4':5.35
        }
        price_ifo =568.50
        price_aux =595.50
        self.model = BaseShipModel(model_specific_options,price_ifo,price_aux)

    def test(self):
        self.assertTrue(True)

    def test_3(self):
        self.assertEqual(self.model.options,{
            'A4':13.00 , 'B4':17.70,'C4':13.00, 'D4':21.20, 'E4':8.75, 'F4':None, 'G4':5.35
        })

    def test_get_steam_value(self):
        steam = self.model.get_steam_value(None, None)
        self.assertEqual(steam, 0.00)

        steam = self.model.get_steam_value(5147,None)
        self.assertEqual(16.496794871794872,steam)

        steam = self.model.get_steam_value('', 'B')
        self.assertEqual(steam, 0.00)

        steam = self.model.get_steam_value(5147, None)
        self.assertEqual(16.496794871794872,steam)

    def test_get_arr_date(self):
        arr_date = self.model.get_arr_date(16.496794872,'03/01/00 0000')
        self.assertEqual(arr_date,'19/01/00 1155')

    def test_get_dep_date(self):
        dep_date = self.model.get_dep_date(4.00, '30/12/99 0000')
        self.assertEqual(dep_date, '03/01/00 0000')

        dep_date = self.model.get_dep_date(2.25, '19/01/00 1155')
        self.assertEqual(dep_date, '21/01/00 1755')

        dep_date = self.model.get_dep_date(None, '07/02/00 0550')
        self.assertEqual(dep_date, '07/02/00 0550')

    def test_get_IFO_value(self):
        ifo_value = self.model.get_IFO_value(4.00, 0.00, None)
        self.assertEqual(ifo_value, 35.00)

        ifo_value = self.model.get_IFO_value(None, 16.50, 'B')
        self.assertEqual(ifo_value, 292.05)

    def test_get_AUX_value(self):
        aux_value = self.model.get_AUX_value(2.25, 16.50)
        self.assertEqual(aux_value, 12.04)

        aux_value = self.model.get_AUX_value(None, 16.50)
        self.assertEqual(aux_value, 0.0)

        aux_value = self.model.get_AUX_value(None, 0.0)
        self.assertEqual(aux_value, 0.0)

    def test_get_calculated_value_of_steam(self):
        steam_array = [0.00, 16.50, 16.50, 0.00, 0.00]
        sum_of_steam = self.model.get_calculated_value_of_steam(steam_array)
        self.assertEqual(sum_of_steam, 33.0)

    def test_get_add_on_value_of_steam(self):
        add_on_value = self.model.get_add_on_value_of_steam(32.99)
        self.assertEqual(add_on_value, 2.47425)

        add_on_value = self.model.get_add_on_value_of_steam(32.99, True)
        self.assertEqual(add_on_value, 2.47)

    def test_get_calculated_value_of_est_days(self):
        calculated_value_of_est_days = self.model.get_calculated_value_of_est_days([4.00, 2.25])
        self.assertEqual(6.25, calculated_value_of_est_days)

    def test_get_sum_of_steam_and_est_days(self):
        sum_of_steam_and_est_days = self.model.get_sum_of_steam_and_est_days(32.99 + 6.25, 2.47)
        self.assertEqual(41.71, sum_of_steam_and_est_days)

    def test_get_IFO_cons_value(self):
        # TODO testing with rounded values
        ifo_value_array = [35.00, 369.42, 291.99, 0.00]
        IFO_cons_value = self.model.get_IFO_cons_value(ifo_value_array, None, 2.47, True)
        self.assertEqual(748.77, IFO_cons_value)

    def test_get_MDO_cons_value(self):
        aux_value_array = [21.40, 12.04, 0.0]
        mdo_value = self.model.get_MDO_cons_value(aux_value_array, None, 2.47, True)
        self.assertEqual(33.44, mdo_value)

    def test_get_IFO_cost_value(self):
        ifo_cost = self.model.get_IFO_cost_value(748.87, True)
        self.assertEqual(425732.6, ifo_cost)

    def test_get_MDO_cost_value(self):
        mdo_cost = self.model.get_MDO_cost_value(33.44, True)
        self.assertEqual(19913.52, mdo_cost)

    def test_get_bunker_cost(self):
        bunker_cost = self.model.get_bunker_cost(425.734, 19.912, True)
        self.assertEqual(445.65, bunker_cost)

    def test_get_gross_freight(self):
        quantity_array = [35000]
        rate_array = [19.44]
        ws_array = [150]
        gross_feight = self.model.get_gross_freight(quantity_array, rate_array, ws_array)
        self.assertEqual(1020600, gross_feight)

    def test_get_commision(self):
        quantity_array = [35000]
        rate_array = [19.44]
        ws_array = [150]
        commision_array = [2.50]
        commision_value = self.model.get_commision(quantity_array, rate_array, ws_array, commision_array)
        self.assertEqual(25515, commision_value)

    def test_get_sum_of_port_cost(self):
        port_array = [None, 38000, 40000, 0, 0, None]
        sum_of_port = self.model.get_sum_of_port_cost(port_array)
        self.assertEqual(78000, sum_of_port)

    def test_get_total_cost(self):
        seca_bunker_loading = 20000
        canal_cost = None
        port_cost = 78000
        bunker_cost = 445646
        total_cost = self.model.get_total_cost(seca_bunker_loading, canal_cost, port_cost, bunker_cost)
        self.assertEqual(543646, total_cost)

    def test_get_total_net_income(self):
        gross_freight = 1020600
        commision = 25515
        other_income = None
        total_cost = 543646
        total_income = self.model.get_total_net_income(gross_freight, commision, other_income, total_cost)
        self.assertEqual(451439, total_income)

    def test_get_profit_loss_value(self):
        net_income = 451439
        calculated_total = 41.72
        profit_lost = self.model.get_profit_loss_value(net_income,calculated_total)
        self.assertEqual(451439,profit_lost)

    def test_get_net_daily_value(self):
        net_income = 451439
        calculated_total = 41.72
        net_daily_value = self.model.get_net_daily_value(net_income,calculated_total,True)
        self.assertEqual(10821, net_daily_value)

if __name__ == '__main__':
    unittest.main()