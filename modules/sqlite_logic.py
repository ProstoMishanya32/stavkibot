import sqlite3 as sq
def start():
	global base, cur
	base = sq.connect(f"database/db.db")
	print('The database is connected ')
	cur = base.cursor()

	base.execute("""
		CREATE TABLE IF NOT EXISTS 
		check_stavki (
		tree_id TEXT PRIMARY KEY,
		name TEXT,
		league TEXT,
		country TEXT,
		alerts INT default 0)""")
	base.commit()


def get_treeID():
	list_id = cur.execute('SELECT tree_id FROM check_stavki').fetchall()
	return list_id

def finish_check(treeId):
	list_id = cur.execute('SELECT alerts FROM check_stavki WHERE tree_id = ?', (treeId,)).fetchone()
	return list_id

def update_finish(treeId):
	cur.execute("UPDATE check_stavki  SET (alerts) = (?) WHERE tree_id = ?", (1, treeId))
	base.commit()

def get_text(treeId):
	name = cur.execute('SELECT name FROM check_stavki WHERE tree_id = ?', (treeId,)).fetchall()
	country = cur.execute('SELECT country FROM check_stavki WHERE tree_id = ?', (treeId,)).fetchall()
	league = cur.execute('SELECT league FROM check_stavki WHERE tree_id = ?', (treeId,)).fetchall()
	return name[0], country[0], league[0]
	#name, country, league

def check_stavki(treeId, name):
	list_id = cur.execute('SELECT tree_id FROM check_stavki WHERE tree_id = ?', (treeId,)).fetchone()
	if len(list_id) == 0:
		cur.execute('INSERT INTO check_stavki(tree_id, name) VALUES (?, ?)', (treeId, name))
		base.commit()
	else:
		pass

def add_stavki(treeId, name):
	cur.execute('INSERT INTO check_stavki(tree_id, name) VALUES (?, ?)', (treeId, name))
	base.commit()
	return True


def add_stavki_league(league, country, treeId):
	cur.execute("UPDATE check_stavki  SET (league, country) = (?, ?) WHERE tree_id = ?", (league, country, treeId))
	base.commit()
	return True
#async def sql_moderators_admin_add_list(state):
#	async with state.proxy() as data:
#	memory = [(f"{data['id_users']}: {data['usernames']}"), (data['id_users'])]
#		cur.execute('INSERT INTO moderators(id_usernames, id) VALUES (?, ?)', memory)
	#	base.commit()

#async def sql_moderators_admin_see_list(message):
#	users_id = cur.execute('SELECT id_usernames FROM moderators').fetchall()
	#for i, val in enumerate(list(users_id), start = 1):
	#	await bot.send_message(message.from_user.id, f"{i}. <b>{''.join(val)}</b>", parse_mode=types.ParseMode.HTML)

#async def sql_moderators_delete(state):
	#async with state.proxy() as data:
	#	cur.execute("DELETE FROM moderators WHERE id = ?", (data['delete_id_users'],) )
	#	base.commit()
