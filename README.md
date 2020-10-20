# AGH SPACE SYSTEMS 


TASK 1
======

Start-up: 

0. open task1 folder
1. type `pip install requirments.txt`
2. run python shell (usually 'python' or 'python3.6' if you have more than one version on your computer)
3. type `from main import db`
4. type `db.create_all()`
5. type `exit()`
6. type `python main.py` (or `python3.6 main.py` for example)

Now server is running, you can use API with some tool for making http requests (e.g curl, it's built in windows and probably in linux)

For example:

`curl -H "Content-Type: application/json" -d @data.json -X POST http://127.0.0.1:5000/addOne`

`curl -H "Content-Type: application/json" -X GET http://127.0.0.1:5000/getAll`

`curl -H "Content-Type: application/json" -X GET http://127.0.0.1:5000/getOne?id=1`

`curl -H "Content-Type: application/json" -X GET http://127.0.0.1:5000/delete?id=1`

___

TASK 3
======

Start-up: 
0. plug in your Arduino Uno to computer
1. run Arduino IDE, in bottom-right corner check if port is a 'COM4', compile code and write it to arduino
2. if port isn't 'COM4' type `notepad main.py` or `vim main.py` and change line 5 to your port
3. type `pip install requirments.txt`

Now you are ready to run program. You can use it in two different modes. In first you just type `python main.py conn` and then you type commands as they are in manual below. In second mode you type first `python main.py` and then command. In both modes there are some delays due to arduino bootloader, which are impossible to delete or reduce.

## COMMANDS:

`pos <int> : set servo position to <int>`

`open : open servo`

`close : close servo`

`info : get info from servo in format`
	  `("info" <actual_position><status><close_position><open_position>)`
    
`help : for help`

`setclose <int> : to set servo close position to <int>`

`setopen <int> : to set servo open position to <int>`

`conn : to connect (only in 'second' mode)`

`disc : to disconnect (only in 'first' mode)`

___

Please, if I would not get to the third stage of recruitment, then send me some feedback about what could be done better. Thank you :)











