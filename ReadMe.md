# Web Scraper Assignment

## Overview
This project contains a web scraper that extracts data from specific websites and saves it to a MongoDB database. It includes robust error handling, logging, and performance optimizations.

## Requirements
- MongoDB
- Google Chrome (for Selenium)
- The executable file (`web_scraper.exe`)
- Create a Virtual Enviroment download the required packages using requirements.txt file by executing this command
   `pip install -r requirements.txt`. 


## Setup Instructions

### MongoDB Installation
1. **Install MongoDB:**
   - Follow the official guide for your operating system: [MongoDB Installation](https://docs.mongodb.com/manual/installation/)

2. **Start MongoDB Server:**
   - Ensure MongoDB is running. You can start the MongoDB server using:
     ```sh
     mongod --dbpath /path/to/your/db
     ```
   - MongoDB should be accessible at `localhost:27017`.

### Running the Application: 
1. **Clone Repository**
   - Clone the repository as `git clone https://github.com/hrishi483/Vakil-Desk-Assignement`.

2. **Run the Executable:**
   - Navigate to the `dist` directory and double-click `web_scraper.exe` or run it from the command line:
     ```sh
     ./dist/web_scraper.exe
     ```

3. **Ensure Dependencies:**
   - Make sure Google Chrome is installed, as the script uses Selenium for web scraping.

### Log File
- The script logs errors and exceptions to `scraping.log` in the same directory as the executable. Check this file if you encounter any issues.

## Description
The script scrapes data from three specific websites and stores the data in MongoDB:

1. **Website 1:**
   - URL: `https://www.scrapethissite.com/pages/ajax-javascript/#2015`
   - Database: `link1`
   - Collection: `oscars`

2. **Website 2:**
   - URL: `https://www.scrapethissite.com/pages/forms/`
   - Database: `link2`
   - Collection: `teams`

3. **Website 3:**
   - URL: `https://www.scrapethissite.com/pages/advanced/`.
   - Stores raw HTML content in a text file `Website3.txt` (Since the instruction for this website was not clearly specified).

### Script Functions
- The script includes robust error handling and logs errors to a log file for debugging purposes.
- Performance optimization techniques such as parallel scraping and random delays are implemented to improve scraping performance and minimize load on the target website's servers.
- The script prints success messages to the console during execution.

## Submission Structure
clone the git folder with the file structure as follows.<br>
    ├── dist/                    
    │   ├── web_scraper.exe      
    ├── web_scraper.py           
    ├── scraping.log             
    ├── web_scraper.spec         
 

## Contact Information
For any issues or questions, please contact *Hrishikesh Ravindra Karande* at [210010020@iitdh.ac.in].
