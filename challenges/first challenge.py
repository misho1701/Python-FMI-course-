costadines_requirements = ('вино', 'презервативи', 'струни за китара',
                           'презервативи', 'перце за китара',
                           'презервативи', 'пица',
                           'бонбони', 'презервативи')

victors_requirements = ['вино', 'баница', 'цяло пиле', 'туршия',
                        'кисело зеле', 'зехтин', 'картофи', 'вино',
                        'кисели краставички', 'яйца']


joans_requirements = (list(costadines_requirements) +
                      victors_requirements +
                      ['лубрикант', 'хавлия', 'маска на кон'])

unique_requirements = set(joans_requirements)

unique_requirements.add("skyr")

shopping_quantities = dict.fromkeys(unique_requirements, 5)

total_items_to_buy = len(unique_requirements)

print("Уникални продукти:", unique_requirements)
print("Списък за пазаруване:", shopping_quantities)
print("Общо различни продукти за купуване:", total_items_to_buy)