# EstimatingGripForceFromFingertipPressure

<Repository for gripping force estimation with the goal of gripping control of a hand prosthesis with pressure sensors embedded inside its fingers>

Recording both gripping force and the applied pressure on the tips of the thumb, index and middle fingers simultaneously during precision-type gripping

Pressure signals are recorded via a BMP180 pressure sensors from Bosch Co. embedded inside the third knuckle of prosthesis's thumb, index and middle fingers.

Gripping force is the Z-axis force measured using a mini 45 F/T sensor from ATI Industrial Automation Inc.

- Signal processing:

Signals are smoothed and noise is reduced via notch and band-pass filters. All data is normalized.

- Dataset:

Data is derived form a healthy 25 year-old female subject. multiple tests were performed and all data were concatenated.

- Force estimation:

Gripping force is predicted using a Long short-term memory (LSTM) neural networks.
