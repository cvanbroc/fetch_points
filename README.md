# fetch_points coding exercise

# prerequisites
- Make sure Python is installed, it must be installed first if not already present
- My version output is below

$ python3 --version
Python 3.8.10

# install flask if it is not already present as well
$ pip install flask

# change working directory to location where webserver.py exists
$ export FLASK=webserver.py
# run flask executable, if not already added to path may need to update $PATH or call directly
- e.g. $/home/ubuntu/.local/bin/flask run

# open another terminal and use curl to send requests
# sample commands and output from the script are listed below

$ curl -i http://127.0.0.1:5000/transactions -X POST -H 'Content-Type: application/json' -d '{"payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z"}'

{"payer":"DANNON","points":1000,"timestamp":"2020-11-02T14:00:00Z"}

# execute the next four POST commands to coninue populating the data
# reponses are not listed but should resemble the return output above adjusted for different data

$ curl -i http://127.0.0.1:5000/transactions -X POST -H 'Content-Type: application/json' -d '{"payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z"}'
$ curl -i http://127.0.0.1:5000/transactions -X POST -H 'Content-Type: application/json' -d '{"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"}'
$ curl -i http://127.0.0.1:5000/transactions -X POST -H 'Content-Type: application/json' -d '{"payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z"}'
$ curl -i http://127.0.0.1:5000/transactions -X POST -H 'Content-Type: application/json' -d '{"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"}'

# check points with a points GET
$ curl -i http://127.0.0.1:5000/points -X GET

{"DANNON":1100,"MILLER COORS":10000,"UNILEVER":200}

# spend points with a PATCH 
# some point spends and the resulting output are shown below

$ curl -i http://127.0.0.1:5000/points -X PATCH -H 'Content-Type: application/json' -d '{"points": 5000}'

[{"payer":"DANNON","points":-100},{"payer":"UNILEVER","points":-200},{"payer":"MILLER COORS","points":-4700}]

$ curl -i http://127.0.0.1:5000/points -X GET

{"DANNON":1000,"MILLER COORS":5300,"UNILEVER":0}

# try spending too many points and verify that it does not allow the action
# terminal with flask running should report an error code (422 in this case)
$ curl -i http://127.0.0.1:5000/points -X PATCH -H 'Content-Type: application/json' -d '{"points": 10000}'

{"error":"The requested point spend is not allowed"}

# try spending negative points and verify that it does not allow the actions
# terminal with flask running should report an error code (422 in this case)
$ curl -i http://127.0.0.1:5000/points -X PATCH -H 'Content-Type: application/json' -d '{"points": -2}'

{"error":"The requested point spend is not allowed"}

# spend zero points and verify that the request is handled, in this case an empty array is returned as no points are spent

$ curl -i http://127.0.0.1:5000/points -X PATCH -H 'Content-Type: application/json' -d '{"points": 0}'

[]

# I included a transactions GET route so we can verify that points are actually being spent in the correct order
# here we see that the unspent points come from 11-01 and 11-02, while the spent points are from 10-31 as expected (oldest points spent first)
$ curl -i http://127.0.0.1:5000/transactions -X GET

[{"payer":"DANNON","points":0,"timestamp":"2020-10-31T10:00:00Z"},{"payer":"UNILEVER","points":0,"timestamp":"2020-10-31T11:00:00Z"},{"payer":"DANNON","points":0,"timestamp":"2020-10-31T15:00:00Z"},{"payer":"MILLER COORS","points":5300,"timestamp":"2020-11-01T14:00:00Z"},{"payer":"DANNON","points":1000,"timestamp":"2020-11-02T14:00:00Z"}]

# spend more points
$ curl -i http://127.0.0.1:5000/points -X PATCH -H 'Content-Type: application/json' -d '{"points": 5900}'

[{"payer":"DANNON","points":-600},{"payer":"MILLER COORS","points":-5300}]

$ curl -i http://127.0.0.1:5000/points -X GET

{"DANNON":400,"MILLER COORS":0,"UNILEVER":0}

# try to overspend on last transaction
$ curl -i http://127.0.0.1:5000/points -X PATCH -H 'Content-Type: application/json' -d '{"points": 401}'

{"error":"The requested point spend is not allowed"}

# spend exactly the amount of points left
$ curl -i http://127.0.0.1:5000/points -X PATCH -H 'Content-Type: application/json' -d '{"points": 400}'

[{"payer":"DANNON","points":-400}]

# check to make sure points are at zero
$ curl -i http://127.0.0.1:5000/points -X GET

{"DANNON":0,"MILLER COORS":0,"UNILEVER":0}

curl -i http://127.0.0.1:5000/transactions -X GET

[{"payer":"DANNON","points":0,"timestamp":"2020-10-31T10:00:00Z"},{"payer":"UNILEVER","points":0,"timestamp":"2020-10-31T11:00:00Z"},{"payer":"DANNON","points":0,"timestamp":"2020-10-31T15:00:00Z"},{"payer":"MILLER COORS","points":0,"timestamp":"2020-11-01T14:00:00Z"},{"payer":"DANNON","points":0,"timestamp":"2020-11-02T14:00:00Z"}]








