import json
import os

import requests
from simple_logger import Logger

import pm


def write_csv_file(output_file: str, locations: requests.Response) -> None:
    with open(output_file, 'wb') as file:  # open as block write.
        for chunk in locations.iter_content(chunk_size=4096):
            if chunk:  # filter out keep-alive new chunks
                file.write(chunk)
        file.flush()  # Afterall, force data flush into output file (optional)


def download_oasi_data(custom_params: dict = None) -> None:
    """Downloads all the data specified in the passed argument to the data folder.

    :Example:

        .. code-block:: python

            domains = ['meteo', 'air']
            years = range(2000, 2018)
            download_params = {
                "domains": domains,
                "years": years
            }
            download_oasi_data(download_params)

    :param custom_params: Dictionary of custom params to be used to download the data.
    """
    if custom_params is None:
        custom_params = {}

    params = {
        "domains": ["air", "meteo"],
        "years": range(2010, 2018),
        "data_directory": pm.Settings.data_dir,
        "overwrite": False
    }
    params.update(custom_params)

    # Log the parameters being used.
    logger_msg = "Downloading oasi data with following params:"
    align = max([len(name) for name in params]) + 4
    for name, value in params.items():
        logger_msg += "\n{:>{align}}: {}".format(name, value, align=align)
    Logger.info(msg=logger_msg)

    domains = params["domains"]
    years = params["years"]
    data_directory = params["data_directory"]
    overwrite = params["overwrite"]

    if len(domains) == 0:
        raise RuntimeError("Domains passed to `download_oasi_data` is empty!")

    if not os.path.exists(data_directory):
        os.makedirs(data_directory, exist_ok=True)

    for dom in domains:
        Logger.info("Downloading domain {}".format(dom))
        dom_path = os.path.join(data_directory, dom)
        os.makedirs(dom_path, exist_ok=True)
        domain = requests.get('http://www.oasi.ti.ch/web/rest/parameters?domain=' + dom)
        domain_features = json.loads(domain.text)

        for feature in domain_features:
            feature_path = os.path.join(dom_path, feature['code'])
            Logger.info("Downloading feature {}/{}".format(dom, feature["code"]))
            os.makedirs(feature_path, exist_ok=True)

            # Get locations associated to the features.
            locations = requests.get('http://www.oasi.ti.ch/web/rest/locations?domain=' +
                                     dom + '&parameter=' + feature['code'])

            locations = json.loads(locations.text)

            for loc in locations:
                loc_path = os.path.join(feature_path, loc['name'])
                Logger.debug("Downloading {}/{}/{}".format(
                    dom, feature["code"], loc["name"]))
                os.makedirs(loc_path, exist_ok=True)
                for year in years:
                    csv_file_name = os.path.join(loc_path, str(year) + '.csv')

                    # If the file already exists, then continue to next data without
                    # overwriting.
                    if not overwrite and os.path.exists(csv_file_name):
                        continue
                    locations = requests.get(
                        'http://www.oasi.ti.ch/web/rest/measure/csv?domain=' +
                        dom + '&resolution=h&parameter=' + feature['code'] + '&from=' +
                        str(year) + '-01-01&to=' + str(year) + '-12-31&location=' +
                        loc['code'])

                    first_line = locations.text.split('\n', 1)[0]
                    if first_line == '# GENERALE':
                        write_csv_file(csv_file_name, locations)
