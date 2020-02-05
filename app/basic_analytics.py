import time

from app.managers import simulate_simple_connections, save_output_to_file

start_time = time.time()

list_to_print, simple_person_days_avg, spin_person_days_avg, count_of_visits, percent_of_useful_notifications, \
percent_of_spin_users_that_have_notifications = simulate_simple_connections()

print(list_to_print)

print('simple', simple_person_days_avg)

print('spin', spin_person_days_avg)

print('count_of_doctor_visits', count_of_visits)

percent_diff = ((count_of_visits['spin_user'] - count_of_visits['simple_user']) / count_of_visits['spin_user']) * 100

print('count_of_doctor_visits percent diff', percent_diff)

print('percent_of_useful_notifications', percent_of_useful_notifications)

print('percent_of_spin_users_that_have_notifications', percent_of_spin_users_that_have_notifications)

save_output_to_file(list_to_print)

print("--- %s seconds ---" % (time.time() - start_time))