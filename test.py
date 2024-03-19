from game.user import Me

me = Me()

#set the parameters
me.add_deck("main",{1:2,3:1})
me.set_token("test_token")
me.update_file() # save the current data to a file

del me # delete the object 

new_me = Me()
new_me.get_file() # restore the previously written data
print(f"line 14: {new_me.token}")
print(f"line 15: {new_me.decks}")

#trigger the duplicate deck test
print(f"line 17: {new_me.add_deck("main",{1:2,3:1})}")
