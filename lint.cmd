:: Lint the whole App
@echo off
cls

pylint asset_allocation --output-format=colorized

pause