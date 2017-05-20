import datetime
import time
import sys
from poloniex import poloniex
from Charter import Chart

class Trading_Bot():
	prices = []
	currentMovingAverage = 0
	historicalData = False
	tradePlaced = False
	typeOfTrade = False
	dataDate = ""
	orderNumber = ""
	dataPoints = []
	localMax = []
	currentResistance = 0.000
	key = "Your_Key"
	secret = "Your_Secret"

	def __init__(self, timer, pair, lengthOfMA, startTime, endTime):
		self.timer = timer
		self.pair = pair
		self.lengthOfMA = lengthOfMA
		self.startTime = startTime
		self.endTime = endTime

	def connectToPoloniex(self):		
		print("Connecting to Poloniex...")
		self.conn = poloniex(str(self.key), str(self.secret))
		print("Connected.")
		return self.conn

	def getCurrentTicker(self):
		while True:
			currentValues = self.conn.api_query("returnTicker")
			lastPairPrice = currentValues[self.pair]["last"]
			dataDate = datetime.datetime.now()
			print("{:%Y-%m-%d %H:%M:%S}".format(dataDate) + " Period: {}s, Pair:{}, Price:{}".format(self.timer, self.pair, lastPairPrice))
			time.sleep(self.timer)			

	def getHistoricalData(self):
		if not self.conn:
			print("Not Connected to Poloniex")
		if self.startTime:
			print("Getting Historical Data...")
			self.historicalData = self.conn.api_query("returnChartData", {"currencyPair":self.pair, "start":self.startTime, "end":self.endTime, "period":self.timer})
			print("Recieved Historical Data...")
		
	def getChart(self):	
		while True:
			if (self.startTime and self.historicalData):
				nextDataPoint = self.historicalData.pop(0)
				self.lastPairPrice = nextDataPoint['weightedAverage']
				dataDate = datetime.datetime.fromtimestamp(int(nextDataPoint['date'])).strftime('%Y-%m-%d %H:%M:%S')
			elif (self.startTime and not self.historicalData):
				chart = Chart(self.dataPoints)
				chart.makeChart()
				sys.exit()

			self.dataPoints.append({'date':dataDate, 'price': str(self.lastPairPrice), 'trend': 'null', 'label': 'null', 'desc': 'null'})

	def getLocalMaxChart(self):
		while True:
			if (self.startTime and self.historicalData):
				nextDataPoint = self.historicalData.pop(0)
				self.lastPairPrice = nextDataPoint['weightedAverage']
				dataDate = datetime.datetime.fromtimestamp(int(nextDataPoint['date'])).strftime('%Y-%m-%d %H:%M:%S')
			elif (self.startTime and not self.historicalData):
				chart = Chart(self.dataPoints)
				chart.makeChart()
				print(numberOfSimilarLocalMaxes)
				sys.exit()

			self.dataPoints.append({'date':dataDate, 'price': str(self.lastPairPrice), 'trend': str(self.currentResistance), 'label': 'null', 'desc': 'null'})
		
			if ((len(self.dataPoints)>2) and 
				(self.dataPoints[-2]['price']>self.dataPoints[-1]['price']) and 
				(self.dataPoints[-2]['price']>self.dataPoints[-3]['price'])):
				self.dataPoints[-2]['label'] = "'MAX'"
				self.dataPoints[-2]['desc'] = "'This is a local maximum'"

				numberOfSimilarLocalMaxes = 0

				for oldMax in self.localMax:
					if ((float(oldMax)>(float(self.dataPoints[-2]['price']) - .0001)) and 
						(float(oldMax)<(float(self.dataPoints[-2]['price']) + .0001))):
						numberOfSimilarLocalMaxes += 1

				if (numberOfSimilarLocalMaxes>2):
					self.currentResistance = self.dataPoints[-2]['price']
					self.dataPoints[-2]['trend'] = self.dataPoints[-2]['price']
					self.dataPoints[-1]['trend'] = self.dataPoints[-2]['price']

				self.localMax.append(self.dataPoints[-2]['price'])