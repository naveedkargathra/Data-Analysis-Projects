import numpy as np

def calculate(list):
  if len(list) < 9:
    raise ValueError ("List must contain nine numbers.")
  else:
    arr = np.array(list)
    arr1 = arr.reshape(3,3)
    print(arr1)
  
    
    mean = [arr1.mean(0).tolist(), arr1.mean(1).tolist(), arr1.mean()]
    std_dev = [arr1.std(0).tolist(), arr1.std(1).tolist(), arr1.std()]
    variance = [arr1.var(0).tolist(), arr1.var(1).tolist(), arr1.var()]
    maximum = [arr1.max(0).tolist(), arr1.max(1).tolist(), arr1.max()]
    minimum = [arr1.min(0).tolist(), arr1.min(1).tolist(), arr1.min()]
    summation = [arr1.sum(0).tolist(), arr1.sum(1).tolist(), arr1.sum()]

    calculations = {'mean' : mean,
                    'variance': variance,
                    'standard deviation': std_dev,
                    'max' : maximum,
                    'min' : minimum,
                    'sum' : summation}
    return calculations










