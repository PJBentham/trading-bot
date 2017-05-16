import time
import sys
import argparse
import datetime
import csv
from poloniex import poloniex

def main(argv):
	prices = []
	currentMovingAverage = 0
	lengthOfMA = 0	
	startTime = False
	endTime = False
	historicalData = False
	tradePlaced = False
	typeOfTrade = False
	dataDate = ""
	orderNumber = ""
	dataPoints = []
	localMax = []
	currentResistance = 0.018

	with open('polopairs.csv', 'rb') as f:
		reader=csv.reader(f)
		pairs = list(reader)[0]

	parser = argparse.ArgumentParser()
	
	parser.add_argument("-t", "--timer", 
						default=300, 
						type=int, 
						choices=[10, 300, 900, 1800, 7200, 14400, 86400], 
						help="Time Period for Poloniex")
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

	timer = args.timer
	pair = args.currency
	lengthOfMA = args.points
	startTime = args.start
	endTime = args.end

	if not len(argv):
		parser.print_help()
		sys.exit(1)

	conn = poloniex("Your_Key","Your_Secret")

	if(startTime):
		historicalData = conn.api_query("returnChartData", {"currencyPair":pair, "start":startTime, "end":endTime, "period":timer})

	while True:
		if (startTime and historicalData):
			nextDataPoint = historicalData.pop(0)
			lastPairPrice = nextDataPoint['weightedAverage']
			dataDate = datetime.datetime.fromtimestamp(int(nextDataPoint['date'])).strftime('%Y-%m-%d %H:%M:%S')
		elif (startTime and not historicalData):
			sys.exit()
		else:		
			currentValues = conn.api_query("returnTicker")
			lastPairPrice = currentValues[pair]["last"]
			dataDate = datetime.datetime.now()

		if len(prices) > 0:
			currentMovingAverage = sum(prices) / float(len(prices))
			previousPrice = prices[-1]
			if(not tradePlaced):
				if((lastPairPrice > currentMovingAverage) and (lastPairPrice < previousPrice)):
					print("SELL ORDER")
					tradePlaced = True
					typeOfTrade = "short"
				elif((lastPairPrice < currentMovingAverage) and (lastPairPrice > previousPrice)):
					print("BUY ORDER")
					tradePlaced = True
					typeOfTrade = "long"
			elif (typeOfTrade == "short"):
				if( lastPairPrice < currentMovingAverage):
					print("EXIT TRADE")
					tradePlaced = False
					typeOfTrade = False
			elif (typeOfTrade == "long"):
				if( lastPairPrice > currentMovingAverage):
					print("EXIT TRADE")
					tradePlaced = False
					typeOfTrade = False
		else:
			previousPrice = 0		
		
		print("{} Period: {}s, {}:{}, Moving Average: {}".format(dataDate, timer, pair, lastPairPrice, currentMovingAverage))	

		prices.append(float(lastPairPrice))
		prices = prices[-lengthOfMA:]

		if(not startTime):
			time.sleep(timer)

if __name__ == "__main__":
	main(sys.argv[1:])
