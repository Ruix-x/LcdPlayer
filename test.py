# import usb1
# with usb1.USBContext() as context:
#     handle = context.openByVendorIDAndProductID(
#         0x0403,
#         0xc630,
#         skip_on_error=True,
#     )
#     if handle is None:
#         print(None)
#         pass
#     with handle.claimInterface(0):
#         pass
#         # Device not present, or user is not allowed to access device.

from lcd2usb import LCD,SMILE_SYMBOL,LCD_CTRL_1,LCD_CTRL_0,LCD_DATA,LCD_BOTH
lcd = LCD()
lcd.clear()
SMILE_SYMBOL = bytearray([0x81, 0x41, 0x21, 0x11, 0x11, 0x11, 0x11, 0x11,0x81, 0x41, 0x21, 0x11, 0x11, 0x11, 0x11, 0x11])

lcd.define_char(0, SMILE_SYMBOL)
lcd.write(SMILE_SYMBOL, 0, 0)
lcd.write_char(0, 19, 0)
