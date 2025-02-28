# Documentation - Solar Generator Configurator

## Overview

This project implements a script to automate the process of creating solar generators based on components available in Neosolar's inventory. The script follows the compatibility rules between components (solar panels, inverters, and charge controllers) as specified in the instructions.

## Requirements

The script was developed using Python 3.7+ and requires the following libraries:
- pandas: for data manipulation and CSV export
- json: for reading the product file
- random: for generating random IDs for the generators
- datetime: for obtaining the current date when generating the email

## Project Structure

```
solar_generator_configurator/
│
├── solar_generator_configurator.py  # Main script
├── products.json                    # Product data in stock
├── configured_generators.csv        # Output: Table of configured generators
└── marketing_email.txt              # Output: Email for the marketing team
```

## Logic of Operation

The script follows the following logic:

1. **Data Loading**: The available products are loaded from the JSON file.

2. **Generator Configuration**: Generators are configured following the rules:
   - Each generator is composed of a solar panel, inverter, and charge controller
   - Solar panels must be of the same brand and power rating
   - The combined power of the panels must match the power rating of the inverter and charge controller

3. **Combination Algorithm**:
   - The script iterates through the available inverters
   - For each inverter, it searches for charge controllers with the same power rating
   - For each inverter/charge controller combination, it checks which panels are compatible
   - If the panel's power is divisible by the inverter's power, it calculates the number of panels needed
   - Generates a unique ID for each created generator

4. **Result Export**:
   - Configured generators are exported to a CSV file
   - An email for the marketing team is generated with the number of created generators

## Main Functions

### `load_products(file_path="products.json")`
Loads product data from the specified JSON file.

### `configure_generators(products)`
Creates possible generator combinations based on available products, following compatibility rules.

### `export_to_csv(generators, file_name="configured_generators.csv")`
Exports the list of configured generators to a CSV file.

### `generate_email(generators)`
Generates the content of the email to be sent to the marketing team, including the number of configured generators.

### `export_email_to_pdf(email, file_name="marketing_email.txt")`
Exports the email content to a file (TXT format in this example).

### `main()`
Main function that orchestrates the script's execution flow.

## Limitations

- The current script does not query APIs or databases; it reads data from a local JSON file.
- It does not include advanced input data validation.
- Exports the email as a simple text file instead of PDF.

## Possible Extensions

- Implement product reading directly from an API or database
- Add a logging system for error and activity tracking
- Implement automatic email sending
- Create a web interface for generator visualization and management
- Add authentication and authorization for system access

## Execution

To execute the script, navigate to the project directory and run:

```bash
python solar_generator_configurator.py
```

The script will generate two files:
1. `configured_generators.csv`: Containing the details of all configured generators
2. `marketing_email.txt`: Containing the email to be sent to the marketing team

## Maintenance

To add new products or change compatibility rules:

1. **Add New Products**: Edit the `products.json` file by adding new objects following the same structure.

2. **Change Compatibility Rules**: Modify the `configure_generators()` function in the main script.

## Contact

For questions or maintenance needs, contact the Neosolar engineering team.
