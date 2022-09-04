def stockEntity(item) -> dict:
    return {
        "model_no": item['model'],
        "description": item['description'],
        "price": item['price']
    }

def stocksEntity(entity) -> list:
    return [stockEntity(item) for item in entity]