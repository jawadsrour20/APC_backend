# APC_Backend

Automatic Program Corrector Backend is a RESTful back-end server built with Python's FastAPI framework. It provides functionality that allows for automatically generating unit test cases for uploaded files. Data is persisted in a MySQL database.

---

## Configuring the Server

1. Make sure Python 3.6+ is installed on your machine, as well as pip. Instructions on how to install [pip](https://pip.pypa.io/en/stable/installation/)

---

### Creating a Virtual Environment

2. Create a virtual environment and activate it by executing the following commands:

   ```bash
   cd APC_backend # navigate to project directory
   pip install virtualenv
   virtualenv env # create a virtual environment
   source env/bin/activate # activate the virtual environment
   ```

3. To install the required dependencies, execute the following command:

   ```bash
   pip install -r requirements.txt # installs required dependencies
   
   ```

---

### Create required directories

```bash
mkdir input output
```

---

### Setting Up the Database

4. [Download MySQL Community Server and MySQL Workbench](https://dev.mysql.com/downloads/ )

5. Create a root user account. Note down your host name, user, and password

6. Import the database.sql file from MySQL Workbench Server settings.

---

### Setting Up the .env file

7. To create .env file to store the server's environment variables, execute the following commands:

```bash
touch .env # creates .env file
vim .env # use vim or open the .env file in a code editor 
```

8. Set the values for the following host, user, and password keys:

```bash
host=HOST_NAME # typically host is localhost 
user=USER_NAME
password=PASSWORD
db=DB_NAME
```

---

### Set the DOCKER_IMAGE_TAG variable in PynguinAPI.sh for Unix Machines (MacOS and Linux Distros)

9. Run the below command 

```sh
# In file PynguinAPI.sh
# modify 
```



---

### Running the Server

9. To run the app, execute the following command on your terminal:

   ```bash
   uvicorn main:app --reload # note on this method of running the server. 
   # The server automatically reloads when a change is done in the back-end code
   # An alternative way is to run the main.py Python file --> python3 main.py
   ```

10. Notes:

    - The server automatically runs on **http://localhost:8000** 

    - To access the API documentation (both documentations provide the same functionaltiy, one might just have a preference): 

      a. Swagger API Documentation:  **http://localhost:8000/docs**  

      b. ReDoc Documentation:  **http://localhost:8000/redoc**

---

## Testing Locally using Ngrok

1. [Download](https://dashboard.ngrok.com/get-started/setup) [ngrok](https://ngrok.com/download) 

2. Unzip to install: 

   ```bash
   unzip /path/to/ngrok.zip
   ```

3. Connect your account: 

   ```bash
   ./ngrok authtoken <token>
   ```

4. To start a HTTP tunnel forwarding to your local port PORT_NUMBER, run this next:

   ```bash
   ./ngrok http PORT_NUMBER
   ```

* note: To call fetch() API from the front-end when testing locally we need to sign our backend with an SSL/TLS certificate marking it secure (https). An easy way to do that is by using ngrok!

---

## Running [Pynguin](https://github.com/se2p/pynguin) in a docker environment

Prerequisite: have [docker](https://www.docker.com/products/docker-desktop) installed on your machine.

1. Make sure pynguin is in the home directory

   ```bash
   cd ~
   git clone https://github.com/se2p/pynguin.git
   ```

2. Create input, output, and package directories. Create package/package.txt

   ```bash
   cd ~/pynguin
   mkdir input output package
   touch package/package.txt
   ```

3. Create input, output, and package volumes

   ```bash
   docker volume create input
   docker volume create output
   docker volume create package
   # run "docker volume ls" to check that volumes got created successfully
   ```

4. Containerize the app by running the Makefile script

   ```bash
   make # make docker
   # OR RUN THE BELOW INSTEAD
   docker build \
   	  -t $(IMAGE):$(VERSION) . \
   	  -f ./docker/Dockerfile --no-cache
   	  
```

5. Check your docker Image container Tag for Pynguin container

   ```bash
   docker image ls
   # output would be something like the below
   ```

   REPOSITORY   TAG        IMAGE ID       CREATED       SIZE
   appname      latest     a4962c112cd9   6 days ago    169MB
   pynguin      <mark style="background-color:#F0EDE5;color:#88B04B">**9ccbdc17**</mark>   203050f9142a   6 days ago    153MB
   hello-app    latest     518ae29ba4ea   6 days ago    169MB
   ubuntu       latest     a457a74c9aaa   3 weeks ago   65.6MB

6. Run Pynguin in docker container

   ```bash
   docker run \
       -v ~/pynguin/input:/input:ro \
       -v ~/pynguin/output:/output \
       -v ~/pynguin/package:/package:ro pynguin:<DOCKER_IMAGE_TAG> --project-path /input \
       --output-path /output \
       --module-name PYTHON_FILE_NAME -v
   ```

---



