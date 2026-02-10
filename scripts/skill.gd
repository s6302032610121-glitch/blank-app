extends Node
class_name GameSkill

var id: String
var skill_name: String
var type: String # Physical, Magic, Support, LB
var element: String
var multiplier: float
var hits: int
var frame_data: Array
var chain_family: String
var lb_fill: float

func _init(data: Dictionary):
	id = data.get("id", "")
	skill_name = data.get("name", "Unknown Skill")
	type = data.get("type", "Physical")
	element = data.get("element", "None")
	multiplier = data.get("multiplier", 1.0)
	hits = data.get("hits", 1)
	frame_data = data.get("frame_data", [0])
	chain_family = data.get("chain_family", "None")
	lb_fill = data.get("lb_fill", 0.0)
