extends Node
class_name ChainSystem

signal chain_updated(count, multiplier)

var current_chain: int = 0
var current_multiplier: float = 1.0
var max_multiplier: float = 4.0
var chain_window: float = 0.33 # roughly 20 frames at 60fps
var last_hit_time: float = 0.0

var active_hits: Array = [] # Array of dicts {time, character, damage, family}

func _process(delta):
	if current_chain > 0:
		last_hit_time += delta
		if last_hit_time > chain_window:
			reset_chain()

func register_hit(family: String, element: String):
	last_hit_time = 0.0
	current_chain += 1

	var increment = 0.1
	if family != "None" and family != "":
		# If same family and timed right, bigger multiplier increment
		# In FFBE, spark chain or elemental chain increases faster
		increment = 0.3

	current_multiplier = min(max_multiplier, current_multiplier + increment)
	chain_updated.emit(current_chain, current_multiplier)
	return current_multiplier

func reset_chain():
	current_chain = 0
	current_multiplier = 1.0
	chain_updated.emit(current_chain, current_multiplier)
