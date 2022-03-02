from screen_scrape import scrape, screenshot


window = 'LOST ARK (64-bit, DX11) v.2.0.2.1'
screenshot_path = screenshot.take_screenshot_of_window(window)

descriptor = 'enhancement_page_4'
scrape.get_aution_house_prices(screenshot_path,descriptor)

