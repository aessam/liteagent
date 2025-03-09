import json
import sys
from typing import Any, Dict, List, Optional, Union

def get_node_by_xpath(data: Any, path: str) -> Any:
    """
    Extract a node from a nested data structure using an XPath-like path.
    
    Args:
        data: The data structure to search through
        path: An XPath-like path to the node
        
    Returns:
        The node at the specified path, or None if not found
    """
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
        
        # Check if token is an array index
        if isinstance(node, list):
            try:
                index = int(token)
                if 0 <= index < len(node):
                    return search(node[index], rest)
            except ValueError:
                # Not an integer, so search for a matching key in each dict
                if token == 'type':
                    # Special case for matches by "type" field
                    for item in node:
                        if isinstance(item, dict) and len(rest) > 0 and item.get('type') == rest[0]:
                            return search(item, rest[1:])
                
                # Handle token[condition] syntax
                if '[' in token and token.endswith(']'):
                    field, condition = token.split('[', 1)
                    condition = condition[:-1]  # Remove the trailing ']'
                    
                    # Handle field='value' condition
                    if '=' in condition:
                        cond_field, value = condition.split('=', 1)
                        if value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]  # Remove quotes
                        
                        for item in node:
                            if isinstance(item, dict) and item.get(field, {}).get(cond_field) == value:
                                return search(item, rest)
                
                # Default behavior: search in each item
                for item in node:
                    if isinstance(item, dict) and token in item:
                        result = search(item[token], rest)
                        if result is not None:
                            return result
        
        # Try to access a key in a dictionary
        elif isinstance(node, dict) and token in node:
            return search(node[token], rest)
        
        return None
    
    return search(data, tokens)

def get_paths(data: Any, current_path: str = "") -> set:
    """
    Get all possible paths in a data structure.
    
    Args:
        data: The data structure to traverse
        current_path: The current path prefix
        
    Returns:
        A set of all paths in the data structure
    """
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

class XPathExtractor:
    """Utility class for extracting nodes using XPath-like paths."""
    
    def get_node(self, data: Any, path: str) -> Any:
        """
        Extract a single node from a nested data structure.
        
        Args:
            data: The data structure to search through
            path: An XPath-like path to the node
            
        Returns:
            The node at the specified path, or None if not found
        """
        return get_node_by_xpath(data, path)
    
    def get_nodes(self, data: Any, path: str) -> List[Any]:
        """
        Extract multiple nodes from a nested data structure.
        
        Args:
            data: The data structure to search through
            path: An XPath-like path to the nodes
            
        Returns:
            A list of nodes matching the path
        """
        tokens = path.strip('/').split('/')
        
        def _collect_nodes(node, tokens, results):
            if not tokens:
                results.append(node)
                return
            
            token = tokens[0]
            rest = tokens[1:]
            
            # Handle direct attribute matching (key=value)
            if '=' in token and '[' not in token:
                attr_name, attr_value = token.split('=', 1)
                # If the value is quoted, remove the quotes
                if attr_value.startswith(("'", '"')) and attr_value.endswith(("'", '"')):
                    attr_value = attr_value[1:-1]

                if isinstance(node, list):
                    for item in node:
                        if isinstance(item, dict) and item.get(attr_name) == attr_value:
                            _collect_nodes(item, rest, results)
                elif isinstance(node, dict):
                    # If node is a dict, check all values that are lists or dicts
                    for key, value in node.items():
                        if isinstance(value, (list, dict)):
                            _collect_nodes(value, tokens, results)
                return
            
            # Handle wildcard
            if token == '*':
                if isinstance(node, dict):
                    for key in node:
                        _collect_nodes(node[key], rest, results)
                elif isinstance(node, list):
                    for item in node:
                        _collect_nodes(item, rest, results)
            elif isinstance(node, dict) and token in node:
                _collect_nodes(node[token], rest, results)
            elif isinstance(node, list):
                # Try to interpret token as an index
                try:
                    index = int(token)
                    if 0 <= index < len(node):
                        _collect_nodes(node[index], rest, results)
                except ValueError:
                    # Not an integer, so search in each item
                    # Handle token[condition] syntax
                    if '[' in token and token.endswith(']'):
                        field, condition = token.split('[', 1)
                        condition = condition[:-1]  # Remove the trailing ']'
                        
                        # Handle field='value' condition
                        if '=' in condition:
                            cond_field, value = condition.split('=', 1)
                            if value.startswith("'") and value.endswith("'"):
                                value = value[1:-1]  # Remove quotes
                            
                            for item in node:
                                if isinstance(item, dict) and item.get(field, {}).get(cond_field) == value:
                                    _collect_nodes(item, rest, results)
                    
                    # Default behavior: search for the token in each item
                    for item in node:
                        if isinstance(item, dict) and token in item:
                            _collect_nodes(item[token], rest, results)
        
        results = []
        _collect_nodes(data, tokens, results)
        return results
    
    def path_exists(self, data: Any, path: str) -> bool:
        """
        Check if a path exists in a data structure.
        
        Args:
            data: The data structure to search through
            path: An XPath-like path to check
            
        Returns:
            True if the path exists, False otherwise
        """
        result = self.get_node(data, path)
        return result is not None
    
    def get_all_paths(self, data: Any) -> set:
        """
        Get all possible paths in a data structure.
        
        Args:
            data: The data structure to traverse
            
        Returns:
            A set of all paths in the data structure
        """
        return get_paths(data, "") 