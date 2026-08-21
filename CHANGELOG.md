# Changelog

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## 1.2.0 - 2026-08-21
### Added
- Setup script for automated environment configuration
- Apache HTTP Server support (replacing Nginx)
- Portuguese translation of README
- Automatic migration check before server startup

### Changed
- Migrated to Ubuntu 26.04 LTS support
- Updated all dependencies to latest stable versions
- Replaced Nginx with Apache
- Enhanced documentation with detailed setup instructions
- Updated README with current technologies and build instructions

## 1.1.0 - 2024-03-19
### Added
- Docker support with docker-compose for easy deployment
- Load testing suite in performance_analysis directory
- Gunicorn as production WSGI server
- Nginx configuration for production deployment
- PostgreSQL/PostGIS as the main database system
- Comprehensive documentation with UML diagrams (class, user, sequence)

### Changed
- Updated Django to latest stable version
- Migrated from SQLite to PostgreSQL/PostGIS
- Improved project structure and organization
- Enhanced documentation with detailed setup instructions
- Updated README with current technologies and build instructions

### Removed
- SQLite database configuration
- Old installation scripts

## 1.0.2 - 2017-05-25
### Added
- This CHANGELOG file to begin the versioning and keep the changes easy to read.

### Created
- Documentation to keep serve as information about the development ([README](https://github.com/RadarLivre/RadarLivre/blob/master/README.md)).

### Changed
- README.md to give information about installation, development and tools that were used or can be used.

### Removed
- Unnecessary .pyc files.
- Old installation files.

## 1.0.1 - 2016-12-18
### Created
- .txt files to make it easier to setup(next version will take care of unnecessary files to clean the project).

### Changed
- Changed database to be sqlite, so it becomes easier to setup with no problems in other computers.

## 1.0.0 - 2016-10-17
	- Considered this version the 1.0.0, as there was no changelog prior to this point.
