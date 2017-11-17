import os
from datetime import datetime
from typing import List

from .settings import Location, Parameter


class OasiLoadParameters:
    def __init__(self, location: Location, param_list: list, start_date: datetime,
                 end_date: datetime):
        self.location = location
        self.param_list = param_list
        self.start_date = start_date
        self.end_date = end_date


def __csv_contains_date(csv_file_name: str,
                        start_date: datetime, end_date: datetime) -> bool:
    assert (csv_file_name.endswith(".csv"))
    csv_file_name = csv_file_name[:-4]

    assert (len(csv_file_name) == 4 or len(csv_file_name) == 9)
    if "-" in csv_file_name:
        start_date_file, end_date_file = csv_file_name.split("-")
        start_date_file = datetime(day=1, month=1, year=int(start_date_file))
        end_date_file = datetime(day=31, month=12, year=int(end_date_file))
    else:
        year = int(csv_file_name)
        start_date_file = datetime(day=1, month=1, year=year)
        end_date_file = datetime(day=31, month=12, year=year)

    return start_date_file <= start_date <= end_date_file or \
           start_date_file <= end_date <= end_date_file


def __parse_csv_file(csv_file_name: str,
                     start_date: datetime, end_date: datetime) -> tuple:
    pass


def load_measurements(parameters: OasiLoadParameters, data_path: str):
    param_list = parameters.param_list  # type: List[Parameter]
    measurements = {}

    for param in param_list:
        param_code = param.code
        location = parameters.location.name + "_" + parameters.location.code

        directory = os.path.join(os.path.join(data_path, param_code), location)
        csv_files = [file for file in os.listdir(directory) if file.endswith(".csv")]
        csv_files = sorted(csv_files)

        param_measurements = []
        for csv_file in csv_files:
            if __csv_contains_date(csv_file_name=csv_file,
                                   start_date=parameters.start_date,
                                   end_date=parameters.end_date):
                current_measurement = __parse_csv_file(csv_file_name=csv_file,
                                               start_date=parameters.start_date,
                                               end_date=parameters.end_date)
                param_measurements.append(current_measurement)

        measurements[param_code] = param_measurements
