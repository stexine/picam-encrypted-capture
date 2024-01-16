from picamera2 import Picamera2
from libcamera import controls
import time
import io
from Crypto.Cipher import AES

encrypt_key = b'\x8d5\x89\xbb\xe1\x1c\xed\x9f\x92HQ~kF \xd2\xea\x19\x9b\xaa\x03\x10\xbaM\xe0\x14R\xfb\x01\xc5\x9f\xc6'

picam2 = Picamera2()

# turn on HDR if needed
import os
os.system("v4l2-ctl --set-ctrl wide_dynamic_range=1 -d /dev/v4l-subdev0")
print("Setting HDR to ON")

#capture_config = picam2.create_still_configuration(main={"size": (4608,2592), "brightness": ("0","0"), "contrast": 1.0, "exposure": "normal", "framerate": 25, "gain": 0, "awb": "auto", "metering": "centre", "saturation": 1.0, "sharpness": 1.0, "denoise": "cdn_off", "quality": 95})
capture_config = picam2.create_still_configuration({"size": picam2.sensor_resolution})

picam2.start(show_preview=False)

picam2.controls.set_controls({"AfMode": 1,
                              "AfTrigger": 0,
                              "LensPosition": 2.5, 
                              "ExposureTime": 75000,
                              "AfSpeed": controls.AfSpeedEnum.Fast,
                              "AwbEnable": 0,
                              "AeEnable": 0,
                              "Saturation": 1.0,
                              "Sharpness": 1.0})


# print properties 
#print(picam2.camera_properties)

# print metadata
#metadata = picam2.capture_metadata()
#print(metadata)

# time to run
total_time = 7.5

# set time to wait before taking photo
time_used = 1

# pic number
pic_num = 0

start_time = time.time()
time.sleep(time_used)
output_dir = "./data"

while time_used <= total_time:

    start = time.time()
    pic_file = output_dir + "/id_img_" + str(pic_num) + ".jpg"

    data = io.BytesIO()

    print(picam2.capture_metadata())
    picam2.switch_mode_and_capture_file(capture_config, data, format='jpeg')
    
    cipher = AES.new(encrypt_key, AES.MODE_CFB)
    
    out_file = open(pic_file, "wb")
    out_file.write(cipher.iv)
    out_file.write(cipher.encrypt(data.getvalue()))

    # out_file.write(data.getbuffer())
    
    out_file.close()

    data.close()

    pic_num = pic_num + 1
    end = time.time()

    time_used = time_used + (end - start)

print("Total time used: " + str(time.time() - start_time))

#picam2.start_and_capture_files("py-photo-{:d}.jpg", num_files=17, delay=0)
#picam2.stop_preview()

'''
totalTime = 11.5
totalPic = 20
sleepTime = (totalTime / totalPic) * 0.8
print("Time sleep: " + str(sleepTime))
for i in range(totalPic):
    picam2.switch_mode_and_capture_file("still", "test_full-" + str(i) + ".jpg")
#    time.sleep(sleepTime)
'''

picam2.stop()

# ture off HDR if needed
print("Setting HDR to OFF")
os.system("v4l2-ctl --set-ctrl wide_dynamic_range=0 -d /dev/v4l-subdev0")

