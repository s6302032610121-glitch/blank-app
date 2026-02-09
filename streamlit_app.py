import streamlit as st
import random

# --- Data Definitions ---
CLASSES = {
    "Warrior": {"hp": 100, "max_hp": 100, "mp": 0, "max_mp": 0, "atk": 15, "def": 10},
    "Thief": {"hp": 80, "max_hp": 80, "mp": 0, "max_mp": 0, "atk": 12, "def": 8},
    "White Mage": {"hp": 60, "max_hp": 60, "mp": 40, "max_mp": 40, "atk": 5, "def": 5},
    "Black Mage": {"hp": 50, "max_hp": 50, "mp": 60, "max_mp": 60, "atk": 7, "def": 4},
}

MONSTERS = {
    "Imp": {"hp": 20, "max_hp": 20, "atk": 5, "def": 2, "exp": 10, "gold": 5},
    "Wolf": {"hp": 30, "max_hp": 30, "atk": 8, "def": 3, "exp": 15, "gold": 8},
    "Garland": {"hp": 150, "max_hp": 150, "atk": 20, "def": 10, "exp": 100, "gold": 100},
}

LOCATIONS = {
    "Coneria": {
        "description": "The City of Dreams. A peaceful town.",
        "connections": ["Forest"],
        "has_inn": True,
        "has_king": True
    },
    "Forest": {
        "description": "A dark forest filled with monsters.",
        "connections": ["Coneria", "Chaos Shrine"],
        "monsters": ["Imp", "Wolf"]
    },
    "Chaos Shrine": {
        "description": "A dark shrine where Garland resides.",
        "connections": ["Forest"],
        "monsters": ["Imp", "Garland"]
    }
}

# --- Game Logic Functions ---
def init_game():
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
        st.session_state.player = None
        st.session_state.location = "Coneria"
        st.session_state.inventory = []
        st.session_state.gold = 100
        st.session_state.logs = ["Welcome to Final Fantasy Streamlit!"]
        st.session_state.quest_progress = 0
        st.session_state.battle = None
        st.session_state.game_over = False

def reset_game():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def start_game(char_class):
    st.session_state.player = CLASSES[char_class].copy()
    st.session_state.player['class'] = char_class
    st.session_state.player['lvl'] = 1
    st.session_state.player['exp'] = 0
    st.session_state.game_started = True
    st.session_state.game_over = False
    st.session_state.logs.append(f"Started journey as a {char_class}!")

def move_to(new_loc):
    st.session_state.location = new_loc
    st.session_state.logs.append(f"Moved to {new_loc}.")
    if "monsters" in LOCATIONS[new_loc] and random.random() < 0.4:
        trigger_battle(new_loc)

def trigger_battle(loc):
    monster_name = random.choice(LOCATIONS[loc]["monsters"])
    if monster_name == "Garland" and st.session_state.quest_progress != 1:
        monster_name = "Imp"

    monster_stats = MONSTERS[monster_name].copy()
    st.session_state.battle = {
        "monster_name": monster_name,
        "monster_hp": monster_stats["hp"],
        "monster_max_hp": monster_stats["hp"],
        "monster_atk": monster_stats["atk"],
        "monster_def": monster_stats["def"],
        "monster_exp": monster_stats["exp"],
        "monster_gold": monster_stats["gold"]
    }
    st.session_state.logs.append(f"Encountered a {monster_name}!")

def player_attack():
    damage = max(1, st.session_state.player['atk'] - st.session_state.battle['monster_def'] + random.randint(-2, 2))
    st.session_state.battle['monster_hp'] -= damage
    st.session_state.logs.append(f"You attacked for {damage} damage!")
    if st.session_state.battle['monster_hp'] <= 0:
        win_battle()
    else:
        monster_attack()

def player_magic():
    if st.session_state.player['mp'] >= 10:
        st.session_state.player['mp'] -= 10
        damage = st.session_state.player['lvl'] * 15 + random.randint(5, 15)
        st.session_state.battle['monster_hp'] -= damage
        st.session_state.logs.append(f"You cast Fire! Dealt {damage} damage!")
        if st.session_state.battle['monster_hp'] <= 0:
            win_battle()
        else:
            monster_attack()
    else:
        st.session_state.logs.append("Not enough MP!")

def monster_attack():
    damage = max(1, st.session_state.battle['monster_atk'] - st.session_state.player['def'] + random.randint(-2, 2))
    st.session_state.player['hp'] -= damage
    st.session_state.logs.append(f"{st.session_state.battle['monster_name']} attacked for {damage} damage!")
    if st.session_state.player['hp'] <= 0:
        st.session_state.game_over = True
        st.session_state.logs.append("You have been defeated... Game Over.")

def win_battle():
    exp = st.session_state.battle['monster_exp']
    gold = st.session_state.battle['monster_gold']
    st.session_state.player['exp'] += exp
    st.session_state.gold += gold
    st.session_state.logs.append(f"Victory! Gained {exp} EXP and {gold} Gold.")
    st.toast(f"Victory! +{exp} EXP, +{gold} G")

    if st.session_state.battle['monster_name'] == "Garland":
        st.session_state.quest_progress = 2
        st.session_state.logs.append("You defeated Garland! The Princess is safe.")
        st.balloons()

    if st.session_state.player['exp'] >= st.session_state.player['lvl'] * 50:
        level_up()

    st.session_state.battle = None

def level_up():
    st.session_state.player['lvl'] += 1
    st.session_state.player['max_hp'] += 20
    st.session_state.player['hp'] = st.session_state.player['max_hp']
    st.session_state.player['atk'] += 5
    st.session_state.player['def'] += 2
    if st.session_state.player['max_mp'] > 0:
        st.session_state.player['max_mp'] += 10
        st.session_state.player['mp'] = st.session_state.player['max_mp']
    st.session_state.logs.append(f"LEVEL UP! Reached Level {st.session_state.player['lvl']}!")
    st.toast(f"Level Up! Level {st.session_state.player['lvl']}")

def rest_at_inn():
    if st.session_state.gold >= 10:
        st.session_state.gold -= 10
        st.session_state.player['hp'] = st.session_state.player['max_hp']
        st.session_state.player['mp'] = st.session_state.player['max_mp']
        st.session_state.logs.append("Rested at the Inn. HP/MP restored!")
        st.toast("HP/MP Restored!")
    else:
        st.session_state.logs.append("Not enough gold to rest at the Inn.")

def talk_to_king():
    if st.session_state.quest_progress == 0:
        st.session_state.quest_progress = 1
        st.session_state.logs.append("King: Please rescue my daughter from Garland at the Chaos Shrine!")
    elif st.session_state.quest_progress == 2:
        st.session_state.quest_progress = 3
        st.session_state.gold += 500
        st.session_state.logs.append("King: Thank you for saving the Princess! Here is 500 Gold.")
        st.balloons()
    else:
        st.session_state.logs.append("King: Good luck on your journey!")

# --- UI Layout ---
st.set_page_config(page_title="FF1 Streamlit Edition", page_icon="⚔️")
init_game()

if not st.session_state.game_started:
    st.title("⚔️ Final Fantasy 1: Streamlit Edition")
    st.write("Welcome, Warrior of Light. Choose your path:")
    cols = st.columns(len(CLASSES))
    for i, (name, stats) in enumerate(CLASSES.items()):
        with cols[i]:
            st.markdown(f"### {name}")
            st.write(f"❤️ HP: {stats['hp']}")
            st.write(f"✨ MP: {stats['mp']}")
            st.write(f"🗡️ ATK: {stats['atk']}")
            if st.button(f"Choose {name}", key=f"btn_{name}", use_container_width=True):
                start_game(name)
                st.rerun()
elif st.session_state.game_over:
    st.title("💀 Game Over")
    st.error("You have been defeated...")
    if st.button("Restart Journey"):
        reset_game()
    st.divider()
    st.write("### 📜 Final Logs")
    for log in reversed(st.session_state.logs[-10:]):
        st.write(log)
else:
    # Sidebar
    st.sidebar.title("👤 Character Stats")
    st.sidebar.write(f"**Class:** {st.session_state.player['class']}")
    st.sidebar.write(f"**Level:** {st.session_state.player['lvl']}")
    st.sidebar.progress(max(0.0, min(1.0, st.session_state.player['hp'] / st.session_state.player['max_hp'])), text=f"HP: {st.session_state.player['hp']}/{st.session_state.player['max_hp']}")
    if st.session_state.player['max_mp'] > 0:
        st.sidebar.progress(max(0.0, min(1.0, st.session_state.player['mp'] / st.session_state.player['max_mp'])), text=f"MP: {st.session_state.player['mp']}/{st.session_state.player['max_mp']}")
    st.sidebar.write(f"**Gold:** {st.session_state.gold} G")

    st.sidebar.divider()
    st.sidebar.title("❓ Quest Helper")
    helper_text = ""
    next_dest = ""
    if st.session_state.quest_progress == 0:
        helper_text = "Talk to the King in Coneria to start your quest."
        if st.session_state.location == "Coneria": next_dest = "King"
    elif st.session_state.quest_progress == 1:
        helper_text = "Head to the Chaos Shrine and defeat Garland."
        if st.session_state.location == "Coneria": next_dest = "Forest"
        elif st.session_state.location == "Forest": next_dest = "Chaos Shrine"
    elif st.session_state.quest_progress == 2:
        helper_text = "You defeated Garland! Return to the King in Coneria."
        if st.session_state.location == "Chaos Shrine": next_dest = "Forest"
        elif st.session_state.location == "Forest": next_dest = "Coneria"
        elif st.session_state.location == "Coneria": next_dest = "King"
    else:
        helper_text = "You have saved the kingdom! Enjoy your stay."
    st.sidebar.info(helper_text)

    if st.sidebar.button("Reset Game"):
        reset_game()

    if st.session_state.battle:
        st.title(f"⚔️ Battle: {st.session_state.battle['monster_name']}")
        st.write(f"Monster HP: {st.session_state.battle['monster_hp']} / {st.session_state.battle['monster_max_hp']}")
        st.progress(max(0.0, min(1.0, st.session_state.battle['monster_hp'] / st.session_state.battle['monster_max_hp'])))

        battle_cols = st.columns(3)
        with battle_cols[0]:
            if st.button("Attack", use_container_width=True):
                player_attack()
                st.rerun()
        with battle_cols[1]:
            if st.session_state.player['max_mp'] > 0:
                if st.button("Magic (10 MP)", use_container_width=True):
                    player_magic()
                    st.rerun()
            else:
                st.button("No MP", disabled=True, use_container_width=True)
        with battle_cols[2]:
            if st.button("Run", use_container_width=True):
                if random.random() < 0.6:
                    st.session_state.battle = None
                    st.session_state.logs.append("Successfully escaped!")
                else:
                    st.session_state.logs.append("Failed to escape!")
                    monster_attack()
                st.rerun()
    else:
        st.title(f"📍 {st.session_state.location}")
        st.write(LOCATIONS[st.session_state.location]["description"])

        st.write("### Actions")
        nav_cols = st.columns(len(LOCATIONS[st.session_state.location]["connections"]))
        for i, conn in enumerate(LOCATIONS[st.session_state.location]["connections"]):
            with nav_cols[i]:
                label = f"Go to {conn}"
                if conn == next_dest:
                    label += " 📍"
                if st.button(label, use_container_width=True):
                    move_to(conn)
                    st.rerun()

        st.write("### Interactions")
        int_cols = st.columns(2)
        with int_cols[0]:
            if LOCATIONS[st.session_state.location].get("has_inn"):
                if st.button("Rest at Inn (10 G)", use_container_width=True):
                    rest_at_inn()
                    st.rerun()
        with int_cols[1]:
            if LOCATIONS[st.session_state.location].get("has_king"):
                label = "Talk to King"
                if next_dest == "King":
                    label += " 📍"
                if st.button(label, use_container_width=True):
                    talk_to_king()
                    st.rerun()

    st.divider()
    st.write("### 📜 Adventure Logs")
    for log in reversed(st.session_state.logs[-8:]):
        st.write(log)
