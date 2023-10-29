from PIL import Image
import math
import json

start_time = 12 * 60
minute_step = 1
total_steps = 24 * 60
cell_size = 32
cell_count = int(total_steps / minute_step)

x_offset = 7  # int(math.floor((cell_size - 17) / 2))
y_offset = 13  # int(math.floor((cell_size - 5) / 2))

base = Image.open("clock-base.png")
top = Image.open("clock-top.png")

digit_maps = [
    "111101101101111",
    "001001001001001",
    "111001111100111",
    "111001011001111",
    "101101111001001",
    "111100111001111",
    "100100111101111",
    "111001001001001",
    "111101111101111",
    "111101111001001",
]

clock_data = {
    "parent": "minecraft:item/generated",
    "textures": {"layer0": "digiclock:item/clock_1200"},
    "overrides": [],
}

time = start_time
for y in range(0, cell_count):
    face_image = Image.new("RGBA", (cell_size, cell_size))

    hour = math.floor(time / 60)
    hour = str(int(hour)).zfill(2)
    minute = time % 60
    minute = str(int(minute)).zfill(2)
    digits = hour + minute

    face_image.paste(base, (0, 0), base)

    for digit_index in range(4):
        digit = digits[digit_index]
        for dy in range(5):
            for dx in range(3):
                if digit_maps[int(digit)][dy * 3 + dx] == "0":
                    continue

                xy = (
                    x_offset + dx + digit_index * 4 + (2 if (digit_index >= 2) else 0),
                    y_offset + dy,
                )
                face_image.putpixel(xy, 0xFF181616)

    face_image.putpixel((x_offset + (2 * 4), y_offset + 4), 0xFF181616)
    face_image.putpixel((x_offset + (2 * 4), y_offset + 2), 0xFF181616)

    face_image.paste(top, (0, 0), top)

    time += minute_step
    time %= total_steps

    clock_data["overrides"].append(
        {
            "predicate": {
                "time": ((time + total_steps - start_time - 1) % total_steps)
                / total_steps
            },
            "model": "digiclock:item/clock_{time}".format(time=digits),
        }
    )

    face_data = {
        "parent": "minecraft:item/generated",
        "textures": {
            "layer0": "digiclock:item/clock_{time}".format(time=digits),
        },
    }

    face_image.save(
        "../assets/digiclock/textures/item/clock_{time}.png".format(time=digits)
    )

    with open(
        "../assets/digiclock/models/item/clock_{time}.json".format(time=digits), "w"
    ) as face_file:
        json.dump(face_data, face_file, indent="\t")

clock_data["overrides"] = sorted(
    clock_data["overrides"], key=lambda d: d["predicate"]["time"]
)
with open("../assets/minecraft/models/item/clock.json", "w") as item_file:
    json.dump(clock_data, item_file, indent="\t")
