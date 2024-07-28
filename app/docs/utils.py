def get_description() -> str:
    with open("./app/docs/description.txt", "r") as file:
        description = file.read()
    return description
