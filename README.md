# Covid-tests report

In this repository can be found all the necessary modules in order to generate a report about the covid-tests which were taken in a specific date range. The data is retrieved from a PostgreSQL database via a cli application.   


# Information

* A user can create a report for a specific date range by using the CLI application. The report is exported by default to a csv format file. The user has the option to convert it to microsoft excel or pdf file and the option to send an email with the report as an attachment.  
* The generated report contains information about the following:  
  * date and time of appointment  
  * name of the test location  
  * type of the test (pcr/antigen)  
  * number of tests (grouped by date, location and test type)  
  * number of not taken tests (grouped by date, location and type of test)  

# Requirements

* The whole application can be run by typing the following commands (a virtual environment is suggested but not mandatory):  
`pip install -r requirements`  
`sudo apt-get install wkhtmltopdf`   
* The next step is to define the environmental variables. We use those for the database and email settings. The email settings refer to a gmail account.  
  * EMAIL_ADDRESS  
  * EMAIL_PASSWORD  
  * POSTGRES_HOST  
  * POSTGRES_DB  
  * POSTGRES_USER  
  * POSTGRES_PASS  

# How to run

* We can get a report in a csv file based on a date range and save it to a specific path by typing:  
`python3 cli.py <starting date> <ending date> <path_to_save_file>`  
Dates and path are positional arguments and are mandatory. The dates must be in yyyy-mm-dd format and the path must be absolut.  

* In order to convert the csv file or email it we have to use the optional arguments  
  * convert to excel  
  `python3 cli.py <starting date> <ending date> <path> -toexcel`  
  * convert to pdf  
  `python3 cli.py <starting date> <ending date> <path> -topdf`  
  * convert to excel and email file  
  `python3 cli.py <starting date> <ending date> <path> -eexcel <email_address>`  
  * convert to pdf and email file  
  `python3 cli.py <starting date> <ending date> <path> -epdf <email_address>`  

# How to run tests  

The tests of the application have been written by using unittest library and can be run by typing the following command:  
`python3 -m unittest tests`  

# Cronjob

We can schedule a cronjob (by using the crontab of linux) in order to receive an email with the report as an excel attachment at the time we want. We type the next commands in a terminal. The example refers to a report which is generated at every Monday at 06:00 and extracts the data of the previous week (Monday to Sunday).  

Open the linux crontab for editing  
`crontab -e`  
Add the cronjob  
`0 6 * * 1 python3 /<path_to_python_module>/cli.py $(date --date="1 week ago" "+\%Y-\%m-\%d") $(date --date="yesterday" "+\%Y-\%m-\%d") <path_to_save_file> -eexcel <email_address>`  
