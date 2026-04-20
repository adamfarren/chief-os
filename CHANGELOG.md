# Changelog

All notable changes to Chief OS are documented here.

This project uses [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) formatting. It does not ship versioned releases — `main` is the supported branch — but entries here track meaningful skill additions, breakages, and behavior changes so forks can see what's new.

## [Unreleased]

### Added
- `CONTRIBUTING.md`, `SECURITY.md`, `.github/` issue + PR templates, this changelog
- `chief-style` is now a fork-and-customize template with a neutral example palette and a config-driven Figma fileKey (read from `chief-context/company.yaml` under `style.figma_file_key`)
- `company-update` now reads workspace IDs (Notion database, parent page, Slack channel) from `chief-context/company.yaml` rather than hardcoding them

### Notes
- Company-specific skill variants (partnership PRDs tied to a particular SDK, customer-360 flows wired to a specific product) are intentionally out of scope for the public package — fork and add your own if needed

## [0.1.0] — Initial public release

First public release of Chief OS: a package of Claude Code skills that give you an AI Chief of Staff. Includes the `chief` router, shared company context layer, and 20+ interconnected skills spanning investor prep, board materials, pipeline updates, customer 360s, weekly company updates, and more.
