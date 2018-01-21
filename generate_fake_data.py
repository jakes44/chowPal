from db_manager import DBManager
import random

food_allergies = ['peanut', 'sesame', 'soy', 'gluten', 'vegetarian', 'shellfish']

dbManager = DBManager("DB/chow.db")

uids = []

for i in range(100):
    allergy_count = random.randrange(len(food_allergies))
    allergies = " ".join(random.sample(food_allergies, allergy_count))
    uid = dbManager.create_user_profile(allergies)
    uids.append(uid)

uids_set = set(uids)

all_uids = dbManager.get_all_uid()

assert len([i for i in all_uids if i not in uids_set]) == 0
