import copy
import os
import time
from datetime import datetime
from statistics import mean

from app.managers import simulate_simple_connections_for_spin_influence_analytics, save_output_to_file
from app.models import StandardPerson
from app.simulation_settings import POPULATION, AVG_STEP_QUANTITY, DISEASES_DETECT_LIST, \
    MIN_SPIN_USERS_FOR_INFLUENCE_ANALYTICS, \
    MAX_SPIN_USERS_FOR_INFLUENCE_ANALYTICS, STEP_OF_SPIN_USERS_FOR_INFLUENCE_ANALYTICS, SPIN_INFLUENCE_OUTPUT_FILE

print(datetime.now())

start_time = time.time()

# start

people_with_diseases_in_last_day = copy.deepcopy(DISEASES_DETECT_LIST)

for i in range(MIN_SPIN_USERS_FOR_INFLUENCE_ANALYTICS, MAX_SPIN_USERS_FOR_INFLUENCE_ANALYTICS,
               STEP_OF_SPIN_USERS_FOR_INFLUENCE_ANALYTICS):

    os.environ['SPIN_USERS'] = str(i/100)

    persons = [StandardPerson() for k in range(POPULATION)]

    list_of_diseases_with_this_percent_of_spin_users = copy.deepcopy(DISEASES_DETECT_LIST)

    for j in range(AVG_STEP_QUANTITY):

        list_of_diseases = simulate_simple_connections_for_spin_influence_analytics(persons)

        for disease in list_of_diseases_with_this_percent_of_spin_users:
            list_of_diseases_with_this_percent_of_spin_users[disease].append(list_of_diseases[disease])

    for disease in list_of_diseases_with_this_percent_of_spin_users:
        people_with_diseases_in_last_day[disease].append(mean(list_of_diseases_with_this_percent_of_spin_users[disease]))

    print(people_with_diseases_in_last_day)

# end

print(people_with_diseases_in_last_day)

save_output_to_file(people_with_diseases_in_last_day, SPIN_INFLUENCE_OUTPUT_FILE)

print("--- %s seconds ---" % (time.time() - start_time))
