prompts = [
    "Generate a JSON product description with fields: title, features, and tags.",
    "Returnr a JSON product description with exactly these keys: title (string), features (list of strings), and tags (list of strings).",
    'Generate a JSON product description based on this example: {"title": "Phone", "features": ["Waterproof", "20h battery life"], "tags": ["phone", "bluetooth"]}',
    "Generate a JSON description of a product with a title, no more than 2 features, and up to 3 tags."
]

prompts_with_system =[
    (
        "You are a helpful assistant that always returns product data as a JSON object with the structure: title, features, tags.",
        "Generate a JSON description for a product."
    )
]