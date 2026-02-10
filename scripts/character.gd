extends Node
class_name GameCharacter

var id: String
var character_name: String
var element: String
var rarity: int

var max_hp: int
var hp: int
var atk: int
var def: int
var mag: int
var spr: int

var lb_gauge: float = 0.0
var max_lb: float = 100.0

var skills: Array = []

func _init(data: Dictionary):
	id = data.get("id", "")
	character_name = data.get("name", "Unknown")
	element = data.get("element", "None")
	rarity = data.get("rarity", 3)
	max_hp = data.get("hp", 1000)
	hp = max_hp
	atk = data.get("atk", 100)
	def = data.get("def", 100)
	mag = data.get("mag", 100)
	spr = data.get("spr", 100)

func take_damage(amount: int):
	hp = max(0, hp - amount)
	lb_gauge = min(max_lb, lb_gauge + (amount / max_hp) * 50.0)

func add_lb(amount: float):
	lb_gauge = min(max_lb, lb_gauge + amount)
