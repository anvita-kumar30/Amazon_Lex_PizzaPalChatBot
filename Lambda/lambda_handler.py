import json

pizza_sizes = ['small', 'medium', 'large', 'extra-large']
pizza_franchises = ['pizza paradise', 'slice heaven', 'crispy crust pizzeria']
pizza_paradise_types = ['vegetarian', 'bbq chicken', 'pepperoni']
slice_heaven_types = ['margherita', 'hawaiian', 'meat lovers']
crispy_crust_pizzeria_types = ['thin crust', 'roman', 'grilled']


def validate_order(slots):
    # Validate PizzaSize
    if not slots['PizzaSize']:
        print('Validating PizzaSize Slot')

        return {
            'isValid': False,
            'invalidSlot': 'PizzaSize'
        }

    if slots['PizzaSize']['value']['originalValue'].lower() not in pizza_sizes:
        print('Invalid PizzaSize')

        return {
            'isValid': False,
            'invalidSlot': 'PizzaSize',
            'message': 'Please select a {} pizza size.'.format(", ".join(pizza_sizes))
        }

    # Validate PizzaFranchise
    if not slots['PizzaFranchise']:
        print('Validating PizzaFranchise Slot')

        return {
            'isValid': False,
            'invalidSlot': 'PizzaFranchise'
        }

    if slots['PizzaFranchise']['value']['originalValue'].lower() not in pizza_franchises:
        print('Invalid PizzaFranchise')

        return {
            'isValid': False,
            'invalidSlot': 'PizzaFranchise',
            'message': 'Please select from {} pizza franchises.'.format(", ".join(pizza_franchises))
        }

    # Validate PizzaType
    if not slots['PizzaType']:
        print('Validating PizzaType Slot')

        return {
            'isValid': False,
            'invalidSlot': 'PizzaType'
        }

    # Validate PizzaType for PizzaFranchise
    if slots['PizzaFranchise']['value']['originalValue'].lower() == 'pizza paradise':
        if slots['PizzaType']['value']['originalValue'].lower() not in pizza_paradise_types:
            print('Invalid PizzaType for Pizza Paradise')

            return {
                'isValid': False,
                'invalidSlot': 'PizzaType',
                'message': 'Please select a Pizza Paradise type of {}.'.format(", ".join(pizza_paradise_types))
            }

    if slots['PizzaFranchise']['value']['originalValue'].lower() == 'slice heaven':
        if slots['PizzaType']['value']['originalValue'].lower() not in slice_heaven_types:
            print('Invalid PizzaType for Slice Heaven')

            return {
                'isValid': False,
                'invalidSlot': 'PizzaType',
                'message': 'Please select a Slice Heaven type of {}.'.format(", ".join(slice_heaven_types))
            }

    if slots['PizzaFranchise']['value']['originalValue'].lower() == 'crispy crust pizzeria':
        if slots['PizzaType']['value']['originalValue'].lower() not in crispy_crust_pizzeria_types:
            print('Invalid PizzaType for Crispy Crust Pizzeria')

            return {
                'isValid': False,
                'invalidSlot': 'PizzaType',
                'message': 'Please select a Crispy Crust Pizzeria type of {}.'.format(", ".join(crispy_crust_pizzeria_types))
            }

    # Valid Order
    return {'isValid': True}


def lambda_handler(event, context):
    print(event)

    bot = event['bot']['name']
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']

    order_validation_result = validate_order(slots)

    if event['invocationSource'] == 'DialogCodeHook':
        if not order_validation_result['isValid']:
            if 'message' in order_validation_result:
                response = {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": order_validation_result['invalidSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        }
                    },
                    "messages": [
                        {
                            "contentType": "PlainText",
                            "content": order_validation_result['message']
                        }
                    ]
                }
            else:
                response = {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": order_validation_result['invalidSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        }
                    }
                }
        else:
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots
                    }
                }
            }

    if event['invocationSource'] == 'FulfillmentCodeHook':
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": intent,
                    "slots": slots,
                    "state": "Fulfilled"
                }

            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "I've placed your order."
                }
            ]
        }

    print(response)
    return response