import sensor, time, image, sys, pyb

RED_LED_PIN = 1
BLUE_LED_PIN = 3


# Reset sensor
sensor.reset()
sensor.set_contrast(1)
sensor.set_gainceiling(16)
sensor.set_framesize(sensor.HQVGA)
sensor.set_pixformat(sensor.GRAYSCALE) 
sensor.set_framesize(sensor.B128X128) 
sensor.set_windowing((128,128))
face_cascade = image.HaarCascade("frontalface", stages=25)
print(face_cascade)

clock = time.clock()


num = 2     #设置被拍摄者序号，第一个人的图片保存到s1文件夹，第二个人的图片保存到s2文件夹，以此类推。每次更换拍摄者时，修改num值。

n = 20      #设置每个人拍摄图片数量。
m = 0
while (True):
    clock.tick()

    img = sensor.snapshot()

    objects = img.find_features(face_cascade, threshold=0.75, scale=1.25)

    ddd = clock.fps()
    fff = int(ddd)

    for r in objects:
        img.draw_rectangle(r)
        if fff != 0:
            print(fff)
            m = m + 1
            print(m)
            pyb.LED(BLUE_LED_PIN).on()
            sensor.snapshot().save("face/s%s/%s.pgm" % (num, m) )
            print("Done! Reset the camera to see the saved image.")
            pyb.LED(BLUE_LED_PIN).off()
            if m == 20:
                m = 20

        else:
            print("wrong")
    if m is 20:
        break