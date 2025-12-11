# RNC Project Discovery

A Docker-based utility for analyzing Java and JavaServer Faces (JSF) projects to discover and document project architecture, entity classes, business components, and JSF pages.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Docker Usage](#docker-usage)
- [Examples](#examples)
- [Docker Hub](#docker-hub)
- [Output](#output)
- [Troubleshooting](#troubleshooting)

## Overview

RNC Project Discovery is an automated analysis tool that scans Java projects to identify:
- **Entity Classes** - Classes annotated with `@Entity` or `@Table`
- **Business Components** - Classes annotated with `@Service`, `@Controller`, `@RestController`, `@Named`, `@ManagedBean`, etc.
- **JSF Pages** - JavaServer Faces views (`.xhtml` and `.jsf` files)
- **Project Statistics** - Overall project metrics and composition

## Features

✨ **Automated Discovery**
- Scans entire Java projects recursively
- Identifies architectural patterns and components
- Generates comprehensive analysis reports

� **Business Rules Analysis (AST)**
- Detects methods with business logic using Abstract Syntax Tree (AST) parsing
- Identifies control flow, complex operations, and state mutations
- Calculates average business rule methods per Controller/Service
- Uses intelligent heuristics to identify complex methods (size-based detection)

�🐳 **Docker-Ready**
- Fully containerized application
- No local dependencies required
- Works on any platform with Docker

📊 **Detailed Reports**
- Entity and business component mapping
- JSF page discovery
- Business rules and logic complexity analysis
- Markdown format with tables and statistics
- Excel workbook with 6 detailed sheets
- Formatted console output
- Easy-to-parse analysis data

🏗️ **Multi-Platform Support**
- Built for multiple architectures
- Supports: Linux AMD64, ARM64, ARM/v7
- Works on Mac (both Apple Silicon and Intel)
- Works on Linux (x86_64, ARM servers)
- Works on Windows (via Docker Desktop)

## Prerequisites

- **Docker** (version 20.10 or later) OR **Python 3.11+** (for local usage)
- **A Java project** to analyze
- Approximately 500MB of disk space for the Docker image

### Python Dependencies

The project requires the following Python packages (included in Docker):
- **openpyxl** - For generating Excel (.xlsx) reports
- **javalang** - For Java AST (Abstract Syntax Tree) parsing and business rules analysis

**For local installation:**
```bash
pip install openpyxl javalang
```

### Install Docker

- **macOS/Windows**: [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux**: `sudo apt-get install docker.io` (Ubuntu/Debian)

## Quick Start

### Option A: Using Docker (Recommended)

#### 1. Build the Docker Image

```bash
docker build -t rnc-discover:latest .
```

**For Multi-Architecture Build** (AMD64, ARM64, ARM/v7):

```bash
# Create/use a builder instance
docker buildx create --name multiarch-builder
docker buildx use multiarch-builder

# Build for multiple architectures
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t rnc-discover:latest .

# Build and push to registry
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t skalena/rnc-discover:latest \
  --push .
```

#### 2. Run Analysis on Your Project

```bash
docker run --rm -v /path/to/your/project:/workspace rnc-discover:latest /workspace
```

### Option B: Using Python Locally

#### 1. Setup Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # On macOS/Linux
# or
.\.venv\Scripts\activate   # On Windows

# Install dependencies
pip install openpyxl javalang
```

#### 2. Run Analysis

```bash
python discover.py /path/to/your/java/project
```

The output folder will be created inside your project directory.

```bash
docker run --rm -v /path/to/your/project:/data rnc-discover:latest /data
```

Replace `/path/to/your/project` with the actual path to your Java project.

### 3. View Results

The analysis results will be displayed in your terminal, and output files will be created in `{project}/output/`.

## Docker Usage

### Platform Support

This Docker image is built to support multiple processor architectures:

| Platform | Status | Note |
|----------|--------|------|
| **linux/amd64** | ✅ Supported | Standard x86_64 Linux servers |
| **linux/arm64** | ✅ Supported | ARM64 servers, Apple Silicon Mac |
| **linux/arm/v7** | ✅ Supported | ARM32 v7 servers (Raspberry Pi, etc.) |

The `python:3.11-slim` base image automatically provides architecture-specific builds.

### Running with the Makefile (Recommended)

The project includes a `Makefile` for convenient Docker operations.

#### Build the Image

```bash
make build
```

#### Run Analysis

```bash
make run PROJECT=/path/to/your/project
```

Or use the current directory:

```bash
make run PROJECT=$(pwd)/my-project
```

#### Open Interactive Shell

```bash
make bash
```

#### Clean Up

```bash
make clean
```

#### View Help

```bash
make help
```

### Running with Docker Commands Directly

#### Build the Image

```bash
docker build -t rnc-discover:latest .
```

#### Run Analysis with Absolute Path

```bash
docker run --rm -v /absolute/path/to/project:/data rnc-discover:latest /data
```

#### Run Analysis with Relative Path

```bash
docker run --rm -v $(pwd)/my-project:/data rnc-discover:latest /data
```

#### Run Analysis with Current Directory

```bash
docker run --rm -v $(pwd):/data rnc-discover:latest /data
```

#### Run with Custom Options

```bash
docker run --rm -v /path/to/project:/data rnc-discover:latest /data --help
```

#### Interactive Shell Access

```bash
docker run --rm -it -v $(pwd):/data rnc-discover:latest /bin/bash
```

#### Keep Container Running for Inspection

```bash
docker run --rm -it -v $(pwd)/my-project:/data rnc-discover:latest
```

## Examples

### Example 1A: Analyze Using Docker (Recommended)

```bash
docker run --rm -v /Users/john/projects/my-java-app:/workspace rnc-discover:latest /workspace
```

Results in:
- `/Users/john/projects/my-java-app/output/rnc-my-java-app.md`
- `/Users/john/projects/my-java-app/output/rnc-my-java-app.xlsx`

### Example 1B: Analyze Using Python (Local)

```bash
# Setup (first time only)
python3 -m venv .venv
source .venv/bin/activate
pip install openpyxl javalang

# Run analysis
python discover.py /Users/john/projects/my-java-app
```

Results in:
- `/Users/john/projects/my-java-app/output/rnc-my-java-app.md`
- `/Users/john/projects/my-java-app/output/rnc-my-java-app.xlsx`

### Example 2: Analyze a Project in Current Directory

```bash
# Using Docker
docker run --rm -v $(pwd):/workspace rnc-discover:latest /workspace

# Using Python (with venv activated)
python discover.py $(pwd)
```

Results in:
- `./output/rnc-{project-name}.md`
- `./output/rnc-{project-name}.xlsx`

### Example 3: Business Rules Analysis Output

The reports include a new **"Análise de Regras de Negócio"** (Business Rules Analysis) section that shows:

```markdown
## 5. Análise de Regras de Negócio

**Total de Classes Analisadas:** 192
**Controllers Encontrados:** 0
**Services Encontrados:** 3
**Métodos com Regras de Negócio:** 224
**Número Médio de Métodos com Regras de Negócio por Controller:** 0.00
**Número Médio de Métodos com Regras de Negócio por Service:** 1.33

### Services com Regras de Negócio

- **DocumentService** (src/main/java/org/primefaces/ultima/service/DocumentService.java)
  - Métodos públicos: 2
  - Métodos com regras: 2
  - Métodos: createDocuments, createCheckboxDocuments
```

### Example 4: Copy Output Files to Local Machine

```bash
# Run analysis and extract output
docker run --rm -v $(pwd)/my-project:/data rnc-discover:latest /data

# Files are created in my-project/output/
ls my-project/output/
```

### Example 5: Run in Interactive Mode for Debugging

```bash
docker run --rm -it \
  -v $(pwd)/my-project:/data \
  rnc-discover:latest \
  /bin/bash
```

Then inside the container:

```bash
cd /data
python /app/discover.py /data
ls -la output/
```

## Docker Hub

### Push to Docker Hub (Multi-Platform)

The `push-to-docker-hub.sh` script automatically builds and pushes multi-platform images to Docker Hub:

```bash
# Push latest tag to Docker Hub (builds for amd64, arm64, arm/v7)
./push-to-docker-hub.sh

# Or with a specific version tag
./push-to-docker-hub.sh v1.0.0
```

**What it does:**
1. ✅ Checks Docker buildx availability (creates builder if needed)
2. ✅ Verifies Docker Hub login
3. ✅ Builds image for multiple platforms: `linux/amd64`, `linux/arm64`, `linux/arm/v7`
4. ✅ Pushes all platform images to Docker Hub
5. ✅ Provides verification commands

**Requirements:**
- Docker Desktop (Mac/Windows) or Docker with buildx installed
- Logged in to Docker Hub (`docker login`)
- Internet connection for pushing

**Example output:**
```
🐳 Multi-Platform Docker Hub Push Script
========================================

Configuration:
  Docker Hub User: skalena
  Image Name:     rnc-discover
  Tag:            latest
  Remote Image:   skalena/rnc-discover:latest
  Platforms:      linux/amd64,linux/arm64,linux/arm/v7

✅ Using existing builder: multiarch-builder
✅ Docker Hub login verified

🏗️  Building for platforms: linux/amd64,linux/arm64,linux/arm/v7
📤 Building and pushing to Docker Hub...

✅ Image built and pushed successfully!

🎉 Done! Your image is now available at:
   https://hub.docker.com/r/skalena/rnc-discover
```

### Advanced: Manual Multi-Architecture Build

For more control over the build process, use the `build-multiarch.sh` script:

```bash
# Build and push to Docker Hub
./build-multiarch.sh latest push

# Build and push with version tag
./build-multiarch.sh v1.0.0 push

# Build without pushing (default)
./build-multiarch.sh latest

# Build for current architecture and load locally
./build-multiarch.sh latest load
```

**Script Usage:**

```bash
./build-multiarch.sh [TAG] [ACTION]

Arguments:
  TAG     - Docker image tag (default: latest)
  ACTION  - build, push, or load (default: build)

Examples:
  ./build-multiarch.sh latest push         # Build and push latest
  ./build-multiarch.sh v1.0 push          # Build and push v1.0
  ./build-multiarch.sh latest load        # Build and load locally
```

### Verify Multi-Platform Image on Docker Hub

```bash
docker buildx imagetools inspect skalena/rnc-discover:latest
```

Expected output:
```
Name:      docker.io/skalena/rnc-discover:latest
MediaType: application/vnd.docker.distribution.manifest.list.v2+json
Digest:    sha256:abc123...

Manifests:
  Name:      docker.io/skalena/rnc-discover:latest@sha256:amd64_digest
  Platform:  linux/amd64

  Name:      docker.io/skalena/rnc-discover:latest@sha256:arm64_digest
  Platform:  linux/arm64

  Name:      docker.io/skalena/rnc-discover:latest@sha256:armv7_digest
  Platform:  linux/arm/v7
```

### Pull from Docker Hub

If the image is published on Docker Hub:

```bash
docker pull skalena/rnc-discover:latest
```

Run the pulled image (automatically uses correct platform):

```bash
docker run --rm -v $(pwd)/my-project:/data skalena/rnc-discover:latest /data
```

The correct image for your platform will be automatically selected.

## Output

The analysis generates comprehensive reports in multiple formats:

### Output Folder Structure

```
output/
├── rnc-{project-name}.md      # Markdown report
└── rnc-{project-name}.xlsx    # Excel workbook with multiple sheets
```

### Markdown Report (.md)

A detailed text report including:
- Project information and analysis timestamp
- Complete list of entity classes with patterns found
- Business components and controllers
- JSF pages discovered
- Database configuration files detected
- Full analysis execution log

**Location**: `output/rnc-{project-name}.md`

### Excel Report (.xlsx)

A comprehensive workbook with 5 sheets:

1. **Summary Sheet**
   - Project name and analysis date
   - Key metrics (counts of entities, components, JSF pages)
   - Quick overview of findings

2. **Entity Classes Sheet**
   - File paths (absolute and relative)
   - JPA/Hibernate patterns detected
   - Sortable and filterable data

3. **Business Components Sheet**
   - File paths (absolute and relative)
   - Component type annotations found
   - Sortable and filterable data

4. **JSF Pages Sheet**
   - File paths (absolute and relative)
   - View layer components

5. **Analysis Log Sheet**
   - Complete execution log with timestamps
   - Error messages and status information

**Location**: `output/rnc-{project-name}.xlsx`

### Console Output Example

```
📁 Pasta 'output' criada com sucesso.
✅ Relatório Markdown salvo em: output/rnc-APM.md
✅ Relatório Excel salvo em: output/rnc-APM.xlsx

==========================================================================
RESUMO DA ANÁLISE ESTATICA
==========================================================================
Projeto Analisado: APM
Total de Entidades: 8
Total de Componentes de Negócio/Controladoras: 138
Total de Páginas JSF: 41
Informações de DB Encontradas: Não
==========================================================================
📂 Arquivos de saída estão em: output/
==========================================================================
```

### Output Details

#### Markdown Report (`rnc-{project-name}.md`)

Contains 6 main sections:

1. **Classes de Entidades** - Java classes marked with JPA annotations (`@Entity`, `@Table`)
2. **Classes de Componentes de Negócio** - Service, controller, and managed bean classes (`@Service`, `@Controller`, `@Named`, etc.)
3. **Páginas JSF** - View layer files used in JSF applications (`.xhtml`, `.jsf`)
4. **Informações do Banco de Dados** - Configuration files that may contain database connection details
5. **Análise de Regras de Negócio** - AST-based business logic analysis:
   - Total classes analyzed
   - Controllers and Services found
   - Business logic method count
   - Average business methods per Controller/Service
   - Detailed method names for each component
6. **Log de Execução** - Execution log with analysis details

#### Excel Report (`rnc-{project-name}.xlsx`)

Contains 6 worksheets:

1. **Summary** - Project overview and metrics summary
2. **Entity Classes** - Detailed entity class information
3. **Business Components** - Business component listings with annotations found
4. **JSF Pages** - JSF view files
5. **Business Rules Analysis** - AST analysis with:
   - Class name and file path
   - Component type (Controller, Service, Repository, etc.)
   - Count of public methods
   - Count of business rule methods
   - Specific method names with business logic
   - Summary statistics with averages
6. **Analysis Log** - Detailed execution log

## Troubleshooting

### Issue: "Project path not found"

**Solution**: Ensure the path is correct and absolute:

```bash
# ✅ Correct
docker run --rm -v /Users/john/projects/app:/workspace rnc-discover:latest /workspace

# ❌ Wrong (relative paths may not work)
docker run --rm -v ./app:/workspace rnc-discover:latest /workspace
```

### Issue: "Permission denied"

**Solution**: Check file permissions in your project directory:

```bash
chmod -R 755 /path/to/your/project
```

### Issue: "javalang não está disponível" (Local Python)

**Solution**: Ensure dependencies are installed in the virtual environment:

```bash
source .venv/bin/activate  # Activate venv
pip install javalang openpyxl
python discover.py /path/to/project
```

### Issue: "No space left on device"

**Solution**: Clean up Docker images and containers:

```bash
docker system prune -a
```

### Issue: Container exits immediately

**Solution**: Ensure you're providing a valid project path:

```bash
docker run --rm -v $(pwd):/data rnc-discover:latest /data
```

### Issue: "Docker not found"

**Solution**: Install Docker or add it to your PATH:

```bash
which docker
# If empty, install Docker Desktop or Docker CLI
```

### Debugging: View Container Logs

```bash
# Run and keep terminal open
docker run --rm -it -v $(pwd)/my-project:/data rnc-discover:latest /data

# Or run bash to explore
docker run --rm -it -v $(pwd)/my-project:/data rnc-discover:latest /bin/bash
```

## Project Structure

```
rnc-project-discovery/
├── discover.py              # Main analysis script
├── entrypoint.sh           # Container entry point
├── Dockerfile              # Multi-platform Docker definition
├── .dockerignore           # Docker ignore patterns
├── Makefile                # Build and run commands
├── push-to-docker-hub.sh   # Multi-platform push script
├── build-multiarch.sh      # Advanced multi-platform build script
├── README.md               # This file
└── LICENSE                 # License information
```

## Environment Variables

The Docker image sets these environment variables:

- `PYTHONUNBUFFERED=1` - Python output is unbuffered
- `PYTHONDONTWRITEBYTECODE=1` - No .pyc files are created

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker
5. Submit a pull request

## License

See the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or suggestions, please open an issue on the project repository.

## Related Commands

### Common Docker Commands

```bash
# List all images
docker images

# List running containers
docker ps

# Remove an image
docker rmi rnc-discover:latest

# View image history
docker history rnc-discover:latest

# Tag an image for Docker Hub
docker tag rnc-discover:latest skalena/rnc-discover:latest

# Push to Docker Hub
docker push skalena/rnc-discover:latest
```

### Useful Aliases

Add these to your shell configuration (`.bashrc`, `.zshrc`, etc.):

```bash
# Quick run
alias rnc-discover='docker run --rm -v $(pwd):/data rnc-discover:latest /data'

# Build and run
alias rnc-build-run='make build && make run PROJECT=$(pwd)'
```

Then use:

```bash
rnc-discover /path/to/project
```

---

**Version**: 1.0.0  
**Last Updated**: December 2024  
**Maintained by**: skalena