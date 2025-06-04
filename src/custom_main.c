#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/fs.h>
#include <asm/uaccess.h>
#include <linux/slab.h>

static int __init custom_driver_init(void)
{
    printk(KERN_ALERT "driver init successful\n");
    return 0;
}

static void __exit custom_driver_exit(void)
{
    printk(KERN_ALERT "driver cleanup successful\n");
}

module_init(custom_driver_init);
module_exit(custom_driver_exit);
MODULE_LICENSE("GPL");