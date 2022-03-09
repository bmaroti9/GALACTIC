import json

data = []
data.append({
    "name": "mosquito",
    "shrink": 0.13,
    "guns": [[11, 30]],
    "gun_timer": 20,
    "engine_efficiancy": 0.05
})

data.append({
    "name": "Hummingbird",
    "shrink": 0.11,
    "guns": [[11, 30]],
    "gun_timer": 20,
    "engine_efficiancy": 0.13
})

data.append({
    "name": "Crabb",
    "shrink": 0.11,
    "guns": [[19, 60], [-19, 60]],
    "gun_timer": 10,
    "engine_efficiancy": 0.075
})

print("saving data", data)

# kimenti a data valtozot a data.txt fileba
with open("data.txt", "w") as f:
    json.dump(data, f, indent=2)

with open("names.txt", "w") as f:
    json.dump([0, 0, 0], f, indent=2)


# betoltjuk a data2 valtozot a data.txt filebol
with open("data.txt", "r") as f:
    data2 = json.load(f)

print("loaded data", data2)
