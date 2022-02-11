a = [(123, {"x": 1,"y": 2}), (456, {"x": 4, "y": 5}), (0, {"x": 4, "y": 5})]
a.sort(key=lambda x: x[0])
print(a)