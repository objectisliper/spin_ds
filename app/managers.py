import copy
import datetime
import json
from random import randint, sample
from secrets import randbelow
from statistics import mean

from app.models import StandardPerson
from app.settings import POPULATION, TIME_INTERVAL_DAYS, DISEASES_DETECT_LIST, \
    USER_DAYS_DELAY_BEFORE_USE_SPIN, NEW_PEOPLE_DAY_LUCK, \
    EXIT_PEOPLE_DAY_LUCK
from app.utils import decision


def save_output_to_file(results: dict, file_name, is_keys_tuple=False):
    def remap_keys(mapping):
        return {" ".join(k): v for k, v in mapping.items()}

    with open(file_name, 'w+') as f:
        f.write(json.dumps(remap_keys(results) if is_keys_tuple else results))


def simulate_simple_connections() -> (dict, list, list, dict, float, float, list):
    simple_person_days_avg = copy.deepcopy(DISEASES_DETECT_LIST)

    spin_person_days_avg = copy.deepcopy(DISEASES_DETECT_LIST)

    count_of_doctor_visits = {'simple_user': [], 'spin_user': []}

    infections_via_connection_percent = {'simple_user': [], 'spin_user': []}

    percent_of_useful_notifications = []

    people_with_diseases_by_day = {}

    persons = [StandardPerson() for i in range(POPULATION)]

    for disease in DISEASES_DETECT_LIST:
        people_with_diseases_by_day[disease, 'SIMPLE USER'] = []
        people_with_diseases_by_day[disease, 'SPIN USER'] = []
        people_with_diseases_by_day[disease, 'ALL POPULATION'] = []

    get_disease_day_data(people_with_diseases_by_day, persons, 0)

    print(datetime.datetime.now())

    iterate_through_days(people_with_diseases_by_day, persons, simple_person_days_avg, spin_person_days_avg,
                         count_of_doctor_visits, percent_of_useful_notifications, infections_via_connection_percent)

    percent_of_spin_users_that_have_notifications = get_analytics_data(persons, simple_person_days_avg,
                                                                       spin_person_days_avg, count_of_doctor_visits,
                                                                       percent_of_useful_notifications)

    calculate_avg(simple_person_days_avg)

    calculate_avg(spin_person_days_avg)

    calculate_avg(count_of_doctor_visits)

    return people_with_diseases_by_day, simple_person_days_avg, spin_person_days_avg, count_of_doctor_visits, \
           mean(percent_of_useful_notifications), percent_of_spin_users_that_have_notifications, \
           infections_via_connection_percent


def get_analytics_data(persons, simple_days_avg, spin_days_avg, count_of_doctor_visits,
                       percent_of_useful_notifications):
    spin_users_that_have_notifications = 0
    spin_users_count = 0
    for person in persons:
        get_count_of_doctor_visits_for_one(person, count_of_doctor_visits)
        get_days_avg_before_find_disease_for_one(person, simple_days_avg, spin_days_avg)
        if person.is_spin_user:
            spin_users_count += 1
            if person.is_already_have_notifications():
                percent_of_useful_notifications.append(person.get_percent_of_useful_notifications())
                spin_users_that_have_notifications += 1

    return spin_users_that_have_notifications / spin_users_count * 100


def get_count_of_doctor_visits_for_one(person, count_of_doctor_visits):
    if len(person.count_of_doctor_visits_per_year) > 0:
        avg_count_of_doctor_visits = mean(person.count_of_doctor_visits_per_year)
        if person.is_spin_user:
            count_of_doctor_visits['spin_user'].append(avg_count_of_doctor_visits)
        else:
            count_of_doctor_visits['simple_user'].append(avg_count_of_doctor_visits)


def get_days_avg_before_find_disease_for_one(person, simple_days_avg, spin_days_avg):
    for disease, value in person.get_days_before_found_disease_avg():
        if person.is_spin_user:
            spin_days_avg[disease].append(value)
        else:
            simple_days_avg[disease].append(value)


def iterate_through_days(people_with_diseases_by_day, persons, simple_days_avg, spin_days_avg, count_of_doctor_visits,
                         percent_of_useful_notifications, infections_via_connection_percent):
    for i in range(TIME_INTERVAL_DAYS):
        # persons = MultiprocSimulation(persons).process_population()

        try_to_connect_persons(i, persons)

        total_simple_connection_quantity = 0
        total_simple_infection_via_connection_quantity = 0

        total_spin_connection_quantity = 0
        total_spin_infection_via_connection_quantity = 0

        for person in persons:
            if person.is_already_connected_today:
                if person.is_connected_with_spin_user:
                    total_spin_connection_quantity += 1
                else:
                    total_simple_connection_quantity += 1
                if person.was_infected_today:
                    if person.is_connected_with_spin_user:
                        total_spin_infection_via_connection_quantity += 1
                    else:
                        total_simple_infection_via_connection_quantity += 1
            person.is_already_connected_today = False
            person.is_notified = False
            person.was_infected_today = False
            person.is_connected_with_spin_user = False
            person.is_connected_with_simple_user = False


        infections_via_connection_percent['simple_user'].append(
            (total_simple_infection_via_connection_quantity / total_simple_connection_quantity) * 100 if total_simple_connection_quantity != 0 else 0
        )

        infections_via_connection_percent['spin_user'].append(
            (total_spin_infection_via_connection_quantity / total_spin_connection_quantity) * 100 if total_spin_connection_quantity != 0 else 0
        )

        get_disease_day_data(people_with_diseases_by_day, persons, i)

        simulate_population_change(persons, simple_days_avg, spin_days_avg, count_of_doctor_visits,
                                   percent_of_useful_notifications)
        # print(people_with_diseases_by_day)


def try_to_connect_persons(day, persons):
    for person in persons:
        people_to_connect = get_people_to_connect(person, persons)

        person.live_a_day(people_to_connect, day > USER_DAYS_DELAY_BEFORE_USE_SPIN, day % 365)


def get_people_to_connect(person, persons):
    luck = person.luck
    if len(person.known_diseases) > 0:
        luck = luck / 2
    if not person.is_already_connected_today and decision(luck):
        # list_of_possible_people_to_connect = list(
        #         filter(lambda person_to_chose: not person_to_chose.is_already_connected_today and
        #                person_to_chose != person, persons)
        #     )

        list_of_possible_people_to_connect = sample(persons, 2)

        if list_of_possible_people_to_connect[0] != person:
            people_to_connect = list_of_possible_people_to_connect[0]
        else:
            people_to_connect = list_of_possible_people_to_connect[1]
    else:
        people_to_connect = None
    return people_to_connect


def calculate_avg(dict_of_values_to_calculate_avg):
    for key in dict_of_values_to_calculate_avg:
        dict_of_values_to_calculate_avg[key] = mean(dict_of_values_to_calculate_avg[key])


def simulate_population_change(persons, simple_days_avg, spin_days_avg, count_of_doctor_visits,
                               percent_of_useful_notifications):
    persons_len = len(persons)
    for i in range(int(randint(*EXIT_PEOPLE_DAY_LUCK) / 1000 * persons_len)):
        person_that_exit = persons.pop(randbelow(len(persons)))
        get_count_of_doctor_visits_for_one(person_that_exit, count_of_doctor_visits)
        get_days_avg_before_find_disease_for_one(person_that_exit, simple_days_avg, spin_days_avg)
        if person_that_exit.is_spin_user and person_that_exit.is_already_have_notifications():
            percent_of_useful_notifications.append(person_that_exit.get_percent_of_useful_notifications())
    for i in range(int(randint(*NEW_PEOPLE_DAY_LUCK) / 1000 * persons_len)):
        persons.append(StandardPerson())


def get_disease_day_data(people_with_diseases_by_day, persons, day):
    spin_users = list(filter(lambda person_to_check: person_to_check.is_spin_user, persons))
    simple_peoples = list(set(persons) - set(spin_users))
    for disease, disease_group in people_with_diseases_by_day:
        if disease_group == 'SPIN USER':
            if day > USER_DAYS_DELAY_BEFORE_USE_SPIN:
                people_with_diseases_by_day[disease, disease_group].append(
                    len([spin_user.diseases for spin_user in spin_users if disease in spin_user.diseases]) / len(
                        spin_users) * 100
                )
            else:
                people_with_diseases_by_day[disease, disease_group].append(0)
        elif disease_group == 'ALL POPULATION':
            people_with_diseases_by_day[disease, disease_group].append(
                len([person.diseases for person in persons if disease in person.diseases]) / len(
                    persons) * 100
            )
        else:
            people_with_diseases_by_day[disease, disease_group].append(
                len([simple_people.diseases for simple_people in simple_peoples if
                     disease in simple_people.diseases]) / len(
                    simple_peoples) * 100
            )
