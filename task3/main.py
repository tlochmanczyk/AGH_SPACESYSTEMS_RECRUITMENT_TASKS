import sys
import serial 
import time

PORT = 'COM4'
SPEED = 9600

cmds = ['pos', 'open', 'close', 'info', 'help', 'conn', 'setclose', 'setopen']
helpInfo = '''
		AVAILABLE COMMANDS:
pos <int> : set servo position to <int>
open : open servo
close : close servo
info : get info from servo in format
	  ("info" <actual_position><status><close_position><open_position>)
help : for help
setclose <int> : to set servo close position to <int>
setopen <int> : to set servo open position to <int>
disc : to disconnect

			'''

def actionHandler(*args):

	if args[0] == 'conn':
		contTransmission()
	elif args[0] == 'help':
		print(helpInfo) 
	elif len(args) > 1:
		return args[0] + ' ' + args[1] + '\n'
	else:
		return args[0] + '\n'
	return None


def validation():
	pass


def contTransmission():
	arg = ''
	with serial.Serial(PORT, SPEED, timeout=1) as ser:
		time.sleep(3)

		while True:
			arg = input('type commands>>> ').split()
			if 'conn' in arg:
				print('you are actually in continuos transmission mode')

			elif 'disc' in arg:
				ser.close()
				return None

			elif arg[0] in cmds:
				data = actionHandler(*arg)
				if data:
					send(data, ser)

			else:
				print('wrong command, try again or type <help>, or type <disc> to disconnect')
	

def send(data, ser):
			received = ''
			while data not in received:
				received = ''
				ser.write(data.encode())
				time.sleep(2)
				while ser.inWaiting() > 0:
					received += (ser.read(ser.inWaiting())).decode()

				#print('r: %s, d: %s' % (len(received), len(data)))
				print('r: %s, d: %s' % (received, data))


def frameTransmission(data):
	if data:		
		with serial.Serial(PORT, SPEED, timeout=1) as ser:
			time.sleep(3)
			send(data, ser)


def main():
	if sys.argv[1] in cmds:
		data = actionHandler(*sys.argv[1:])
		frameTransmission(data)
	else:
		print('wrong command, try again or type help')


if __name__ == '__main__':
	main()

