# Singapore Postal Code to Address

This Python CLI tool uses the One Map SG API to batch process postal codes and collect their address information.

## Usage

The CSV file inputted must have the heading "Postal Codes" for the column containing the postal codes. An example can be seen in `postalcodes.csv`.

    usage: main.py [-h] [-i INPUT] [-o OUTPUT]

    Converting Singapore Postal Code into Addresses.

    options:
      -h, --help            show this help message and exit
      -i INPUT, --input INPUT
                            The path to the CSV file with postal code data. Default: `postalcodes.csv`
      -o OUTPUT, --output OUTPUT
                            The path to the output CSV. Default: `postalcodeswithaddress.csv`.