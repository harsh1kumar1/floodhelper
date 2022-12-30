function doGet(e)
{
    return HtmlService.createHtmlOutputFromFile('index');
}
function saveCoordinates(latitude,longitude,locationpin){
    var latlongcol,pinlocationcol;
    const sheet=SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Responses");
    var lastrow=sheet.getLastRow();
    var header=sheet.getRange(1,1,1,sheet.getLastColumn()).getValues();
    header=header.flat();
    for(var i=1;i<=header.length;i++){
        if(header[i]=="LatLong")
        {
            latlongcol=i+1;
        }
        if(header[i]=="GeoLocation"){
            pinlocationcol=i+1;
        }
    }
    if(sheet.getRange(lastrow,1).getValue()!="" && sheet.getRange(lastrow,latlongcol).getValue()=="" && sheet.getRange(lastrow,pinlocationcol).getValue==""){
        sheet.getRange(lastrow,latlongcol).setValue(latitude+","+longitude);
        sheet.getRange(lastrow,pinlocationcol).setValue(locationpin);
    }
}