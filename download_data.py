import pm

if __name__ == '__main__':
    LogLevel = pm.settings.LogLevel
    pm.settings.setup_logger(console_log_level=LogLevel.INFO,
                             file_log_level=LogLevel.DEBUG)

    download_params = {
        "domains": ["air", "meteo"],
        "years": range(1980, 2018)
    }

    # check_data_already_downloaded()
    pm.oasi.download_oasi_data(custom_params=download_params)
