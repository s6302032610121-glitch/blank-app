extends Node

var rng = RandomNumberGenerator.new()

func _ready():
	rng.randomize()

func pull(count: int = 1):
	var results = []
	for i in range(count):
		var roll = rng.randf()
		if roll < 0.01:
			results.append(get_random_unit(5))
		elif roll < 0.10:
			results.append(get_random_unit(4))
		else:
			results.append(get_random_unit(3))
	return results

func get_random_unit(rarity: int):
	# In a real app, this would pull from gacha_rates.json pool
	return "unit_rarity_" + str(rarity) + "_" + str(rng.randi_range(1, 100))
