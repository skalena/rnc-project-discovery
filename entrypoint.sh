#!/bin/bash

# ============================================================================
# entrypoint.sh - Entry point script for discover.py Docker container
# 
# This script provides a user-friendly interface for running discover.py
# inside a Docker container as a utility.
#
# Usage:
#   docker run discover [PROJECT_PATH] [OPTIONS]
#   docker run discover --help
# ============================================================================

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Display help message
show_help() {
    cat << EOF
${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}
${BLUE}║         RNC Discover - Static Java Project Analyzer            ║${NC}
${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}

${GREEN}USAGE:${NC}
  discover <PROJECT_PATH>
  discover --help
  discover --version

${GREEN}DESCRIPTION:${NC}
  Analyzes a Java project structure and generates a Markdown report with:
  - Entity classes (@Entity, @Table)
  - Business components (@Controller, @Service, @Named, etc.)
  - JSF pages (.xhtml, .jsf)
  - Database configuration references

${GREEN}ARGUMENTS:${NC}
  PROJECT_PATH    Absolute or relative path to the Java project directory

${GREEN}OPTIONS:${NC}
  --help          Display this help message
  --version       Display version information

${GREEN}EXAMPLES:${NC}
  # Analyze a project on your machine
  discover /path/to/my/java/project

  # Using Docker (relative path mapping)
  docker run -v /your/project:/data discover /data

  # Using Docker (interactive with current directory)
  docker run -v \$(pwd):/data discover /data

${GREEN}OUTPUT:${NC}
  A Markdown file (rcn-<project-name>.md) will be generated in the
  project root directory containing the analysis report.

${BLUE}════════════════════════════════════════════════════════════════${NC}
EOF
}

show_version() {
    cat << EOF
RNC Discover v1.0.0
Python Static Java Project Analyzer
Compatible with Java, JPA, Hibernate, JSF projects
EOF
}

# Handle command-line arguments
case "${1:-}" in
    --help|-h|help)
        show_help
        exit 0
        ;;
    --version|-v|version)
        show_version
        exit 0
        ;;
    "")
        # No argument provided
        echo -e "${RED}✗ Error: Project path is required${NC}"
        echo ""
        show_help
        exit 2
        ;;
    *)
        # Assume it's a project path
        PROJECT_PATH="${1}"
        
        # Validate that the path exists
        if [ ! -d "$PROJECT_PATH" ]; then
            echo -e "${RED}✗ Error: Directory does not exist: $PROJECT_PATH${NC}"
            exit 3
        fi
        
        echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${BLUE}║                  Starting Analysis...                          ║${NC}"
        echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
        echo -e "${YELLOW}Project Path:${NC} $PROJECT_PATH"
        echo -e "${YELLOW}Analysis started at:${NC} $(date '+%Y-%m-%d %H:%M:%S')"
        echo ""
        
        # Change to the project directory and run the Python script
        cd "$PROJECT_PATH" || exit 1
        python /app/discover.py "$PROJECT_PATH"
        
        exit $?
        ;;
esac
