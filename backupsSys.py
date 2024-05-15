#  ____             _                      ____                      ____              _             _     _       _      ___ ____  _  _    __
# | __ )  __ _  ___| | ___   _ _ __  ___  / ___| _   _ ___          | __ ) _   _    __| | __ ___   _(_) __| | __ _| |__  ( _ )___ \| || |  / /_
# |  _ \ / _` |/ __| |/ / | | | '_ \/ __| \___ \| | | / __|  _____  |  _ \| | | |  / _` |/ _` \ \ / / |/ _` |/ _` | '_ \ / _ \ __) | || |_| '_ \
# | |_) | (_| | (__|   <| |_| | |_) \__ \  ___) | |_| \__ \ |_____| | |_) | |_| | | (_| | (_| |\ V /| | (_| | (_| | |_) | (_) / __/|__   _| (_) |
# |____/ \__,_|\___|_|\_\\__,_| .__/|___/ |____/ \__, |___/         |____/ \__, |  \__,_|\__,_| \_/ |_|\__,_|\__, |_.__/ \___/_____|  |_|  \___/
#                             |_|                |___/                     |___/                             |___/

# STATUS CODES:
# 1 - Settings file bad formatted.
# 2 - Illegal Arguments on config file.

import sys
import datetime
import calendar

fill_int_wildcard = 999


def load_config_file(config_file_path="/etc/backupSys/backupSys-settings.txt"):
    try:
        configuration_file = open(config_file_path, "r")
    except OSError:
        print("No se pudo cargar el fichero de configuración.")
        sys.exit()

    return configuration_file


def get_config_settings(configuration_file):
    settings = {
        28: {"completas": [], "diferenciales": [], "incrementales": []},
        29: {"completas": [], "diferenciales": [], "incrementales": []},
        30: {"completas": [], "diferenciales": [], "incrementales": []},
        31: {"completas": [], "diferenciales": [], "incrementales": []},
    }

    sources_backup = []
    destinations_backup = []
    log_directory = ""

    month_type = 0
    total_found, differential_found, incremental_found = False, False, False

    for line in configuration_file:
        if line.startswith("#") or line.replace(" ", "").replace("\n", "") == "":
            continue

        if line.find("28:") != -1:
            month_type = 28
            total_found, differential_found, incremental_found = False, False, False
        elif line.find("29:") != -1:
            month_type = 29

            if not total_found or not differential_found or not incremental_found:
                sys.exit(1)

            total_found, differential_found, incremental_found = False, False, False
        elif line.find("30:") != -1:
            month_type = 30

            if not total_found or not differential_found or not incremental_found:
                sys.exit(1)

            total_found, differential_found, incremental_found = False, False, False
        elif line.find("31:") != -1:
            month_type = 31

            if not total_found or not differential_found or not incremental_found:
                sys.exit(1)

            total_found, differential_found, incremental_found = False, False, False

        if line.find("completas:") != -1:
            args = line.replace(" ", "").replace("\n", "").split(":")[1].replace("[", "").replace("]", "").split(",")
            total_found = True

            for arg in args:
                if not arg.startswith("D") and arg != "R*":
                    sys.exit(2)

                actual_arg = arg.replace("D", "")
                if actual_arg.find("R*") == -1:
                    day = int(actual_arg)
                else:
                    day = fill_int_wildcard

                if 1 <= day <= month_type or day == fill_int_wildcard:
                    settings[month_type]["completas"].append(day)
                else:
                    sys.exit(2)

        elif line.find("diferenciales:") != -1:
            args = line.replace(" ", "").replace("\n", "").split(":")[1].replace("[", "").replace("]", "").split(",")
            differential_found = True

            for arg in args:
                if not arg.startswith("D") and arg != "R*":
                    sys.exit(2)

                actual_arg = arg.replace("D", "")
                if actual_arg.find("R*") == -1:
                    day = int(actual_arg)
                else:
                    day = fill_int_wildcard

                if 1 <= day <= month_type or day == fill_int_wildcard:
                    settings[month_type]["diferenciales"].append(day)
                else:
                    sys.exit(2)

        elif line.find("incrementales:") != -1:
            args = line.replace(" ", "").replace("\n", "").split(":")[1].replace("[", "").replace("]", "").split(",")
            incremental_found = True

            for arg in args:
                if not arg.startswith("D") and arg != "R*":
                    sys.exit(2)

                actual_arg = arg.replace("D", "")
                if actual_arg.find("R*") == -1:
                    day = int(actual_arg)
                else:
                    day = fill_int_wildcard

                if 1 <= day <= month_type or day == fill_int_wildcard:
                    settings[month_type]["incrementales"].append(day)
                else:
                    sys.exit(2)

        if line.find("rutas_copiar:") != -1:
            args = line.replace(" ", "").replace("\n", "").split(":")[1].replace("[", "").replace("]", "").split(",")
            for arg in args:
                arg = arg.replace('"', "")
                sources_backup.append(arg)

        elif line.find("rutas_destino:") != -1:
            args = line.replace(" ", "").replace("\n", "").split(":")[1].replace("[", "").replace("]", "").split(",")
            for arg in args:
                arg = arg.replace('"', "")
                destinations_backup.append(arg)

        elif line.find("directorio_logs:") != -1:
            log_directory = str(line.replace(" ", "").replace("\n", "").split(":")[1].replace('"', ""))

    configuration_file.close()
    return settings, sources_backup, destinations_backup, log_directory


def build_backup_calendar(settings, date):
    timetable = [
        [['X', 'N'], ['X', 'N'], ['X', 'N'], ['X', 'N'], ['X', 'N'], ['X', 'N'], ['X', 'N']],
        [['X', 'N'], ['X', 'N'], ['X', 'N'], ['X', 'N'], ['X', 'N'], ['X', 'N'], ['X', 'N']],
        [['X', 'N'], ['X', 'N'], ['X', 'N'], ['X', 'N'], ['X', 'N'], ['X', 'N'], ['X', 'N']],
        [['X', 'N'], ['X', 'N'], ['X', 'N'], ['X', 'N'], ['X', 'N'], ['X', 'N'], ['X', 'N']],
        [['X', 'N'], ['X', 'N'], ['X', 'N'], ['X', 'N'], ['X', 'N'], ['X', 'N'], ['X', 'N']],
        [['X', 'N'], ['X', 'N'], ['X', 'N'], ['X', 'N'], ['X', 'N'], ['X', 'N'], ['X', 'N']],
    ]

    date = "01-" + date
    today = datetime.datetime.strptime(date, '%d-%m-%Y')
    first_day_month = today.replace(day=1).weekday()
    min_column = first_day_month

    actual_day = 1
    max_month_day = calendar.monthrange(today.year, today.month)[1]

    fill_with_total_backups = False
    fill_with_diff_backups = False
    fill_with_incr_backups = False

    if fill_int_wildcard in settings[max_month_day]["completas"]:
        fill_with_total_backups = True
    elif fill_int_wildcard in settings[max_month_day]["diferenciales"]:
        fill_with_diff_backups = True
    elif fill_int_wildcard in settings[max_month_day]["incrementales"]:
        fill_with_incr_backups = True

    row = 0
    column = min_column
    while row < len(timetable) and actual_day <= max_month_day:
        while column < len(timetable[row]) and actual_day <= max_month_day:
            if actual_day <= max_month_day:
                timetable[row][column][0] = actual_day

                if actual_day in settings[max_month_day]["completas"]:
                    timetable[row][column][1] = 'T'
                elif actual_day in settings[max_month_day]["diferenciales"]:
                    timetable[row][column][1] = 'D'
                elif actual_day in settings[max_month_day]["incrementales"]:
                    timetable[row][column][1] = 'I'
                elif fill_with_total_backups:
                    timetable[row][column][1] = 'T'
                elif fill_with_diff_backups:
                    timetable[row][column][1] = 'D'
                elif fill_with_incr_backups:
                    timetable[row][column][1] = 'I'

                actual_day += 1
            column += 1

        column = 0
        row += 1

    return timetable


config_file = load_config_file()
backup_type_settings, backup_source_paths, backup_destination_paths, log_path = get_config_settings(config_file)

today_date = datetime.datetime.today().strftime('%m-%Y')
# today_date = "02-2024"
today_formatted = datetime.datetime.strptime("01-" + today_date, '%d-%m-%Y')
month_length = calendar.monthrange(today_formatted.year, today_formatted.month)[1]

backup_calendar = build_backup_calendar(backup_type_settings, today_date)


print()
print('\t\t\t\t\t\t\t  CALENDARIO [' + str(today_formatted.month) + "-" + str(today_formatted.year) + "] [" + str(month_length) + "]")
print()
print(*["L", "M", "X", "J", "V", "S", "D"], sep="\t\t\t")
for r in backup_calendar:
    for c in r:
        print(str(c[0]) + "\t[" + c[1] + "]", end="\t\t")
    print()

print()
print("Config Mes [" + str(month_length) + "]: " + str(backup_type_settings[month_length]))
