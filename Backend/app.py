from flask import Flask, jsonify, request, json
import numpy as np
import scipy
import scipy.signal

from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)
  
Filter = None

@app.route('/getFinalFilter', methods=['POST', 'GET'])
@cross_origin()
def getFinalFilter():
    if request.method == 'POST':
        zerosAndPoles = json.loads(request.data)
        zeros = parseToComplex(zerosAndPoles['zeros'])
        poles = parseToComplex(zerosAndPoles['poles'])
        gain = 1

        a = zerosAndPoles['a']

        w, allPassAngles = getAllPassFrequencyResponse(a)
        w, filterAngels, filterMagnitude = frequencyResponse(zeros, poles, gain)

        finalAngles = np.add(allPassAngles, filterAngels)

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

@app.route('/getAllPassFilter', methods=['POST', 'GET'])
def getAllPassFilterData():
    if request.method == 'POST':
        data = json.loads(request.data)
        filterCoeffients = data['a']
        w, filter_angles = getAllPassFrequencyResponse(filterCoeffients)
        response_data = {
            'w': w.tolist(),
            'angels': filter_angles.tolist(),
        }
        return jsonify(response_data)
    else:
        return 'There is no Post request'


def getAllPassFrequencyResponse(filterCoeffients):
        filter_angles = np.zeros(512)
        w = np.zeros(512)
        for coeffient in filterCoeffients:
            w, angles = phaseResponse(coeffient)
            filter_angles = np.add(filter_angles, angles)
        return w, filter_angles

if __name__ == '__main__':
    app.run(debug=True, port=8080)
