obj-m := custom_driver.o

custom_driver-y += \
	src/custom_main.o \
	src/custom_main_ops.o

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules
clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean