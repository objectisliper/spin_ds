import copy
import json
import time
from random import randint, random
from uuid import uuid4
import multiprocessing as mp

from numpy import asarray, savetxt, loadtxt

from app.settings import DISEASES_LIST, POPULATION, TIME_INTERVAL_DAYS, DISEASES_DETECT_LIST, DISEASES_LUCK_LIST, \
    DOCTOR_CHECK_TIME_INTERVAL, DISEASES_LUCK_HEAL_LIST, VACCINATION, SPIN_USERS, REACT_LUCKY, \
    DISEASES_DAILY_LUCK_HEAL_LIST, USER_DAYS_DELAY_BEFORE_USE_SPIN, UNHEALABLE_DISEASES


def decision(probability: float) -> bool:
    return random() < probability


class StandardPerson:

    def __init__(self, name: str):
        self.luck = randint(27, 500) / 10000
        self.test_time_interval = randint(160, 1800)
        self.last_test_was = randint(randint(1, randint(2, 30)), int(self.test_time_interval/randint(1, 3)))
        self.is_already_connected_today = bool(randint(0, 1))
        self.diseases = []
        self.is_notified = False
        self.known_diseases = []
        self.name = name
        self.__spin_partner_list = []
        self.is_spin_user = decision(SPIN_USERS)
        self.__vaccination = []
        self.__vaccination_try()

        for disease in DISEASES_LIST:
            if len(self.diseases) > 14:
                break
            if decision(DISEASES_LIST.get(disease)):
                self.diseases.append(disease)

    def __vaccination_try(self):
        for disease in VACCINATION:
            if decision(VACCINATION[disease]):
                self.__vaccination.append(disease)

    def live_a_day(self, person_to_connect, start_use_spin):
        if person_to_connect is not None:
            person_to_connect.connect(self, start_use_spin)
            self.connect(person_to_connect, start_use_spin)
        self.last_test_was -= 1
        self.check_is_need_go_to_doctor()
        if len(self.known_diseases) > 0 and not self.__is_only_unhealable_known_diseases:
            self.__try_to_heal()

    def connect(self, person_to_connect, start_use_spin):
        if start_use_spin and self.is_spin_user and person_to_connect.is_spin_user:
            self.__spin_partner_list.append(person_to_connect)
        for connect_disease in person_to_connect.diseases:
            if connect_disease in self.diseases:
                continue
            elif len(self.diseases) > 14:
                break
            elif decision(DISEASES_LIST.get(connect_disease)):
                if connect_disease not in self.__vaccination and \
                        (connect_disease not in DISEASES_LUCK_LIST or decision(DISEASES_LUCK_LIST[connect_disease])):
                    self.diseases.append(connect_disease)
        self.is_already_connected_today = True

    def notified(self, from_who):
        self.is_notified = True
        for partner in self.__spin_partner_list:
            if partner != from_who and not partner.is_notified:
                partner.notified(self)
        self.__clear_spin_partner_list()
        if decision(REACT_LUCKY):
            self.check_is_need_go_to_doctor(is_spin=True)

    def check_is_need_go_to_doctor(self, is_spin=False):
        if self.last_test_was < 1 or is_spin:
            self.last_test_was = self.test_time_interval
            if self.is_spin_user and len(self.diseases) > 0 and not is_spin:
                for partner in self.__spin_partner_list:
                    partner.notified(self)
                self.__clear_spin_partner_list()
            self.__try_to_heal(doctor=True)

    def __clear_spin_partner_list(self):
        self.__spin_partner_list = []

    def __try_to_heal(self, doctor=False):
        for disease_index, disease in enumerate(self.diseases):
            if doctor:
                self.known_diseases.append(disease)
            if disease not in DISEASES_LUCK_HEAL_LIST:
                self.diseases.pop(disease_index)
            elif doctor and decision(DISEASES_LUCK_HEAL_LIST[disease]):
                self.diseases.pop(disease_index)
                if disease in self.known_diseases:
                    self.known_diseases.pop(self.known_diseases.index(disease))
            elif not doctor and decision(DISEASES_DAILY_LUCK_HEAL_LIST[disease]):
                self.diseases.pop(disease_index)
                if disease in self.known_diseases:
                    self.known_diseases.pop(self.known_diseases.index(disease))

    def __is_only_unhealable_known_diseases(self) -> bool:
        unheal_diseases_number = 0
        for disease in self.diseases:
            if disease in UNHEALABLE_DISEASES:
                unheal_diseases_number += 1
        return len(self.diseases) == unheal_diseases_number


def save_output_to_file(results: dict):
    with open('output.json', 'w+') as f:
        f.write(json.dumps(results))


def simulate_simple_connections() -> dict:

    persons = []

    people_with_diseases_by_day = copy.deepcopy(DISEASES_DETECT_LIST)

    for i in range(POPULATION):
        persons.append(StandardPerson(uuid4()))

    for disease in DISEASES_DETECT_LIST:
        people_with_diseases_by_day[f'{disease} SPIN USER'] = []
        people_with_diseases_by_day[f'{disease} ALL POPULATION'] = []

    get_disease_day_data(people_with_diseases_by_day, persons, 0)

    print(people_with_diseases_by_day)

    save_output_to_file(people_with_diseases_by_day)

    for i in range(TIME_INTERVAL_DAYS):
        # persons = MultiprocSimulation(persons).process_population()

        for person in persons:
            luck = person.luck
            if len(person.known_diseases) > 0:
                luck = luck/2
            if not person.is_already_connected_today and decision(luck):
                list_of_possible_people_to_connect = list(
                        filter(lambda person_to_chose: not person_to_chose.is_already_connected_today and
                               person_to_chose.name != person.name, persons)
                    )

                people_to_connect = list_of_possible_people_to_connect[randint(0, len(list_of_possible_people_to_connect) - 1)]
            else:
                people_to_connect = None

            person.live_a_day(people_to_connect, i > USER_DAYS_DELAY_BEFORE_USE_SPIN)

        for person in persons:
            person.is_already_connected_today = False
            person.is_notified = False

        get_disease_day_data(people_with_diseases_by_day, persons, i)

        persons.pop(randint(0, len(persons) - 1))
        persons.append(StandardPerson(uuid4()))
        # print(people_with_diseases_by_day)

    return people_with_diseases_by_day


def get_disease_day_data(people_with_diseases_by_day, persons, day):
    spin_users = list(filter(lambda person_to_check: person_to_check.is_spin_user, persons))
    simple_people = list(filter(lambda person_to_check: not person_to_check.is_spin_user, persons))
    for disease in people_with_diseases_by_day:
        if 'SPIN USER' in disease:
            if day > USER_DAYS_DELAY_BEFORE_USE_SPIN:
                people_with_diseases_by_day[disease].append(
                    len(
                        list(
                            filter(lambda person_to_check: disease.replace(' SPIN USER', '') in person_to_check.diseases,
                                   spin_users)
                        )
                    ) / len(spin_users) * 100)
            else:
                people_with_diseases_by_day[disease].append(0)
        elif 'ALL POPULATION' in disease:
            people_with_diseases_by_day[disease].append(
                len(list(
                    filter(lambda person_to_check: disease.replace(' ALL POPULATION', '') in person_to_check.diseases,
                           persons)
                )) / len(persons) * 100
            )
        else:
            people_with_diseases_by_day[disease].append(
                len(list(
                    filter(lambda person_to_check: disease in person_to_check.diseases, simple_people)
                )) / len(simple_people) * 100
            )


start_time = time.time()

list_to_print = simulate_simple_connections()

print(list_to_print)

save_output_to_file(list_to_print)

print("--- %s seconds ---" % (time.time() - start_time))

