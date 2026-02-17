# MindsDB BeautifulSoup4 Dependency Fix

## Issue Fixed

MindsDB HTTP API was failing to start with error:
```
ModuleNotFoundError: No module named 'bs4'
```

## Root Cause

The `beautifulsoup4` package (imported as `bs4`) is required by:
- `mindsdb.interfaces.knowledge_base.preprocessing.document_loader`
- `mindsdb.integrations.handlers.web_handler.urlcrawl_helpers`

But it was not listed in `requirements/requirements.txt`.

## Fix Applied

✅ **Added to requirements.txt:**
```txt
beautifulsoup4>=4.12.0  # required for knowledge base document loader and web handler
```

✅ **Installed package:**
- `beautifulsoup4-4.14.3` (latest version)
- `soupsieve-2.8.1` (dependency)

## Verification

The package is now installed and can be imported:
```python
from bs4 import BeautifulSoup  # ✅ Works
```

## Next Steps

1. **Restart MindsDB** to verify HTTP API starts successfully:
   ```bash
   make run_mindsdb_full_apis
   ```

2. **Expected Result:**
   ```
   mindsdb: http API: started on 47334
   ```
   (Instead of the `ModuleNotFoundError`)

## Additional Notes

- The LiteLLM server error about missing `--agent` parameter is a separate configuration issue
- The MySQL API is starting successfully on port 47335
- BeautifulSoup4 is used for HTML parsing in knowledge base document processing
