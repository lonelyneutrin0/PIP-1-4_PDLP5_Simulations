import matplotlib.pyplot as plt
import numpy as np
import time
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif"
})
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']


def digitizewater(data):
	bins = np.array([-25,-2,12,25])
	digitizedwater = np.digitize(data,bins)
	#Timestep is the first axis, second axis is for a specific water molecule.
	return digitizedwater
#Get the same array as the input, but now without duplicates so it is easier to look at. https://stackoverflow.com/questions/37839928/remove-consecutive-duplicates-in-a-numpy-array
def filternorepeats(arr):
	#Filter out odd numbers.
	eventimes = np.nonzero(arr%2==0)[0]
	arr = arr[arr%2==0]//2
	diff = np.diff(arr)
	return (arr[np.insert(diff.astype(bool), 0, True)], np.hstack([0, eventimes[1+np.nonzero(diff)[0]]]))

def norepeats(arr):
	diff = np.diff(arr)
	return (arr[np.insert(diff.astype(bool), 0, True)], np.hstack([0, 1+np.nonzero(diff)[0]]))

counter = 0
def plotcrossing(data, start, stop):
	global counter
	if counter < 100:
		fig, ax = plt.subplots(1,1)
		ax.plot(data)
		ax.axvspan(start,stop, color='gray')
		fig.savefig("waterplots/plot_%d.png" % counter)
		counter += 1
def countcrossings2(digitized, data):
	crossingtimes = []
	crossingdurations = []
	counter = 0
	# print(digitized.shape)
	# print(np.sum(digitized == 2))
	# print(np.nonzero(digitized == 2))
	# print(np.nonzero(digitized == 2)[1].shape)
	#For whatever reason, np.nonzero will give you the same "j" axis multiple times. 
	#We just want it once, so put it into a set.
	jset = set(np.nonzero(digitized == 2)[1])
	# print(len(jset))
	# exit()
	#We want a sequence for a specific water molecule where it is in the "1" bin for a bit, but has 0 and 2 as bookends.
	for j in jset:
		shortarray, times = filternorepeats(digitized[:,j])
		oneidxs = np.nonzero(shortarray==1)[0]
		for k in oneidxs:
			if (k > 0) and (k < len(shortarray) - 1) and (shortarray[k-1] != shortarray[k+1]):
				# print("We have a crossing! %d, %d" % (j, k))
				#print(shortarray, times)
				# print(shortarray, oneidxs)
				crossingtimes.append(times[k+1])
				crossingdurations.append(times[k+1]-times[k-1])
				#plotcrossing(data[:,j],times[k-1],times[k+1])
	return (np.array(crossingtimes), np.array(crossingdurations))
def countcrossings(digitized, data):
	crossingset = set()
	crossingtimes = []
	crossingdurations = []
	jset = set(np.nonzero(digitized == 2)[1])
	#We want a sequence for a specific water molecule where it is in the "1" bin for a bit, but has 0 and 2 as bookends.
	for j in jset:
		shortarray, times = norepeats(digitized[:,j])
		oneidxs = np.nonzero(shortarray==2)[0]
		for k in oneidxs:
			l = 1
			while k - l > 0 and not (shortarray[k-l] == 0 or shortarray[k-l] == 4):
				l+=1
			m = 1
			while k+m < len(shortarray)-1 and not (shortarray[k+m] == 0 or shortarray[k+m] == 4):
				m+=1
			if (k - l  >= 0) and (k + m <= len(shortarray) - 1) and (shortarray[k-l] != shortarray[k+m]) and (shortarray[k+m] == 0 or shortarray[k+m] == 4) and (shortarray[k-l] == 0 or shortarray[k-l] == 4) and (j,k+m) not in crossingset:
				#print("We have a crossing! %d, %d" % (j, k))
				crossingset.add((j,k+m))
				crossingtimes.append(times[k+m])
				crossingdurations.append(times[k+m]-times[k-l])
				plotcrossing(data[:,j],times[k-l],times[k+m])
	
	return (np.array(list(crossingtimes)), np.array(crossingdurations))


for d in ['porinalone', 'porinwithcap']:
	rates = []
	for i in range(3):
		data = np.load("waterdata/%s_%d.npy" % (d, i))
		#Frames are 100ps apart.
		simtime = 0.1 * len(data) #This is now in ns.
		digitzeddata = digitizewater(data)
		#print(checkcrossings(digitzeddata))
		# start = time.time()
		# times, durations = countcrossings(digitzeddata, data)
		# #print(d, i, times, durations, len(times))
		# rate = len(times) / simtime
		# print(d,i,len(times), simtime, rate)
		# print(time.time() - start)
		start = time.time()
		times, durations = countcrossings2(digitzeddata, data)
		#print(d, i, times, durations, len(times))
		rate = len(times) / simtime
		rates.append(rate)
		print(d,i,len(times), simtime, rate)
		print(time.time() - start)
		np.savez("waterdata/reduced%s_%d.npz", time=times, duration=durations)
	rates = 1000 * np.array(rates) # Multiplying by 1000 puts it in waters/microsecond
	print(np.mean(rates), np.std(rates) / np.sqrt(3))