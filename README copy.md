# RNC Discover - Docker Build & Run Guide

## Overview

This Docker configuration packages the `discover.py` script as a containerized utility for analyzing Java projects. The script identifies entity classes, business components, JSF pages, and database configurations in a Java project and generates a Markdown report.

## Files Included

- **Dockerfile** - Builds the Docker image with Python 3.11
- **entrypoint.sh** - Entry point script with help, version, and usage handling
- **Makefile** - Convenience commands for building and running
- **discover.py** - The main analysis script
- **README.md** - This file

## Quick Start

### Option 1: Using Makefile (Recommended)

```bash
# Build the image
make build

# Run analysis on a project
make run PROJECT=/path/to/your/java/project

# Get help
make help
```

### Option 2: Using Docker Directly

```bash
# Build the image
docker build -t rnc-discover:latest .

# Show help
docker run rnc-discover:latest --help

# Run analysis
docker run --rm -v /path/to/project:/data rnc-discover:latest /data

# Show version
docker run rnc-discover:latest --version
```

## Usage Examples

### Analyze a local project

```bash
make build
make run PROJECT=/Users/edgar/my-java-project
```

### Using the current working directory

```bash
docker run --rm -v $(pwd):/data rnc-discover:latest /data
```

### Open interactive bash shell

```bash
make bash
```

### Get help inside container

```bash
docker run rnc-discover:latest --help
```

## How It Works

1. **Build**: Creates a Docker image with Python 3.11 and copies the scripts
2. **Mount**: Your project directory is mounted as `/data` inside the container
3. **Execute**: The entrypoint script validates paths and runs the analysis
4. **Output**: Generates a `rcn-<project-name>.md` file in your project directory

## Output

The script generates a Markdown report containing:

- **Entity Classes** - Detected using `@Entity`, `@Table` annotations
- **Business Components** - Detected using `@Controller`, `@Service`, `@Named`, `@RestController` annotations
- **JSF Pages** - All `.xhtml` and `.jsf` files found
- **Database Configuration** - References to DB config in `.properties`, `.xml`, `.yml`, `.yaml` files
- **Execution Log** - Details about the analysis process

## Docker Tags

Build with different tags:

```bash
docker build -t rnc-discover:1.0 .
docker build -t rnc-discover:latest .
docker build -t myregistry/rnc-discover:latest .
```

## Troubleshooting

### "Directory does not exist" error
- Ensure the project path exists and is absolute or relative to current directory
- For Docker: Use absolute paths or mount correctly with `-v`

### Report not generated
- Check that the project directory has `.java` files or JSF pages
- Verify read permissions on the mounted volume
- Check the output for any errors in the analysis log

### Permission issues
- Ensure the Docker volume mount has proper permissions
- On macOS/Linux, you may need to adjust file ownership

## Advanced Usage

### Custom entry point
```bash
docker run -it --rm -v /project:/data rnc-discover:latest /bin/bash
# Inside container:
python /app/discover.py /data
```

### Save report to specific location
```bash
docker run --rm -v /project:/data -v /output:/output rnc-discover:latest /data
# Then move/copy the generated .md file to /output
```

## Version Information

- **Base Image**: Python 3.11-slim
- **Script Version**: 1.0.0
- **Supported Java Frameworks**: JPA, Hibernate, JSF, Spring

## License

Same as the original discover.py script.

---

**Created**: December 2025
**Maintained by**: RNC Team
