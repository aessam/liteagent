import json
import sys

def get_node_by_xpath(data, path):
    tokens = path.strip('/').split('/')
    
    def search(node, tokens):
        if not tokens:
            return node  # Found the node
        
        token = tokens[0]
        rest = tokens[1:]
        
        if token == '*':
            # Wildcard: check every child if it's a dict or every element if it's a list.
            if isinstance(node, dict):
                for key in node:
                    result = search(node[key], rest)
                    if result is not None:
                        return result
            elif isinstance(node, list):
                for item in node:
                    result = search(item, rest)
                    if result is not None:
                        return result
            return None
        
        # If token is an integer index (for lists)
        try:
            index = int(token)
            if isinstance(node, list) and 0 <= index < len(node):
                return search(node[index], rest)
            else:
                return None
        except ValueError:
            # Token is a string key for dictionaries
            if isinstance(node, dict) and token in node:
                return search(node[token], rest)
            else:
                return None

    return search(data, tokens)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python script.py <json_file> <xpath_string>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    xpath_string = sys.argv[2]
    
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    result = get_node_by_xpath(data, xpath_string)
    print("Found node:", result)
