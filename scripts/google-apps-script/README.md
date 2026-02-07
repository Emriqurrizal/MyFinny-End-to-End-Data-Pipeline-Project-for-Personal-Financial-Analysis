# Google Apps Script - MyFinny Auto-Sort by Month

This folder contains Google Apps Script for automatically organizing MyFinny transaction data by month.

## Overview

The script automatically sorts incoming transaction data into monthly sheets based on the timestamp in the first column. Each time new data is added (e.g., via Google Form submission), it automatically creates or updates the corresponding monthly sheet.

## Files
- `Code.gs` - Main Apps Script code containing the `autoSortByMonth()` function

## Features

- **Automatic Monthly Sorting**: Sorts transactions into sheets named by month (e.g., "February 2026")
- **Auto-Sheet Creation**: Creates new monthly sheets automatically when needed
- **Header Preservation**: Copies headers from the main sheet to new monthly sheets
- **Date Format Support**: Handles dd/MM/yyyy timestamp format
- **Frozen Headers**: Automatically freezes the first row in new sheets

## Deployment

1. Open your Google Sheet (MyFinny data sheet)
2. Go to **Extensions > Apps Script**
3. Copy the code from `Code.gs`
4. Paste into the Apps Script editor
5. Save the project (give it a name like "MyFinny Auto-Sort")
6. Set up the trigger:
   - Click on the clock icon (Triggers) in the left sidebar
   - Click "+ Add Trigger"
   - Choose function: `autoSortByMonth`
   - Choose event source: "From spreadsheet"
   - Choose event type: "On form submit" (or "On change" if entering data manually)
   - Save
7. Authorize the script when prompted

## How It Works

1. **Trigger**: Activates when new data is added to the sheet
2. **Parse Date**: Extracts the timestamp from the first column (Column A)
3. **Date Format**: Parses the date expecting dd/MM/yyyy format
4. **Generate Sheet Name**: Creates month name in "MMMM yyyy" format (e.g., "February 2026")
5. **Find or Create Sheet**: Looks for existing monthly sheet or creates a new one
6. **Copy Headers**: If creating new sheet, copies headers from the main sheet
7. **Append Data**: Adds the new transaction row to the appropriate monthly sheet

## Requirements

- Google Sheet with transaction data
- First column (Column A) must contain timestamp in dd/MM/yyyy format
- First row must contain column headers

## Date Format

The script expects timestamps in the format: `dd/MM/yyyy HH:mm:ss`

Example: `07/02/2026 14:30:00`

## Troubleshooting

- **Script not running**: Check that the trigger is properly set up
- **Wrong month assignment**: Verify the timestamp format in Column A
- **Permission errors**: Re-authorize the script in Extensions > Apps Script

