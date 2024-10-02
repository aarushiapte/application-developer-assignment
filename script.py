import json
from datetime import datetime, timedelta
import os

# If the file name is changed to something else, please change the value in the file parameter below to be that file name with the appropriate path
file = "trainings.txt"

# Check if file exists
if not os.path.exists(file):
    raise FileNotFoundError("Please change the file name, this file does not exist.")

with open(file, "r") as file:
    data = json.load(file)


def format_date(dt):
    """
    Converts a string date in the format MM/DD/YYYY to a datetime object.

    Args:
        dt (str): Date string in the format MM/DD/YYYY.

    Returns:
        datetime: A datetime object representing the input date.
    """
    return datetime.strptime(dt, "%m/%d/%Y") if dt else None


def data_preprocessing(data):
    """
    Preprocesses the input data by converting the timestamp and expiration date strings to datetime objects

    Args:
        data (list): List of dictionaries containing data, about the name of the person who took the training and each training
                     having a 'completions' field with 'timestamp' and 'expires'.
    """
    for i in data:
        for training in i["completions"]:
            training["timestamp"] = format_date(training["timestamp"])
            training["expires"] = format_date(training["expires"])


data_preprocessing(data)


# Task 1
def training_count(data):
    """
    Gives each completed training with a count of how many people have completed that training.

    Args:
        data (list): List of dictionaries representing the people and their training completions.

    Returns:
        dict: A dictionary where the keys are the training names and the values are the number of completions.
    """
    final_count = {}
    for record in data:
        latest_completions = {}
        for trainings in record["completions"]:
            completion_date = trainings["timestamp"]
            training = trainings["name"]
            if (
                training not in latest_completions
                or completion_date > latest_completions[training]["timestamp"]
            ):
                latest_completions[training] = {"timestamp": completion_date}

        for training in latest_completions:
            if training not in final_count:
                final_count[training] = 0
            final_count[training] += 1

    return final_count


# Task 2
def people_trainings_year(data, trainings_given, fiscal_year):
    """
    Finds list of people who completed specific trainings in a given fiscal year.

    Args:
        data (list): List of dictionaries representing the people and their training completions
        trainings_given (list): List of training names to filter on
        fiscal_year (int): The fiscal year to filter the training

    Returns:
        dict: A dictionary where the keys are the training names and the values are lists of people who completed them during the fiscal year.
    """
    start_date = datetime(fiscal_year - 1, 7, 1)
    print(start_date)
    end_date = datetime(fiscal_year, 6, 30)

    people_list = {}

    for record in data:
        latest_completions = {}
        for trainings in record["completions"]:
            completion_date = trainings["timestamp"]
            training = trainings["name"]
            if (
                training not in latest_completions
                or completion_date > latest_completions[training]["timestamp"]
            ):
                latest_completions[training] = {"timestamp": completion_date}

        for training in latest_completions:
            completion_date = latest_completions[training]["timestamp"]
            if (
                training in trainings_given
                and start_date <= completion_date <= end_date
            ):
                if training not in people_list:
                    people_list[training] = []
                people_list[training].append(record["name"])

    return people_list


# Task 3
def expired_trainings(data, dt):
    """
    Finds names of people and the trainings that have expired or are about to expire within 30 days of the given expiry date

    Args:
        data (list): List of dictionaries representing the people and their training completions.
        dt (datetime): The reference date to check for expiration.

    Returns:
        dict: A dictionary where the keys are the people's names, and the values are lists of trainings that have expired or will expire soon.
    """
    will_expire = dt + timedelta(days=30)

    expired_list = {}
    for record in data:
        latest_completions = {}
        for trainings in record["completions"]:
            completion_date = trainings["timestamp"]
            training = trainings["name"]
            if (
                training not in latest_completions
                or completion_date > latest_completions[training]["timestamp"]
            ):
                latest_completions[training] = {
                    "timestamp": completion_date,
                    "expires": trainings.get("expires"),
                }

        for training in latest_completions:
            expiry_date = latest_completions[training]["expires"]
            if expiry_date:
                if expiry_date < dt:
                    status = "Expired"
                elif expiry_date <= will_expire:
                    status = "Expires soon"
                else:
                    continue
                if record["name"] not in expired_list:
                    expired_list[record["name"]] = []
                expired_list[record["name"]].append(
                    {
                        "training": training,
                        "expires": (
                            expiry_date.strftime("%m/%d/%Y") if expiry_date else None
                        ),
                        "status": status,
                    }
                )
    return expired_list


trainings_given = [
    "Electrical Safety for Labs",
    "X-Ray Safety",
    "Laboratory Safety Training",
]
fiscal_year = 2024
dt = datetime(2023, 10, 1)

completed_training_count = training_count(data)
people_completing_training = people_trainings_year(data, trainings_given, fiscal_year)
expired = expired_trainings(data, dt)

# Saving the results in 3 JSON output files

# Task 1 Output
with open("task_1.json", "w") as file:
    json.dump(completed_training_count, file)

# Task 2 Output
with open("task_2.json", "w") as file:
    json.dump(people_completing_training, file)

# Task 3 Output
with open("task_3.json", "w") as file:
    json.dump(expired, file)

print("Success!")
