# PyCP2K with Python 3.11 Reference

## Compatibility Issues

Two breaking changes when using pycp2k with Python 3.11:

1. **collections.Mapping → collections.abc.Mapping** 
   - Python 3.9+ moved abstract base classes from `collections` to `collections.abc`
   - Direct imports from `collections.Mapping` are deprecated and removed in 3.11+

2. **Removal of distutils.version**
   - The `distutils` module was deprecated in Python 3.10 and removed in 3.12
   - Version comparison functionality needs to be replaced

## Solutions

Both issues can be fixed with:

### Option 1: Manual Patch (3-line fix)
Apply a simple patch to fix the import issues in the pycp2k codebase.

### Option 2: Community Compatibility Package
```bash
pip install pycp2k-compat
```
This community shim package provides the necessary compatibility fixes.

## Technical Details

The specific changes needed are:

1. Replace `from collections import Mapping` with `from collections.abc import Mapping`
2. Replace `distutils.version` usage with `packaging.version` or similar alternative

These are minimal changes that maintain full functionality while ensuring Python 3.11+ compatibility. 