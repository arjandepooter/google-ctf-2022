#include <stdint.h>
#include <stdbool.h>

__sfr __at(0xee) FLAGROM_ADDR;
__sfr __at(0xef) FLAGROM_DATA;

__sfr __at(0xf2) SERIAL_OUT_DATA;
__sfr __at(0xf3) SERIAL_OUT_READY;

void serial_print(const char *s)
{
    while (*s)
    {
        while (!SERIAL_OUT_READY)
        {
            // Busy wait...
        }

        SERIAL_OUT_DATA = *s++;
    }
}

int main(void)
{
    static __xdata char flag[64];

    for (int i = 0; i < 64; i++)
    {
        FLAGROM_ADDR = i;
        flag[i] = FLAGROM_DATA;
    }
    serial_print(flag);
}
