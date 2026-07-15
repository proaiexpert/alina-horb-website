# Notes image hotfix v3.1

This hotfix makes the four Notes images part of the generated HTML instead of depending only on cached JavaScript DOM replacement.

It also:
- resolves asset paths from a versioned script URL;
- covers UA and RU homepages, Notes hubs, and all eight article pages;
- writes article social metadata statically;
- validates local paths and image presence before GitHub Pages deployment.
