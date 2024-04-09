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
    print(order_validation_result)

    if event['invocationSource'] == 'DialogCodeHook':
        if not order_validation_result['isValid']:
            response_message = 'PizzaPal'
            if 'message' in order_validation_result:
                response_message = order_validation_result['message']

            response_card_sub_title = ''
            response_card_buttons = []

            pizza_paradise_sub_title = 'Please select a Pizza Paradise type pizza'
            pizza_paradise_buttons = [
                {
                    "text": "Vegetarian",
                    "value": "Vegetarian"
                },
                {
                    "text": "BBQ Chicken",
                    "value": "BBQ Chicken"
                },
                {
                    "text": "Pepperoni",
                    "value": "Pepperoni"
                }
            ]

            slice_heaven_sub_title = 'Please select a Slice Heaven type pizza'
            slice_heaven_buttons = [
                {
                    "text": "Margherita",
                    "value": "Margherita"
                },
                {
                    "text": "Hawaiian",
                    "value": "Hawaiian"
                },
                {
                    "text": "Meat Lovers",
                    "value": "Meat Lovers"
                }
            ]

            crispy_crust_pizzeria_sub_title = 'Please select a Crispy Crust Pizzeria type pizza'
            crispy_crust_pizzeria_buttons = [
                {
                    "text": "Thin Crust",
                    "value": "Thin Crust"
                },
                {
                    "text": "Roman",
                    "value": "Roman"
                },
                {
                    "text": "Grilled",
                    "value": "Grilled"
                }
            ]

            if order_validation_result['invalidSlot'] == "PizzaSize":
                response_card_sub_title = "Please select a Pizza size"
                response_card_buttons = [
                    {
                        "text": "Small",
                        "value": "Small"
                    },
                    {
                        "text": "Medium",
                        "value": "Medium"
                    },
                    {
                        "text": "Large",
                        "value": "Large"
                    },
                    {
                        "text": "Extra-Large",
                        "value": "Extra-Large"
                    }
                ]

            if order_validation_result['invalidSlot'] == "PizzaFranchise":
                response_card_sub_title = "Please select a Pizza Franchise"
                response_card_buttons = [
                    {
                        "text": "Pizza Paradise",
                        "value": "Pizza Paradise"
                    },
                    {
                        "text": "Slice Heaven",
                        "value": "Slice Heaven"
                    },
                    {
                        "text": "Crispy Crust Pizzeria",
                        "value": "Crispy Crust Pizzeria"
                    }
                ]

            if order_validation_result['invalidSlot'] == "PizzaType":
                if order_validation_result['invalidFranchise'] == "pizza_paradise":
                    response_card_sub_title = pizza_paradise_sub_title
                    response_card_buttons = pizza_paradise_buttons
                elif order_validation_result['invalidFranchise'] == "slice_heaven":
                    response_card_sub_title = slice_heaven_sub_title
                    response_card_buttons = slice_heaven_buttons
                elif order_validation_result['invalidFranchise'] == "crispy_crust_pizzeria":
                    response_card_sub_title = crispy_crust_pizzeria_sub_title
                    response_card_buttons = crispy_crust_pizzeria_buttons
                else:
                    response_card_sub_title = 'Please select a pizza type'
                    response_card_buttons = [
                        {
                            "text": "Vegetarian",
                            "value": "Vegetarian"
                        },
                        {
                            "text": "Margherita",
                            "value": "Margherita"
                        },
                        {
                            "text": "Thin Crust",
                            "value": "Thin Crust"
                        }
                    ]

            response = {
                "sessionState": {
                    "dialogAction": {
                        "slotToElicit": order_validation_result['invalidSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        "name": intent,
                        "slots": slots,
                    }
                },
                "messages": [
                    {
                        "contentType": "ImageResponseCard",
                        "content": response_message,
                        "imageResponseCard": {
                            "title": "PizzaPal",
                            "subtitle": response_card_sub_title,
                            "imageUrl": "https://pizzapalbot.s3.ap-southeast-2.amazonaws.com/WebPage/img/sm_robot.png",
                            "buttons": response_card_buttons
                        }
                    }
                ]
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