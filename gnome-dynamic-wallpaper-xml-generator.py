#!/usr/bin/env python3
import argparse
import os
import jinja2


def render(template_path, output_path, context={}):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(["."])
    )
    template = env.get_template(template_path)
    output_text = template.render(**context)
    with open(output_path, "w") as output_file:
        output_file.write(output_text)


def get_wallpaper_images(wallpapers_root, wallpaper_name):
    wallpaper_root = os.path.join(wallpapers_root, wallpaper_name)
    images = ["" for _ in range(24)]
    home = os.path.expanduser("~")
    for filename in os.listdir(wallpaper_root):
        filepath = os.path.join(wallpaper_root, filename)
        if os.path.isfile(filepath):
            # ["0.jpeg", "1.jpeg", ..., "23.jpeg"]
            basename = filename.split(".")[0]
            if basename.isdigit():
                hour = int(basename)
                if 0 <= hour < 24:
                    images[hour] = os.path.relpath(filepath, start=home)
    return images


def main():
    parser = argparse.ArgumentParser(
        "gnome-dynamic-wallpaper-xml-generator",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="GNOME Dynamic Wallpaper XML Generator",
    )

    parser.add_argument(
        "-r",
        "--wallpapers-root",
        dest="wallpapers_root",
        default="./wallpapers",
        help="root dir for wallpapers collection"
    )

    parser.add_argument(
        "-s",
        "--static-duration",
        dest="static_duration",
        type=int,
        default=3595,
        help="static duration seconds",
    )

    parser.add_argument(
        "-t",
        "--transition-duration",
        dest="transition_duration",
        type=int,
        default=5,
        help="transition duration seconds",
    )

    args = parser.parse_args()
    wallpapers_root = os.path.abspath(args.wallpapers_root)
    for wallpaper_name in os.listdir(wallpapers_root):
        render(
            "gnome-background.xml.j2",
            os.path.join(wallpapers_root, wallpaper_name, wallpaper_name + ".xml"),
            context={
                "images": get_wallpaper_images(wallpapers_root, wallpaper_name),
                "static_duration": args.static_duration,
                "transition_duration": args.transition_duration,
            }
        )


if __name__ == "__main__":
    main()
