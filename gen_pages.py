import mkdocs_gen_files
from pathlib import Path
import yaml
from tabulate import tabulate
import copy
from urllib.parse import urlparse

for file in Path("devices").glob("*.yaml"):

    device_type = file.stem

    # open yaml
    with open(file) as f:
        data = yaml.safe_load(f)

    # parse yaml
    title = data["title"]
    description = data["description"]
    devices = data["devices"]

    # Sort devices into protocols
    devices_sorted = {}
    for d in devices:
        protocols = d["protocol"]
        if type(protocols) is not list:
            protocols = [protocols]
        
        for p in protocols:
            if p not in devices_sorted:
                devices_sorted[p] = [d]
            else:
                devices_sorted[p].append(d)

    # create table
    table = []
    for d in devices:
        tb = copy.deepcopy(d)
        # remove things we don't want in table
        tb.pop("description")
        tb.pop("image")

        # Clean up url
        website = urlparse(tb["url"]).netloc
        tb["url"] = f"[{website}]({d['url']})"

        # Clean up protocols
        if type(tb["protocol"]) is list:
            tb["protocol"] = ", ".join(tb["protocol"])

        # tb["name"] = f"[{d['name']}](#{d['name']})"
        table.append(tb)
    table = tabulate(table, headers="keys", tablefmt="github")
        
    # create md
    md = ""
    md += f"# {title}\n\n"
    md += f"{description}\n\n"
    md += table
    for p, devices in sorted(devices_sorted.items()):
        md += f"\n\n## {p}\n\n"
        for d in devices:
            md += f"### {d['name']}\n\n"
            md += f"![{d['name']}](assets/{device_type}/{d['image']}){{: style='height:100px;width:100px' align='left'}}\n\n"
            md += f"{d['description']}\n\n"
            md += f"**URL**: [{d['url']}]({d['url']})\n\n"
            md += "<br clear='right'/>\n\n"

    # write md
    md_file = device_type + ".md"
    with mkdocs_gen_files.open(md_file, "w") as f:
        f.write(md)

    mkdocs_gen_files.set_edit_path(md_file, file)
