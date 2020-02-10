import copy
import os
from random import randint, random
from statistics import mean

from app.simulation_settings import DISEASES_LIST, SPIN_USER_CONNECT_SIMPLE_USER_LUCK, DISEASES_LUCK_LIST, \
    DISEASES_DETECT_LIST, REACT_LUCKY, VACCINATION, DISEASES_LUCK_HEAL_LIST, DISEASES_DAILY_LUCK_HEAL_LIST, \
    UNHEALABLE_DISEASES
from app.utils import decision


class StandardPerson:

    def __init__(self):
        self.luck = randint(27, 500) / 10000
        self.test_time_interval = randint(160, 1800)
        self.last_test_was = randint(randint(1, randint(2, 30)), int(self.test_time_interval / randint(1, 3)))
        self.is_already_connected_today = bool(randint(0, 1))
        self.was_infected_today = []
        self.is_connected_with_spin_user = False
        self.is_connected_with_simple_user = False
        self.diseases = []
        self.count_of_doctor_visits_per_year = []
        self.count_of_doctor_visits = 0
        self.__count_of_useful_doctor_visits = 0
        self.is_notified = False
        self.known_diseases = []
        self.__spin_partner_list = []
        self.is_spin_user = decision(float(os.getenv('SPIN_USERS')))
        self.__vaccination = []
        self.__vaccination_try()
        self.__days_before_found_disease = {}
        self.__days_before_found_disease_avg = copy.deepcopy(DISEASES_DETECT_LIST)
        self.__count_of_notifications = 0
        self.__count_of_useful_notifications = 0

        for disease in DISEASES_LIST:
            if len(self.diseases) > 14:
                break
            if decision(DISEASES_LIST.get(disease)):
                self.diseases.append(disease)

        self.__count_days_before_found()

    def get_percent_of_useful_doctor_visits(self):
        if sum(self.count_of_doctor_visits_per_year) > 0:
            return (self.__count_of_useful_doctor_visits / sum(self.count_of_doctor_visits_per_year)) * 100
        else:
            return 0

    def get_percent_of_useful_notifications(self):
        return (self.__count_of_useful_notifications / self.__count_of_notifications) * 100

    def is_already_have_notifications(self):
        return self.__count_of_notifications > 0

    def get_days_before_found_disease_avg(self) -> (str, int):
        output_days = copy.deepcopy(self.__days_before_found_disease_avg)
        for key in output_days:
            if len(output_days[key]) > 0:
                yield key, mean(output_days[key])

    def live_a_day(self, person_to_connect, start_use_spin, new_year=False):
        if person_to_connect is not None:
            if not self.is_spin_user or person_to_connect.is_spin_user or decision(SPIN_USER_CONNECT_SIMPLE_USER_LUCK):
                person_to_connect.connect(self, start_use_spin)
                self.connect(person_to_connect, start_use_spin)
        self.__count_days_before_found()
        self.last_test_was -= 1
        self.check_is_need_go_to_doctor()
        if new_year:
            self.count_of_doctor_visits_per_year.append(self.count_of_doctor_visits)
            self.count_of_doctor_visits = 0
        if len(self.known_diseases) > 0 and not self.__is_only_unhealable_known_diseases:
            self.__try_to_heal()

    def connect(self, person_to_connect, start_use_spin):
        if person_to_connect.is_spin_user:
            self.is_connected_with_spin_user = True
        else:
            self.is_connected_with_simple_user = True
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
                    self.was_infected_today.append(connect_disease)
        self.is_already_connected_today = True

    def notified(self, from_who):
        self.is_notified = True
        self.__count_of_notifications += 1
        for partner in self.__spin_partner_list:
            if partner != from_who and not partner.is_notified:
                partner.notified(self)
        self.__clear_spin_partner_list()
        if decision(REACT_LUCKY):
            self.__check_is_need_to_start_day_counting()
            self.check_is_need_go_to_doctor(is_spin=True)

    def check_is_need_go_to_doctor(self, is_spin=False):
        if self.last_test_was < 1 or is_spin:
            self.count_of_doctor_visits += 1
            self.last_test_was = self.test_time_interval
            if len(self.diseases) > 0 and any(disease not in self.known_diseases for disease in self.diseases):
                if is_spin:
                    self.__count_of_useful_notifications += 1
                self.__count_of_useful_doctor_visits += 1
            if self.is_spin_user and len(self.diseases) > 0 and not is_spin:
                for partner in self.__spin_partner_list:
                    partner.notified(self)
                self.__clear_spin_partner_list()
            self.__try_to_heal(doctor=True)

    def __vaccination_try(self):
        for disease in VACCINATION:
            if decision(VACCINATION[disease]):
                self.__vaccination.append(disease)

    def __check_is_need_to_start_day_counting(self):
        for disease in self.diseases:
            if disease not in self.known_diseases and disease not in self.__days_before_found_disease:
                self.__days_before_found_disease[disease] = 0

    def __count_days_before_found(self):
        for disease in self.diseases:
            if disease not in self.known_diseases:
                if disease in self.__days_before_found_disease:
                    self.__days_before_found_disease[disease] += 1
                else:
                    self.__days_before_found_disease[disease] = 0

    def __clear_days_before_found(self, disease):
        try:
            self.__days_before_found_disease_avg[disease].append(self.__days_before_found_disease.pop(disease))
        except KeyError as e:
            print(self.__days_before_found_disease)
            print(self.__days_before_found_disease_avg)
            print(self.diseases)
            print(self.known_diseases)
            raise e

    def __clear_spin_partner_list(self):
        self.__spin_partner_list = []

    def __try_to_heal(self, doctor=False):
        for disease_index, disease in enumerate(self.diseases):
            if doctor:
                if disease not in self.known_diseases:
                    self.__clear_days_before_found(disease)
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
        return all(disease in UNHEALABLE_DISEASES for disease in self.known_diseases)
