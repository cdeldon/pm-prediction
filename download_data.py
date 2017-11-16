import os

import pm


def check_data_already_downloaded(data_dir: str = None) -> None:
    """Checks if the data directory passed as argument is empty or not.

    In case the data directory passed as argument is not empty, the process terminates
    raising a `FileExistsError`.

    :param data_dir: Absolute path to the data directory to be checked. If the
    parameter is not set, then the path returned by
    :attr:`Settings.data_dir <pm.settings.__Settings.data_dir>` is used.
    """

    if data_dir is None:
        data_dir = pm.Settings.data_dir

    if os.path.exists(data_dir):
        dirs_in_data = os.listdir(data_dir)
        if len(dirs_in_data) > 0:
            err_msg = "\nData directory {} is not empty: files found:".format(data_dir)
            for file in dirs_in_data:
                err_msg += " \n\t- {}".format(file)

            raise FileExistsError(err_msg)


if __name__ == '__main__':
    LogLevel = pm.settings.LogLevel
    pm.settings.setup_logger(console_log_level=LogLevel.INFO,
                             file_log_level=LogLevel.DEBUG)

    # check_data_already_downloaded()
    pm.download.download_oasi_data()
