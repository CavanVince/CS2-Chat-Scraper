import json

def parse_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def iter_items(root):
    # Yield every item under each crate's "contains"
    if isinstance(root, list):
        for crate in root:
            for item in crate.get("contains", []):
                yield item
            for item in crate.get("contains_rare", []):
                yield item
    elif isinstance(root, dict):
        for item in root.get("contains", []):
            yield item
        for item in root.get("contains_rare", []):
            yield item

def normalize(path_in="games/CaseGame/case_data.json",
              path_out="games/CaseGame/case_data.json"):
    data = parse_json(path_in)
    modified = 0

    for item in iter_items(data):
        name = item.get("name", "")

        r = item.get("rarity")
        rarity_name = r.get("name") if isinstance(r, dict) else r  # dict|string|None

        # Starred -> Contraband
        if "★" in name:
            if item.get("rarity") != "Contraband":
                item["rarity"] = "Contraband"
                modified += 1
            continue

        # Normalize known rarities
        KNOWN = {
            "Consumer Grade",
            "Industrial Grade",
            "Mil-Spec Grade",
            "Restricted",
            "Classified",
            "Covert",
            "Contraband"
        }
        if rarity_name in KNOWN and item.get("rarity") != rarity_name:
            item["rarity"] = rarity_name
            modified += 1

    with open(path_out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Modified items: {modified}")
    
RARITY_ORDER = [
    "Consumer Grade",
    "Industrial Grade",
    "Mil-Spec Grade",
    "Restricted",
    "Classified",
    "Covert",
    "Contraband"
]

def buckets_contains(case):
    items = case.get("contains", [])
    c_items = case.get("contains_rare", [])
    buckets = {r: [] for r in RARITY_ORDER} 
    for item in items:
        rarity = item.get("rarity", "")
        item.pop("image", None)
        item.pop("id", None)
        if rarity in buckets:
            buckets[rarity].append(item)
    for item in c_items:
        rarity = item.get("rarity", "")
        item.pop("image", None)
        item.pop("id", None)
        if rarity in buckets:
            buckets[rarity].append(item)
        
    case["contains"] = {r: buckets[r] for r in RARITY_ORDER if buckets[r]}
    case["contains_rare"] = [item for item in c_items if item.get("rarity", "") in RARITY_ORDER]

    return case

def clean_cases(path_in="games/CaseGame/case_data.json",
                      path_out="games/CaseGame/case_data.json"):
    data = parse_json(path_in)

    for case in data:
        buckets_contains(case)
        case.pop("contains_rare", None)
        case.pop("description", None)
        case.pop("id", None)
        case.pop("rarity", None)
        case.pop("first_sale_date", None)
        case.pop("image", None)
        case.pop("market_hash_name", None)
        case.pop("rental", None)
        case.pop("model_player", None)
        case.pop("loot_list", None)

    with open(path_out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    

if __name__ == "__main__":
    normalize()
    clean_cases()
