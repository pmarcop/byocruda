# BYOCRUDA

Build Your Own CRUD Application - A highly customizable asset management system that enables teams to build custom solutions without coding.

## Overview

BYOCRUDA is a configuration-driven CRUD application framework that allows teams to create custom asset management systems through configuration files. It supports database schema customization, role-based access control, and automatic REST API generation.

## Features

- Configuration-driven design using TOML files
- Flexible database schema definition
- Role-based access control (RBAC)
- REST API generation
- Support for SQLite and PostgreSQL
- LDAP/SAML authentication
- Extensive logging capabilities
- Production-ready security features

## Requirements

- Python >= 3.12
- PDM (Python package manager)

## Installation

```bash
# Install the package and its dependencies
pdm install
```

## Development Setup

```bash
# Install development dependencies
pdm install -G dev
```

## Testing

```bash
# Install test dependencies
pdm install -G test

# Run tests
pdm run pytest
```

## License

This project is licensed under the GPL-3.0 License - see the LICENSE file for details.

## Author

- **pmarcop** - [GitHub](https://github.com/pmarcop)
