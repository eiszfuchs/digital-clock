import json
import math

from PIL import Image


ticks_per_24h = 20 * 60 * 20
ticks_per_minute = ticks_per_24h / (24 * 60)
cell_size = 32
cell_count = 24 * 60

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

clock_data: dict = {
    "parent": "minecraft:item/generated",
    "textures": {"layer0": "digiclock:item/clock_1200"},
    "overrides": [],
}


def frac(v: float) -> float:
    return v - math.floor(v)


def ticks_to_time_predicate(ticks: int) -> float:
    d = frac(ticks / 24000 - 0.25)
    e = 0.5 - math.cos(d * math.pi) / 2
    return (d * 2 + e) / 3


def ticks_to_minutes(ticks: int) -> int:
    return int(ticks / ticks_per_minute)


current_minutes: int = 0
for y in range(0, cell_count):
    face_image = Image.new("RGBA", (cell_size, cell_size))

    current_ticks: int = int(current_minutes * ticks_per_minute)

    clock_minutes = current_minutes + 6 * 60
    digits = f"{int(clock_minutes / 60) % 24:02}{int(clock_minutes % 60):02}"

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

    # draw the colon
    face_image.putpixel((x_offset + (2 * 4), y_offset + 4), 0xFF181616)
    face_image.putpixel((x_offset + (2 * 4), y_offset + 2), 0xFF181616)

    face_image.paste(top, (0, 0), top)

    current_minutes += 1

    clock_data["overrides"].append(
        {
            "predicate": {"time": ticks_to_time_predicate(int(current_ticks))},
            "model": f"digiclock:item/clock_{digits}",
        }
    )

    face_data = {
        "parent": "minecraft:item/generated",
        "textures": {
            "layer0": f"digiclock:item/clock_{digits}",
        },
    }

    face_image.save(f"../assets/digiclock/textures/item/clock_{digits}.png")

    with open(f"../assets/digiclock/models/item/clock_{digits}.json", "w") as face_file:
        json.dump(face_data, face_file, indent="\t")

clock_data["overrides"] = sorted(
    clock_data["overrides"], key=lambda d: d["predicate"]["time"]
)
with open("../assets/minecraft/models/item/clock.json", "w") as item_file:
    json.dump(clock_data, item_file, indent="\t")
