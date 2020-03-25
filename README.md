# Prayer-Time-Display-2


PrayerTime Display is a web app used to display prayertimes on big screen. It uses the library from http://praytimes.org/code to calculate prayer times.

## Features

  - Enter longitude and latitude
  - Select calculation methods
     > MWL, ISNA, Egypt, Makkah, Karachi, Tehran, Jafari


### Tech

* [FLask](https://flask.palletsprojects.com/en/1.1.x/quickstart/)  - Python web web framework
* [Jinja](https://jinja.palletsprojects.com/en/2.11.x/) - templating engine
* [Pipenv](https://realpython.com/pipenv-guide/) - environment manager
* [Docker](https://docs.docker.com/get-started/) - virtual environment manager

### Installation
 1. Download the app
     ```sh
    $ git clone https://github.com/multekedir/Prayer-Time-Display-2.git$ 
    ```
2. Install Docker -> watch this [vedio](https://www.youtube.com/watch?v=TDLKQWsrSyk)

3.      
    ```sh
    $ cd Prayer-Time-Display-2
    ```
4. ```sh
    $ docker build -t flaskapp:latest .
     ```
5. ```sh
    $ docker run -it -d -p 5000:5000 flaskapp
     ```

### Usage 
1. Open http://127.0.0.1:5000/ in your default browser
2. To make changes to the location and calculation method go to http://127.0.0.1:5000/admin
    username: admin
    password: password



