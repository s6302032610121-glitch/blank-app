extends Node

const SAVE_PATH = "user://save_game.json"

func save_game(data: Dictionary):
	var file = FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file:
		var json_string = JSON.stringify(data)
		file.store_string(json_string)
		file.close()

func load_game() -> Dictionary:
	if not FileAccess.file_exists(SAVE_PATH):
		return {}

	var file = FileAccess.open(SAVE_PATH, FileAccess.READ)
	if file:
		var json_string = file.get_as_text()
		file.close()
		var json = JSON.new()
		var error = json.parse(json_string)
		if error == OK:
			return json.get_data()
	return {}
