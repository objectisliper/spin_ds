import time

from app.managers import simulate_simple_connections, save_output_to_file
from app.simulation_settings import TOTAL_INFECTED_PEOPLE_OUTPUT_FILE, PERCENT_OF_INFECTIONS_BY_DAY_OUTPUT_FILE
from app.utils import set_environment, get_setting

start_time = time.time()

set_environment()

list_to_print, simple_person_days_avg, spin_person_days_avg, count_of_visits, percent_of_useful_notifications, \
percent_of_spin_users_that_have_notifications, infections_via_connection_percent, \
count_of_useful_doctor_visits = simulate_simple_connections()

print(list_to_print)

print('simple', simple_person_days_avg)

print('spin', spin_person_days_avg)

print('count_of_doctor_visits', count_of_visits)

percent_diff = ((count_of_visits['spin_user'] - count_of_visits['simple_user']) / count_of_visits['spin_user']) * 100

print('count_of_doctor_visits percent diff', percent_diff)

print('percent_of_useful_notifications', percent_of_useful_notifications)

print('percent_of_spin_users_that_have_notifications', percent_of_spin_users_that_have_notifications)

print('infections_via_connection_percent', infections_via_connection_percent)

print('count_of_useful_doctor_visits (simple_users)', count_of_useful_doctor_visits)

save_output_to_file(list_to_print, TOTAL_INFECTED_PEOPLE_OUTPUT_FILE, is_keys_tuple=True)

save_output_to_file(infections_via_connection_percent, PERCENT_OF_INFECTIONS_BY_DAY_OUTPUT_FILE)

print("--- %s seconds ---" % (time.time() - start_time))
