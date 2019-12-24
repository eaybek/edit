from edit.edit import Edit
sample_input="/home/erdem/Masaüstü/edit.sample"
with open(sample_input,"w") as f:
    f.writelines(
        [
            "Hello World\n",
            "How are you",
        ]
    )

with Edit(sample_input) as buffer:
    buffer.search(r"^How .*$")
    buffer.openline()
    buffer.write("greetings")

add_attr("new = asdljfkla")


with open(sample_input, "r") as f:
    print("¶".join(f.readlines()))
