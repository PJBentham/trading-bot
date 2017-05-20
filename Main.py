import argparse
import sys
import csv
from Trading_Bot import Trading_Bot

def checkArgs(argv):
	if not len(argv):
		parser.print_help()
		sys.exit(1)

def parseArgs(argv):
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--timer", 
						default=10, 
						type=int, 
						choices=[10, 300, 900, 1800, 7200, 14400, 86400], 
						help="Time Period for Poloniex")
	with open('polopairs.csv', 'rb') as f:
		reader=csv.reader(f)
		pairs = list(reader)[0]
	parser.add_argument("-c", "--currency",
						type=str,
						choices=pairs,
						help="Poloniex Currency Pairing")
	parser.add_argument("-p", "--points",
						type=int,
						default=10,
						help="Number of Points for Moving Average")
	parser.add_argument("-s", "--start", 
						help="Poloniex Start Time (Unixtimestamp)")
	parser.add_argument("-e", "--end", 
						help="Poloniex End Time (Unixtimestamp)")
	args=parser.parse_args()
	return args

def main(argv):

	checkArgs(argv)
	args = parseArgs(argv)

	myBot = Trading_Bot(args.timer, args.currency, args.points, args.start, args.end)
	myBot.connectToPoloniex()
	# myBot.getCurrentTicker()
	myBot.getHistoricalData()
	# myBot.getChart()
	myBot.getLocalMaxChart()


if __name__ == "__main__":
	main(sys.argv[1:])
