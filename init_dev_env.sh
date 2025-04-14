#!/bin/bash

# Fauxmots development environment setup script
echo "Setting up Fauxmots development environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Update pip
echo "Updating pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install development dependencies
echo "Installing development dependencies..."
pip install pytest pytest-cov flake8 black

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p emails
mkdir -p instance

# Set up pre-commit hook for code formatting
echo "Setting up pre-commit hook..."
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Run black on all Python files to be committed
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')
if [ -n "$FILES" ]; then
    echo "Running black on Python files..."
    venv/bin/black $FILES
    git add $FILES
fi
EOF
chmod +x .git/hooks/pre-commit

echo "Development environment setup complete."
echo "To activate the virtual environment, run: source venv/bin/activate"
