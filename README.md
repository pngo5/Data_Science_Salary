# Data Science Salary Analysis

## Overview
This project scrapes and analyzes data science job postings from Glassdoor to determine the average salary for data scientists. By collecting and processing job listing data, this tool helps data science professionals understand salary trends and negotiate better compensation packages.

## Repository Contents
- `web_scraping.py`, `web_scraping_v1.py`, `web_scraping_v2.py`: Different versions of the web scraping script
- `cleaning.py`: Script for cleaning and preprocessing the scraped data
- `collection.py`: Data collection utilities
- `glassdoor_jobs_12_20.csv`: Dataset of scraped job listings
- `chromedriver.exe`: Chrome WebDriver executable for Selenium
- `vars_cleaning.spydata`, `vars.spydata`: Saved Spyder variables
- `debug.log`: Log file for debugging

## Setup Instructions

### Prerequisites
- Python 3.x
- Chrome browser
- ChromeDriver (matching your Chrome version)

### Installation Options

#### Option 1: Using pip
```bash
# Update pip first
python -m pip install --upgrade pip

# Install Selenium
pip install selenium

# Install WebDriver Manager (optional)
pip install webdriver_manager --user
```

#### Option 2: Using Anaconda
```bash
# Run as administrator in Anaconda PowerShell
conda install -c conda-forge selenium
```

#### Option 3: Using a Virtual Environment
```bash
# Create virtual environment
py -m virtualenv folder_env

# Activate virtual environment
source folder_env/Scripts/activate

# Check environment settings
which python
which pip

# Install Selenium
pip install selenium

# Verify installation
pip list

# Exit virtual environment when done
deactivate folder_env
```

## Usage Tips
- When using the `get_jobs` function, adjust the delay parameter based on your internet speed
- For slow internet connections, increase delay to 30-50 seconds
- If you encounter `StaleElementReferenceException`, try increasing the delay time
- The Chrome WebDriver version must match your Chrome browser version

## Resources
- [Selenium Tutorial for Scraping Glassdoor](https://towardsdatascience.com/selenium-tutorial-scraping-glassdoor-com-in-10-minutes-3d0915c6d905)
- [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)

## Project Structure
```
Data_Science_Salary/
├── __pycache__/
├── README.md              # Project documentation
├── chromedriver.exe       # Chrome WebDriver executable
├── cleaning.py            # Data cleaning script
├── collection.py          # Data collection utilities
├── debug.log              # Debug log file
├── glassdoor_jobs_12_20.csv # Scraped job data
├── vars.spydata           # Saved Spyder variables
├── vars_cleaning.spydata  # Saved Spyder cleaning variables
├── web_scraping.py        # Main web scraping script
├── web_scraping_v1.py     # Web scraping version 1
└── web_scraping_v2.py     # Web scraping version 2 with bug fixes
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing
Contributions to improve the scraper or extend the analysis are welcome! Please feel free to submit a Pull Request.

## Support and Contact
- **GitHub Repository**: [https://github.com/pngo5/Data_Science_Salary](https://github.com/pngo5/Data_Science_Salary)
- **Report Issues**: [https://github.com/pngo5/Data_Science_Salary/issues](https://github.com/pngo5/Data_Science_Salary/issues)
