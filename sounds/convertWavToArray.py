from scipy.io import wavfile

filename = "test"
extension = ".wav"


samplingRate, data = wavfile.read(filename + extension)
print(samplingRate)
print(data)
arrayFile = open(samplingRate + filename, "x")
arrayFile.write(data)
