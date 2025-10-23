# Ghana Post GPS API

A simple python code for looking up Ghana Post GPS codes, converting coordinates to GPS addresses, and validating GPS addresses. Features a Python Flask backend to handle CORS and API requests.

##  Features

- **GPS Code Lookup** - Enter a GPS code (e.g., CG-1234-5678) to get detailed location information
- **Coordinates to GPS** - Convert latitude/longitude coordinates to Ghana Post GPS addresses
- **Address Validation** - Validate and format GPS addresses


##  Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the program**
   ```bash
   python main.py
   ```


That's it! The Python handles the requests to the Ghana Post GPS API.


##Usage Examples

### GPS Code Lookup
- Use the `get_location` function
- Get: Full location details including region, district, area, and coordinates

### Coordinates to GPS
- use the`get_address` function
- Get: GPS address for the location

### Validate Address
- Use the `is_valid_gp_address` function
- Get: Validation status and formatted address

### API
- **Ghana Post GPS API** - Location data


## License

This project is open source and available under the MIT License.

## Contributing

Contributions, issues, and feature requests are welcome!

## Credits

Based on the Ghana Post GPS Python implementation. Converted from a paper by Justice Owusu Agyemang [here](https://www.researchgate.net/publication/344133922_Reverse_Engineering_GhanaPostGPS_Mobile_Application_to_Create_an_Application_Programming_Interface_for_Local_Developers).

---
