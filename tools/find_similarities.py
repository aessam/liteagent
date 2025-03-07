import glob
import json

def get_paths(data, current_path=""):
    paths = set()
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{current_path}/{key}" if current_path else key
            paths.add(new_path)
            paths.update(get_paths(value, new_path))
    elif isinstance(data, list):
        for item in data:
            paths.update(get_paths(item, current_path + "/*"))
    return paths

def main():
    json_files = glob.glob(".tool_test/*.json")
    groups = {}  # key: tuple of sorted paths, value: list of file names
    contins_tool_call = []
    for file in json_files:
        try:
            with open(file, 'r') as f:
                try:
                    data = json.load(f)
                except Exception as e:
                    data = list(map(json.loads, f.readlines()))
            structure = sorted(get_paths(data))
            for coll in structure:
                if "tool_calls" in coll:
                    contins_tool_call.append(file)
                    break
            key = tuple(structure)
            groups.setdefault(key, []).append(file)
        except Exception as e:
            print(f"Error processing {file}: {e}")

    for idx, (structure, files) in enumerate(groups.items(), 1):
        print(f"Group {idx}:")
        for path in structure:
            print(path)
        print("Files:", files)
        print("-" * 40)

    print("Files with tool_call in xpath:", "\n".join(set(contins_tool_call)))
    print("-" * 40)
    print("Files without tool_call in xpath:", "\n".join(set(json_files) - set(contins_tool_call)))
    print("-" * 40)
if __name__ == "__main__":
    main()
