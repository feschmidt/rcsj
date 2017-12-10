# rcsj
Simulating Josephson junctions with the RCSJ model

## TODO:
* frequency analysis
	* as a function of current
	* as a function of voltage
* $I_r/I_s$ as a function of Q
* everything in real physical values

## weblinks
* ```https://www.wmi.badw.de/teaching/Lecturenotes/AS/AS_Chapter3.pdf```

## recommended times for current bias:
```python
for Q in qs:
	if Q < 0.1:
		times.append(np.arange(0,4000,0.01))
		ts.append(0.8)
	elif Q < 1.:
		times.append(np.arange(0,1000,0.01))
		ts.append(0.8)
	elif Q < 10.:
		times.append(np.arange(0,500,0.01))
		ts.append(5e-2)
	elif Q < 100.:
		times.append(np.arange(0,500,0.01))
		ts.append(1e-2)
	else:
		times.append(np.arange(0,200,0.01))
		ts.append(1e-4)
```
