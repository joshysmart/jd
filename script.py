import json

with open("symptoms.json") as f:
    lines = f.read()
    input_json = json.loads(lines)
    output_json = []
    for x in input_json:
        output_json.append({
            x["Name"]: x["ID"]
        })
    with open("symptoms2.json", "w") as f2:
        f2.write(str(output_json))
    print(output_json)
    # for line in lines:
    #     print(line)

    # print(lines[0])
