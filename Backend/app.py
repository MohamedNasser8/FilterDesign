from flask import Flask, jsonify, request, json
import numpy as np
import scipy
import scipy.signal

from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

def frequencyResponse(zeros, poles, gain):
    w, h = scipy.signal.freqz_zpk(zeros, poles, gain)
    magnitude = 20 * np.log10(np.abs(h))
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

@app.route('/getFinalFilter', methods=['POST', 'GET'])
@cross_origin()
def getFinalFilter():
    if request.method == 'POST':
        zerosAndPoles = json.loads(request.data)
        zeros = parseToComplex(zerosAndPoles['zeros'])
        poles = parseToComplex(zerosAndPoles['poles'])
        gain = 1

        a = zerosAndPoles['a']

        w, finalAngles, filterMagnitude = frequencyResponse(zeros, poles, gain)

        finalMagnitude = filterMagnitude*gain

        response_data = {
                'w': w.tolist(),
                'angels': finalAngles.tolist(),
                'magnitude': finalMagnitude.tolist()
            }
    return jsonify(response_data)

@app.route('/getFilter', methods=['POST'])
@cross_origin()
def getFrequencyResponce():
    if request.method == 'POST':
        zerosAndPoles = json.loads(request.data)
        zeros = parseToComplex(zerosAndPoles['zeros'])
        poles = parseToComplex(zerosAndPoles['poles'])
        gain = zerosAndPoles['gain']
        print(zeros, poles, gain)

        w, angles, magnitude = frequencyResponse(zeros, poles, gain)
        response_data = {
                'w': w.tolist(),
                'angels': angles.tolist(),
                'magnitude': magnitude.tolist()
            }
    return jsonify(response_data)


@app.route('/differenceEquationCoefficients' , methods=['GET','POST'])
def differenceEquationCoefficients():
    if request.method == 'POST':

        zerosAndPoles = json.loads(request.data)
        zeros = parseToComplex(zerosAndPoles['zeros'])
        poles = parseToComplex(zerosAndPoles['poles'])
        b, a = scipy.signal.zpk2tf(zeros, poles, 1)

        response_data = {
            'b': b.flatten().tolist(),
            'a': a.flatten().tolist()
        }

        return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
