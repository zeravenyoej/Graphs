object_example = {
  "cat": "bob",
  "dog": 23,
  19: 18,
  90: "fish"
}

def get_the_answer(object):
    list_of_values = list(object.values())
    sum  = int()
    for value in list_of_values:
        if type(value) is int:
            sum +=value
    return sum


print(get_the_answer(object_example))