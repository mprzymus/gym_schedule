import functools
import itertools
from io import StringIO

import matplotlib.pyplot as plt

from app.service.date_service import generate_dates_list
from app.service.exercise_usage_service import find_exercises_for_day, find_exercise_for_day_by_name
from app.strings import *


class UserChartService:
    def __init__(self, user, period_start, period_end):
        self.user = user
        self.dates = generate_dates_list(period_start, period_end)

    def generate_general_chart(self):
        x, y = self.prepare_data(find_exercises_for_day)
        return create_chart(x, y, GENERAL_CHART_TITLE)

    def prepare_data(self, fun):
        days = []
        data = []
        for day in self.dates:
            exercises = fun(day, self.user)
            weight_sum = fold_left_exercises(exercises)
            if weight_sum != 0:
                days.append(day)
                data.append(weight_sum)
        data_found_size = len(days)
        '''if data_found_size == 0:
            days = self.dates
            data = [0] * len(self.dates)'''
        return days, data

    def generate_chart_for_exercise(self, name):
        x, y = self.prepare_data(lambda day, user: find_exercise_for_day_by_name(day, user, name))
        return create_chart(x, y, EXERCISE_CHART_TITLE % name)


def create_chart(x, y, tittle=''):
    if len(x) != 0:
        fig = plt.figure()
        plt.plot(x, y, linestyle="--", marker="o")
        plt.xticks(rotation=20)
        plt.title(tittle)
        img_data = StringIO()
        fig.savefig(img_data, format='svg')
        img_data.seek(0)
        data = img_data.getvalue()
        return data
    return NO_DATA % tittle

def fold_left_exercises(exercises):
    return functools.reduce(lambda acc, ex: ex.weight * ex.repetitions + acc, exercises, 0)
