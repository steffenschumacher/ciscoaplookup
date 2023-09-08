# Versions

## 0.13.2
Lax version of env modules
## 0.13.1
Update docs to reflect new API and restore beautifulsoup for juniper parsing

## 0.13.0
Major overhaul:
* ditch xlrd -> openpyxl
  * xlrd 2+ doesn't support needed xlsx format anymore - only xls
  * openpyxl is slow -> in memory lookups not sufficient
* cache parsed data into sqlite
  * Configurable update intervals in days
  * update checks parsed md5 hash with downloaded md5 if its needed
  * Store country as iso2 for better performance
  * sql for faster lookups
  
## 0.12.0
Updated tabs - 'Controller based' -> 'Indoor'