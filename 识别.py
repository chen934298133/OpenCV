
import sensor, time, image, sys, pyb, time

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


clock = time.clock()                    #TX RX 管脚控制
#from pyb import UART

#uart = UART(3, 115200, timeout_char=1000)                         # i使用给定波特率初始化
#uart.init(115200, bits=8, parity=None, stop=1, timeout_char=1000) # 使用给定参数初始化


n = 1
while (True):
    clock.tick()
    p = pyb.Pin("P0", pyb.Pin.OUT_PP)
    p.low()
    #p.LOW_POWER

    img = sensor.snapshot()

    objects = img.find_features(face_cascade, threshold=0.75, scale=1.25)

    ddd = clock.fps()
    fff = int(ddd)

    for r in objects:
        img.draw_rectangle(r)
        if fff != 0:
            #print(fff)
            n = n + 1
            #print(n)
            #SUB = "s1"
            NUM_SUBJECTS = 3            #图像库中不同人数，一共3 人
            NUM_SUBJECTS_IMGS = 20      #每人有20张样本图片

            img = sensor.snapshot()
            d0 = img.find_lbp((0, 0, img.width(), img.height()))
            img = None
            pmin = 999999
            num=0

            def min(pmin, a, s):
                global num
                if a<pmin:
                    pmin=a
                    num=s
                return pmin

            for s in range(1, NUM_SUBJECTS+1):
                dist = 0

                for i in range(2, NUM_SUBJECTS_IMGS+1):
                    img = image.Image("face/s%d/%d.pgm"%(s, i))
                    d1 = img.find_lbp((0, 0, img.width(), img.height()))             #d1为第s文件夹中的第i张图片的lbp特征
                    dist += image.match_descriptor(d0, d1)                           #计算d0 d1即样本图像与被检测人脸的特征差异度。
                print("Average dist for subject %d: %d"%(s, dist/NUM_SUBJECTS_IMGS))
                pmin = min(pmin, dist/NUM_SUBJECTS_IMGS, s)                          #特征差异度越小，被检测人脸与此样本更相似更匹配。
                print(pmin)
                i=0
            s=0
            if pmin > 100000:
                print(0)

            else:
                print(num)
                p.high()
                sensor.skip_frames(time = 3000)
                p.low()
                #uart.writechar(49)  #通过uart 引脚输出1

            if n == 2:
                n=5
        else:
            print("wrong")
    if n is 5:
        break




