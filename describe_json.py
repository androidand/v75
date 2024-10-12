import json

def describe_json(json_data, indent=0, max_depth=3, current_depth=0):
    """Generates a concise description of a JSON object with improved list descriptions."""
    description = ""
    
    if current_depth > max_depth:
        return description

    if isinstance(json_data, dict):
        description += "Object:\n"
        for key, value in json_data.items():
            description += " " * indent + f"- {key} ({type(value).__name__}):\n"
            if current_depth < max_depth:  # Limit recursion depth
                description += describe_json(value, indent + 2, max_depth, current_depth + 1)

    elif isinstance(json_data, list):
        description += "List:\n"
        if json_data:
            first_element = json_data[0]
            if isinstance(first_element, dict):
                description += " " * indent + "- Contains dictionaries with keys like: "
                sample_keys = ", ".join(first_element.keys())
                description += f"{sample_keys[:50]}...\n" if len(sample_keys) > 50 else sample_keys + "\n"

                # Optionally show a sample element for better understanding
                description += " " * (indent + 2) + "Example item:\n"
                description += describe_json(first_element, indent + 4, max_depth, current_depth + 1)

            else:
                description += " " * indent + f"- Contains {type(first_element).__name__} elements.\n"
        else:
            description += " " * indent + "- Empty list.\n"

    elif isinstance(json_data, (str, int, float, bool, type(None))):
        description += " " * indent + f"- Value: {json_data}\n"

    return description

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python describe_json.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    # Load JSON data from file
    with open(filename, "r") as f:
        data = json.load(f)

    # Generate description with limited depth
    description = describe_json(data, max_depth=3)

    # Save output to a text file for better viewing
    with open('json_description.txt', 'w') as output_file:
        output_file.write(description)

    print("JSON description saved to 'json_description.txt'.")
