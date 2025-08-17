#!/usr/bin/env python3
import ast
import os
import sys

class CallGraphBuilder(ast.NodeVisitor):
    def __init__(self):
        self.definitions = {}       # {function_name: line_number}
        self.call_graph = {}        # {function_name: set(called_function_names)}
        self.top_level_calls = set()  # calls made at module level
        self.current_function = None

    def visit_FunctionDef(self, node):
        # Record function definition and create graph entry
        self.definitions[node.name] = node.lineno
        self.call_graph.setdefault(node.name, set())
        # Set current context and visit the body
        prev_function = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = prev_function

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            called_name = node.func.id
            if self.current_function is not None:
                self.call_graph.setdefault(self.current_function, set()).add(called_name)
            else:
                # Call at module level (entry point)
                self.top_level_calls.add(called_name)
        self.generic_visit(node)

def analyze_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

    try:
        tree = ast.parse(source, filepath)
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return None

    builder = CallGraphBuilder()
    builder.visit(tree)
    defined = set(builder.definitions.keys())

    # Keep only edges to functions defined in the same file
    for func in builder.call_graph:
        builder.call_graph[func] = {callee for callee in builder.call_graph[func] if callee in defined}

    # Determine reachable functions starting from top-level calls
    reachable = set()
    def dfs(func):
        if func in reachable:
            return
        reachable.add(func)
        for callee in builder.call_graph.get(func, []):
            dfs(callee)

    for func in builder.top_level_calls:
        if func in defined:
            dfs(func)

    dead_functions = defined - reachable
    return builder.definitions, builder.call_graph, builder.top_level_calls, reachable, dead_functions

def get_dead_components(dead_functions, call_graph):
    # Build an undirected graph among dead functions to get connected groups
    graph = {func: set() for func in dead_functions}
    for func in dead_functions:
        for callee in call_graph.get(func, []):
            if callee in dead_functions:
                graph[func].add(callee)
                graph[callee].add(func)
    # Find connected components via DFS
    visited = set()
    components = []
    for func in dead_functions:
        if func not in visited:
            comp = set()
            stack = [func]
            while stack:
                current = stack.pop()
                if current in visited:
                    continue
                visited.add(current)
                comp.add(current)
                for neighbor in graph[current]:
                    if neighbor not in visited:
                        stack.append(neighbor)
            components.append(comp)
    return components

def analyze_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                print(f"\nAnalyzing file: {filepath}")
                result = analyze_file(filepath)
                if result is None:
                    continue
                definitions, call_graph, top_level_calls, reachable, dead_functions = result
                print(f"Total defined functions: {len(definitions)}")
                print(f"Reachable functions: {len(reachable)}")
                print(f"Potential dead functions: {dead_functions}")

                components = get_dead_components(dead_functions, call_graph)
                # Sort components by size (largest first)
                components.sort(key=lambda comp: len(comp), reverse=True)
                print("Dead call chain components (sorted by size):")
                for i, comp in enumerate(components, 1):
                    comp_funcs = ", ".join(sorted(comp))
                    print(f"  Component {i} (size {len(comp)}): {comp_funcs}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dead_code_chain.py <directory>")
    else:
        analyze_directory(sys.argv[1])
