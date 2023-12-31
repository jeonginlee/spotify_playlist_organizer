# spotify_playlist_organizer
## Description:
TODO

## Project Setup:
1. Clone project repository:
```
git clone https://github.com/jeonginlee/spotify_playlist_organizer.git <project name>
```
2. Install [Python](https://www.python.org/downloads/)
3. Open up to project directory in terminal
4. Using [virtualenv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) to manage environment and packages
    
    a. Setup: 
    ```
    py -m venv spotify_env
    ```
    b. Activate: 
    ```
    spotify_env/Scripts/activate
    ```
    b. Install packages: 
    ```
    pip install -r requirements.txt
    ```
5. Install [MySQL Server](https://dev.mysql.com/downloads/mysql/). [MySQL Workbench](https://dev.mysql.com/doc/workbench/en/wb-installing.html) can also be downloaded for ease during development. 
6. Setup connection to database with name "localhost" and user/password "root"
7. Create database and tables
    ```
	mysql -u root -p
    -> source C:/Users/jeong/projects/spotify_playlist_organizer/create_tables.sql
    ```
8. Run main module for Flask
    ```
    py app.py
    ```
9. Navigate to http://localhost:3000/ to start authorization workflow

Authorization managed through [Spotify Web API services](https://developer.spotify.com/documentation/web-api/tutorials/code-flow)
Cookies are used for reauthorization so you may need to clear it to retrigger authorization if needed
```
Chrome settings -> Privacy and Security -> See all data and permissions -> search for Spotify and delete cookies
```

---------------------------------------------------------------------------
## To do:

### Priority:
Make dummy account and transfer songs through Postman

### Misc:
Error handling on API responses

Error handling for sql responses

Unit testing!

Group API requests, maybe using graphQL?
	Or at least progress bar for user while requests are being sent

Need to organize dataBP endpoints into controllers with responsibilities that
make sense

Clean up duplicate code in database.py (passing sql command/error message and
arg list as parameter?)
