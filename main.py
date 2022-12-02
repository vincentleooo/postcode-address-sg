import argparse
from datetime import datetime
import requests
import logging
import pandas as pd
import os
import errno
import swifter
import sys


def import_csv(path):

    logging.info(f"Importing CSV from {path}.")

    if not os.path.exists(path):
        logging.error(f"Importing CSV failed. Check if the path '{path}' is correct.")
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

    postal_df = pd.read_csv(path, dtype=str)
    logging.info(f"Success. First five lines of the CSV:\n\n{postal_df.head(5)}\n")

    return postal_df


def find_address(postcode):

    try:
        response = requests.get(
            f"https://developers.onemap.sg/commonapi/search/?searchVal={postcode}&returnGeom=Y&getAddrDetails=Y&pageNum=1"
        )
        results = response.json()["results"]
        logging.debug(results)
        for i in results:
            if i["POSTAL"] == postcode:
                return i["ADDRESS"]
        logging.warning(f"No address found for {postcode}")
    except requests.exceptions.HTTPError as errh:
        logging.error(f"{errh} for {postcode}")
        return f"HTTP error. Check the log files at logs/{START_DATETIME}.log for more information."
    except requests.exceptions.ConnectionError as errc:
        logging.error(f"{errc} for {postcode}")
        return f"Connection error. Check the log files at logs/{START_DATETIME}.log for more information."
    except requests.exceptions.Timeout as errt:
        logging.error(f"{errt} for {postcode}")
        return f"Timeout error. Check the log files at logs/{START_DATETIME}.log for more information."
    except requests.exceptions.RequestException as err:
        logging.error(f"{err} for {postcode}")
        return f"Request exception error. Check the log files at logs/{START_DATETIME}.log for more information."
    except Exception as err:
        logging.error(f"Unexpected {err=}, {type(err)=} for {postcode}")
        return f"Unexpected error. Check the log files at logs/{START_DATETIME}.log for more information."

    return "NO ADDRESS FOUND"


def main():

    parser = argparse.ArgumentParser(
        description="Converting Singapore Postal Code into Addresses."
    )
    parser.add_argument(
        "-i",
        "--input",
        default="postalcodes.csv",
        type=str,
        help="The path to the CSV file with postal code data. Default: `postalcodes.csv`",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="postalcodeswithaddress.csv",
        type=str,
        help="The path to the output CSV. Default: `postalcodeswithaddress.csv`.",
    )

    opt = parser.parse_args()

    INPUT_PATH = opt.input
    OUTPUT_PATH = opt.output

    if not os.path.isdir("logs"):
        os.mkdir("logs")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(f"logs/{START_DATETIME}.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    swifter.set_defaults(progress_bar_desc="Looking for Addresses")
    postal_df = import_csv(INPUT_PATH)
    postal_df["Address"] = postal_df["Postal Codes"].swifter.apply(find_address)
    print("")
    logging.info("Finished job. Exiting...")
    postal_df.to_csv(OUTPUT_PATH)


if __name__ == "__main__":
    START_DATETIME = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    main()
