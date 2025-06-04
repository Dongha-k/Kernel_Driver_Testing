#include <kunit/test.h>

#include "custom_main_ops.h"

static void custom_driver_add_test_basic(struct kunit *test)
{
    KUNIT_EXPECT_EQ(test, 1, custom_driver_add(1, 0));
    KUNIT_EXPECT_EQ(test, 2, custom_driver_add(1, 1));
}

static void custom_driver_mul_test_basic(struct kunit *test)
{
    KUNIT_EXPECT_EQ(test, 12, custom_driver_mul(3, 4));
    KUNIT_EXPECT_EQ(test, 18, custom_driver_mul(9, 2));
}

static void custom_driver_test_failure(struct kunit *test)
{
//    KUNIT_FAIL(test, "This test never passes.");
}

static struct kunit_case custom_driver_test_cases[] = {
    KUNIT_CASE(custom_driver_add_test_basic),
    KUNIT_CASE(custom_driver_mul_test_basic),
    KUNIT_CASE(custom_driver_test_failure),
    {}};

static struct kunit_suite custom_driver_test_suite = {
    .name = "custom-driver-example",
    .test_cases = custom_driver_test_cases,
};
kunit_test_suite(custom_driver_test_suite);

MODULE_LICENSE("GPL");