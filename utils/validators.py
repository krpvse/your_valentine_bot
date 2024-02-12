

async def validate_name(name: str) -> bool:
    """Validate name - not required name without letters, letters quantity > 1"""

    letters = 'abcdefghijklmnopqrstuvwxyz'
    letters_ru = 'абвгдеёжзийклмнопрстуфхцчшщьыъэюя'
    all_letters = letters + letters_ru + letters.upper() + letters_ru.upper()

    letters_in_name = [sign for sign in name if sign in all_letters]
    if len(letters_in_name) > 1:
        print(f'[Validation] Name "{name}" is GOOD')
        validation_result = True
    else:
        print(f'[Validation] Name "{name}" is WRONG')
        validation_result = False

    return validation_result


async def validate_description(name: str) -> tuple:
    """Validate description - letters quantity <= 512"""

    description_signs_qty = len(name)
    if description_signs_qty <= 512:
        print(f'[Validation] Name "{name}" is GOOD')
        validation_result = True
    else:
        print(f'[Validation] Name "{name}" is WRONG')
        validation_result = False

    return validation_result, description_signs_qty


async def validate_valentine_card(valentine_card: str) -> tuple:
    """Validate valentine card - letters quantity <= 512"""

    card_signs_qty = len(valentine_card)
    if card_signs_qty <= 512:
        print(f'[Validation] Valentine card "{valentine_card}" is GOOD')
        validation_result = True
    else:
        print(f'[Validation] Valentine card "{valentine_card}" is WRONG')
        validation_result = False

    return validation_result, card_signs_qty
