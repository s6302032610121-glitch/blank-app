# Project Crystal Fate (2D Portrait RPG)

A 2D Portrait RPG inspired by FFBE and FFXV.

## Core Features
- **FFBE-style Battle System**: Turn-based, 4-man party, simultaneous skill execution.
- **Chain System**: Hit-timing based damage multipliers with chain families.
- **Limit Burst**: Character-specific ultimate moves.
- **Offline Gacha**: 1%/9%/90% rates, simulated with local JSON storage.
- **Portrait Mode**: 9:16 aspect ratio (540x960).

## Project Structure
- `/scenes`: Battle, Story, Gacha, and UI scenes.
- `/scripts`: Core logic (BattleManager, ChainSystem, GachaSystem, etc.).
- `/data`: Game data in JSON format (Characters, Skills, Story).
- `/assets`: Character design prompts and placeholders.

## How to Run
1. Download and install **Godot Engine 4.x**.
2. Open the project by selecting `project.godot`.
3. Press `F5` to run the main battle scene.

## Exporting for Web (HTML5)
1. Go to `Project` > `Export`.
2. Click `Add...` and select `Web`.
3. Ensure the `VRAM Texture Compression` matches your target.
4. Click `Export Project` and choose a destination folder.
5. Host the resulting files on a web server (e.g., GitHub Pages, itch.io).

## Exporting for PC (Windows/Linux/macOS)
1. Go to `Project` > `Export`.
2. Click `Add...` and select your target platform.
3. Click `Export Project`.

## Technical Notes
- The `ChainSystem` uses a timing window of ~0.33s for hits to connect.
- Damage formula: `(Stat^2 / EnemyStat) * Multiplier * ElementMod * ChainMult`.
- Gacha results are saved to `user://save_game.json`.
