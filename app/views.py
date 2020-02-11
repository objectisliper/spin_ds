import time

import aiohttp_jinja2
from aiohttp import web

from . import simulation_settings
from .managers import simulate_simple_connections
from .utils import render_plot, set_simulation_setting, get_setting, live_render_plot
from .settings import STATIC_FOLDER, DISEASES_LIST, UNHEALABLE_DISEASES, VACCINATION, DISEASES_LUCK_LIST, \
    DISEASES_LUCK_HEAL_LIST, DISEASES_DAILY_LUCK_HEAL_LIST, SPIN_USERS, REACT_LUCKY


SETTINGS = [
    'POPULATION',
    'TIME_INTERVAL_DAYS',
    'SPIN_USERS%',
    'REACT_LUCKY%',
    'USER_DAYS_DELAY_BEFORE_USE_SPIN',
    'DISEASES_DETECT_LIST[]',
    'UNHEALABLE_DISEASES[]',
    'VACCINATION{}%',
    'DISEASES_LIST{}%',
    'DISEASES_LUCK_HEAL_LIST{}%',
    'DISEASES_LUCK_LIST{}%',
    'DISEASES_DAILY_LUCK_HEAL_LIST{}%',
]


@aiohttp_jinja2.template('example_html_template.html')
class MainView(web.View):
    async def get(self):
        html, js = render_plot()
        simulation_settings_vars = {settings_variable: vars(simulation_settings)[settings_variable]
                                    for settings_variable in vars(simulation_settings) if '__' not in settings_variable}
        return {'embed_bokeh_html': html, 'simulation_settings': simulation_settings_vars, 'embed_js': js,
                'is_live_render': False}


@aiohttp_jinja2.template('set_up_simulation_template.html')
class SetUpSimulationView(web.View):
    async def get(self):
        diseases = [disease for disease in DISEASES_LIST]
        return {'diseases': diseases, 'diseases_prevalence': DISEASES_LIST, 'unhelable_diseases': UNHEALABLE_DISEASES,
                'vaccination': VACCINATION, 'disease_transmition_chance': DISEASES_LUCK_LIST,
                'disease_doctor_heal_chance': DISEASES_LUCK_HEAL_LIST,
                'disease_self_heal_chance': DISEASES_DAILY_LUCK_HEAL_LIST, 'spin_user_percent': SPIN_USERS,
                'react_on_notification_chance': REACT_LUCKY}


@aiohttp_jinja2.template('example_html_template.html')
class ParametrizedSimulationView(web.View):
    async def get(self):
        for setting in SETTINGS:
            if '[]' in setting:
                if 'DISEASES_DETECT_LIST' in setting:
                    dict_to_set = {disease: [] for disease in self.request.query.getall(setting)}
                    set_simulation_setting(setting.replace('[]', ''), dict_to_set)
                else:
                    set_simulation_setting(setting.replace('[]', ''), self.request.query.getall(setting))
            elif '{}' in setting:
                if '%' in setting:
                    set_simulation_setting(setting.replace('{}', '').replace('%', ''),
                                           {disease: float(self.request.query.get(setting.replace('{}', '_').replace('%', '') + disease))/100
                                            for disease in DISEASES_LIST}
                                           )
                else:
                    set_simulation_setting(setting.replace('{}', ''),
                                           {disease: self.request.query.get(setting.replace('{}', '_') + disease)
                                            for disease in DISEASES_LIST}
                                           )
            else:
                if '%' in setting:
                    set_simulation_setting(
                        setting.replace('%', ''),
                        float(self.request.query.get(setting.replace('%', '')))/100
                    )
                else:
                    set_simulation_setting(setting, int(self.request.query.get(setting)))
        get_setting.cache_clear()
        simulation_settings_vars = {settings_variable: get_setting(settings_variable.replace('[]', '').replace('{}', '')
                                                                   .replace('%', ''))
                                    for settings_variable in SETTINGS}

        start_time = time.time()

        list_to_print, simple_person_days_avg, spin_person_days_avg, count_of_visits, percent_of_useful_notifications, \
        percent_of_spin_users_that_have_notifications, infections_via_connection_percent, \
        count_of_useful_doctor_visits = simulate_simple_connections()

        wasted_time = time.time() - start_time

        percent_diff = ((count_of_visits['spin_user'] - count_of_visits['simple_user']) / count_of_visits[
            'spin_user']) * 100

        html, js = live_render_plot(list_to_print, infections_via_connection_percent)

        return {'embed_bokeh_html': html, 'simulation_settings': simulation_settings_vars, 'embed_js': js,
                'is_live_render': True, 'simple_person_days_avg': simple_person_days_avg,
                'spin_person_days_avg': spin_person_days_avg, 'count_of_visits': count_of_visits,
                'percent_of_useful_notifications': percent_of_useful_notifications,
                'percent_of_spin_users_that_have_notifications': percent_of_spin_users_that_have_notifications,
                'count_of_useful_doctor_visits': count_of_useful_doctor_visits, 'wasted_time': wasted_time,
                'percent_diff': percent_diff}
