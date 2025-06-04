#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/fs.h>
#include <asm/uaccess.h>
#include <linux/slab.h>

#include "../inc/custom_main_ops.h"

u32 custom_driver_add(u32 a, u32 b)
{
    return a + b;
}

u32 custom_driver_mul(u32 a, u32 b)
{
    return a * b;
}

MODULE_LICENSE("GPL");