import json

RARITY_ORDER = [
    "Contraband", "Covert", "Classified",
    "Restricted", "Mil-Spec Grade", "Industrial Grade", "Consumer Grade",
]
    
# Assigns arbitrary prices for testing purposes

def update_prices(data):
    for crate in data:
        crate["cost"] = 0
        for rarity, items in crate.get("contains", []).items():
            for item in items:
                match rarity:
                    
                    case "Contraband":
                        item["price"] = 100
                        continue
                    
                    case "Covert":
                        item["price"] = 50
                        continue
                    
                    case "Classified":
                        item["price"] = 20
                        continue
                    
                    case "Restricted":
                        item["price"] = 10
                        continue
                    
                    case "Mil-Spec Grade":
                        item["price"] = 5
                        continue
                      
                    case "Industrial Grade":
                        item["price"] = 2
                        continue

                    case "Consumer Grade":
                        item["price"] = 1
                        continue

def main():
    with open("games/case_game/case_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    update_prices(data)

    with open("games/case_game/case_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
