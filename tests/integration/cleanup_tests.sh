#!/bin/bash
# Script to remove duplicate test files based on the cleanup plan

# Display what will be deleted
echo "The following files will be deleted:"
echo "---------------------------------"
echo "Duplicate observer: tests/integration/test_observer.py"
echo "Model-specific tests:"
echo "  tests/integration/test_anthropic_claude.py"
echo "  tests/integration/test_groq_llama.py"
echo "  tests/integration/test_ollama_phi.py"
echo "  tests/integration/test_gpt4o_mini.py"
echo "Other duplicated tests:"
echo "  tests/integration/test_validation.py"
echo "  tests/integration/test_multi_agent.py" 
echo "Capability tests:"
echo "  tests/integration/capabilities/test_standalone_tools.py"
echo "  tests/integration/capabilities/test_class_method_tools.py"
echo "  tests/integration/capabilities/test_multi_step.py"
echo "---------------------------------"

# Ask for confirmation
read -p "Do you want to proceed with deletion? (y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo "Deletion cancelled."
    exit 0
fi

# Create backup directory
BACKUP_DIR="tests/integration/backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
echo "Creating backup in $BACKUP_DIR"

# Backup and remove files
backup_and_remove() {
    if [ -f "$1" ]; then
        echo "Backing up $1"
        cp "$1" "$BACKUP_DIR/"
        echo "Removing $1"
        rm "$1"
    else
        echo "File $1 not found, skipping"
    fi
}

# Handle duplicate observer
backup_and_remove "tests/integration/test_observer.py"

# Handle model-specific tests
backup_and_remove "tests/integration/test_anthropic_claude.py"
backup_and_remove "tests/integration/test_groq_llama.py"
backup_and_remove "tests/integration/test_ollama_phi.py"
backup_and_remove "tests/integration/test_gpt4o_mini.py"

# Handle other duplicated tests
backup_and_remove "tests/integration/test_validation.py"
backup_and_remove "tests/integration/test_multi_agent.py"

# Handle capability tests
backup_and_remove "tests/integration/capabilities/test_standalone_tools.py"
backup_and_remove "tests/integration/capabilities/test_class_method_tools.py"
backup_and_remove "tests/integration/capabilities/test_multi_step.py"

echo "Cleanup completed. Files have been backed up to $BACKUP_DIR"
echo "Run tests to verify everything still works: python -m pytest tests/integration/consolidated" 