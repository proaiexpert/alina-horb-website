# Implementation Notes

## Baseline

The package is based on Homepage V2.1. The approved page design, section order, hero grid, content, FAQ behavior, and responsive structure were retained.

## Portrait replacement

The previous `576 × 1280` portrait files were removed. A new optimized production derivative was created from `alina-horb-portrait-master.jpg` and stored under stable production filenames. The source master is not present in the package.

The V3 crop keeps more of the approved portrait visible:

- desktop: `aspect-ratio: .50`, `object-position: 50% 47%`;
- tablet: `aspect-ratio: .52`, `object-position: 50% 47%`;
- mobile: `aspect-ratio: .54`, `object-position: 50% 47%`;
- same tall, narrow arch and ivory bottom fade, with the head, neck, shoulders and upper torso visible.

## Contact layout

Laptop and desktop layouts use a compact two-column contact section with methods on the left and a form capped at 720 px on the right. Tablet and mobile layouts collapse to one column. The textarea is 130 px tall and the desktop submit button keeps its intrinsic width.

## Typography QA

Only targeted readability corrections were applied. Small body, FAQ, process, navigation-label, caption, and footer sizes were raised to production-readable values. Display typography, section geometry, colors, and visual hierarchy were retained.

## Architecture

The project remains dependency-free and can be served directly as static files.
