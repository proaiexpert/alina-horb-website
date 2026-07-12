# Implementation Notes

## Baseline

The package is based on Homepage V2.1. The approved page design, section order, hero grid, arch geometry, crop positions, content, FAQ behavior, and responsive structure were not redesigned.

## Portrait replacement

The previous `576 × 1280` portrait files were removed. A new optimized production derivative was created from `alina-horb-portrait-master.jpg` and stored under stable production filenames. The source master is not present in the package.

The existing V2.1 crop system remains unchanged:

- desktop: `object-position: 50% 43%`;
- tablet: `object-position: 50% 42%`;
- mobile: `object-position: 50% 41%`;
- same tall, narrow arch and ivory bottom fade.

## Typography QA

Only targeted readability corrections were applied. Small body, FAQ, process, navigation-label, caption, and footer sizes were raised to production-readable values. Display typography, section geometry, colors, and visual hierarchy were retained.

## Architecture

The project remains dependency-free and can be served directly as static files.
