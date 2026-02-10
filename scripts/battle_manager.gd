extends Node

var party: Array[GameCharacter] = []
var enemies: Array[GameCharacter] = []
var chain_system: ChainSystem

enum State { PLAYER_TURN, EXECUTING, ENEMY_TURN, WIN, LOSS }
var current_state = State.PLAYER_TURN

func _ready():
	chain_system = ChainSystem.new()
	add_child(chain_system)
	load_game_data()

func load_game_data():
	var file = FileAccess.open("res://data/characters.json", FileAccess.READ)
	var json = JSON.parse_string(file.get_as_text())
	file.close()

	for char_data in json["characters"]:
		var character = GameCharacter.new(char_data)
		party.append(character)
		add_child(character)

	# Mock enemy for testing
	var boss_data = {
		"id": "boss_01",
		"name": "Void Dragon",
		"element": "Dark",
		"hp": 1000000,
		"atk": 500,
		"def": 200,
		"mag": 500,
		"spr": 200
	}
	var boss = GameCharacter.new(boss_data)
	enemies.append(boss)
	add_child(boss)

	setup_ui_signals()

func setup_ui_signals():
	var container = get_node("UI/PartyContainer")
	for i in range(party.size()):
		var btn = container.get_child(i)
		btn.pressed.connect(on_character_pressed.bind(i))

	chain_system.chain_updated.connect(update_chain_ui)

func on_character_pressed(index):
	if current_state != State.PLAYER_TURN and current_state != State.EXECUTING:
		return

	# Trigger first skill for demo
	# In real game, this would check if skill is selected
	var character = party[index]
	# Load a skill for the character
	var skill_file = FileAccess.open("res://data/skills.json", FileAccess.READ)
	var skill_json = JSON.parse_string(skill_file.get_as_text())
	skill_file.close()

	var skill_data = skill_json["skills"][0] # Just use first skill for demo
	if index == 2: skill_data = skill_json["skills"][3] # Sera uses Cyclone Shot
	if index == 3: skill_data = skill_json["skills"][4] # Kaelen uses Abyssal Rain

	var skill = GameSkill.new(skill_data)
	run_skill(character, skill, enemies[0])

func update_chain_ui(count, multiplier):
	var label = get_node("UI/ChainMeter")
	label.text = "%d Chain\nx%.1f" % [count, multiplier]

func execute_player_actions(actions: Array):
	# actions: Array of {character, skill, target}
	current_state = State.EXECUTING

	# In FFBE, players tap characters to trigger skills
	# We'll simulate this with a timeline or simultaneous execution
	for action in actions:
		run_skill(action.character, action.skill, action.target)

func run_skill(attacker, skill, target):
	var elapsed_frames = 0
	for i in range(skill.hits):
		var target_frame = skill.frame_data[i]
		var wait_frames = target_frame - elapsed_frames
		if wait_frames > 0:
			await get_tree().create_timer(wait_frames / 60.0).timeout

		elapsed_frames = target_frame

		var damage = calculate_damage(attacker, skill, target)
		var mult = chain_system.register_hit(skill.chain_family, skill.element)
		var final_damage = damage * mult

		target.take_damage(int(final_damage))
		attacker.add_lb(skill.lb_fill)
		print("Hit %d: %d damage (x%.1f)" % [i+1, final_damage, mult])

func calculate_damage(attacker, skill, target):
	var base = 0
	if skill.type == "Physical":
		base = (attacker.atk ** 2) / target.def
	elif skill.type == "Magic":
		base = (attacker.mag ** 2) / target.spr
	elif skill.type == "LB":
		base = (attacker.atk ** 2 + attacker.mag ** 2) / (target.def + target.spr)

	var element_mod = get_element_modifier(skill.element, target.element)
	return base * skill.multiplier * element_mod

func get_element_modifier(attack_element, target_element):
	# Simple rock-paper-scissors or table lookup
	var table = {
		"Fire": {"Ice": 1.5, "Fire": 0.5, "Thunder": 1.0},
		"Ice": {"Wind": 1.5, "Ice": 0.5},
		"Thunder": {"Water": 1.5, "Thunder": 0.5},
		"Light": {"Dark": 1.5, "Light": 0.5},
		"Dark": {"Light": 1.5, "Dark": 0.5}
	}
	if attack_element in table and target_element in table[attack_element]:
		return table[attack_element][target_element]
	return 1.0
