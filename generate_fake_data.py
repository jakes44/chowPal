from db_manager import DBManager
import random
import json
import pprint

food_allergies = ['peanut', 'sesame', 'soy', 'gluten', 'vegetarian', 'shellfish']

dbManager = DBManager("DB/chow.db")

uids = []

for i in range(10):
    allergy_count = random.randrange(len(food_allergies))
    allergies = " ".join(random.sample(food_allergies, allergy_count))
    uid = dbManager.create_user_profile(allergies)
    uids.append(uid)

uids_set = set(uids)

all_uids = dbManager.get_all_uid()

#assert len([i for i in all_uids if i not in uids_set]) == 0

with open('mcdonald.json', 'r') as mcdonald_file:
    mcdonald_data = json.load(mcdonald_file)

dbManager.import_restaurant_info(mcdonald_data)

dishes = dbManager.get_all_dishes()

scores = [1, -0.1]

for i in range(50):
    user = random.choice(uids)
    dish = random.choice(dishes)

    s = random.choice(scores)
    cid = dbManager.add_user_choice(user, dish, s)

    if s > 0:
        dbManager.add_user_rating(cid, random.randrange(6))

#for i in range(10):
#    print dbManager.get_order_history(uids[i])
#
#for d in dishes:
#    print dbManager.get_blurb(d)
#    pprint.pprint(dbManager.get_health(d))
#    print "--------------"
