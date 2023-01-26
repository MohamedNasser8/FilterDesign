import numpy as np
import scipy
import scipy.signal

class Filter():
    def __init__(self):
        self.poles = None
        self.zeros = None


    def get_filter_coeffiectients(self, zeros, poles):
        self.zeros = self.parseToComplex(zerosAndPoles['zeros'])
        self.poles = self.parseToComplex(zerosAndPoles['poles'])

        self.b, self.a = scipy.signal.zpk2tf(self.zeros, self.poles, 1)
        
    def frequencyResponse(self, gain):
        #h is frequency response as complex
        #
        w, h = scipy.signal.freqz_zpk(self.zeros, self.poles, gain)
        #final filter magnitude
        magnitude = 20 * np.log10(np.abs(h))
        #final filter phase
        angels = np.unwrap(np.angle(h))
        return w/max(w), np.around(angels, decimals=3), np.around(magnitude, decimals=3)


    def phaseResponse(a):
        w, h = scipy.signal.freqz([-a, 1.0], [1.0, -a])
        angels = np.zeros(512) if a==1 else np.unwrap(np.angle(h))
        return w/max(w), np.around(angels, decimals=3)

    def parseToComplex(pairs):
        complexNumbers = [0]*len(pairs)
        for i in range(len(pairs)):
            x = round(pairs[i][0], 2)
            y = round(pairs[i][1], 2)
            complexNumbers[i] = x+ y*1j
        return complexNumbers
