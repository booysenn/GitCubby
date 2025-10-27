#!/bin/bash
# scripts/install-hooks.sh

echo "Installing git hooks..."

# Copy pre-commit hook
cp scripts/hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

echo "Pre-commit hook installed"
echo ""
echo "To uninstall: rm .git/hooks/pre-commit"