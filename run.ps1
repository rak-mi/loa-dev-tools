Get-ChildItem -Path 'C:\Users\diego\OneDrive\Documents\loa\loa-dev-tools\screenshots\market' *.png| foreach { Remove-Item -Path $_.FullName }

# Open market
py .\keyboard.py

py .\mouse.py 448 442

py .\mouse.py 440 483
py .\mouse.py 440 483

Start-Sleep -s 2

# Run script for screenshots
py .\screen.py market market_data enhancement_page_1

# Clicking next page
py .\mouse.py 1146 902
py .\mouse.py 1146 902

py .\screen.py market market_data enhancement_page_2

py .\app.py 
