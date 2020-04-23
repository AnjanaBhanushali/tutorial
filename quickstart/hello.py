import json

def main123():

    name = ["anjana", "bhavika", "ukti"]
    id = ["1", "2", "3"]
    no = ["85421", "76235", "65241"]
    # for i in range(0,3):
    input_dict = {'foo': 3, 'bar': 1}
    result = []

    for k, v in input_dict.items():
        result.append({'key': k, 'value': v})

    j_object = json.dumps(result, indent=4)
    # print(j_object)

    with open("person123.json", "w") as fp:
        fp.write(j_object)
        fp.close()

    """
    for i in range(len(name)):
        dic = {
            "id": id[i],
            "name": name[i],
            "no": no[i]
        }

        j_object[i] = json.dumps(dic, indent=4)
        print(j_object1)
        with open("person.json", "w") as fp:
            fp.write(j_object1)

    
    import json
    json_dict = {'foo': 3, 'bar': 1}
    json_array = [ {'key' : k, 'value' : json_dict[k]} for k in json_dict]
    print(json.dumps(json_array))
    """

if __name__ == '__main123__':
    main123()