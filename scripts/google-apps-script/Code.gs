function autoSortByMonth(e) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getActiveSheet();
  
  // Get the raw timestamp string from the first column
  const timestampStr = e.values[0]; 
  
  // Explicitly split the dd/MM/yyyy string to avoid confusion
  const parts = timestampStr.split(' ')[0].split('/');
  const day = parseInt(parts[0], 10);
  const month = parseInt(parts[1], 10) - 1; // JS months are 0-indexed
  const year = parseInt(parts[2], 10);
  
  const date = new Date(year, month, day);
  
  // Format the month (e.g., "February 2026")
  const monthName = Utilities.formatDate(date, Session.getScriptTimeZone(), "MMMM yyyy");
  
  let targetSheet = ss.getSheetByName(monthName);
  
  if (!targetSheet) {
    targetSheet = ss.insertSheet(monthName);
    const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues();
    targetSheet.getRange(1, 1, 1, headers[0].length).setValues(headers);
    targetSheet.setFrozenRows(1);
  }
  
  targetSheet.appendRow(e.values);
}