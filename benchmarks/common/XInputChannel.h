#pragma once
#include "Common.h"
struct XInputChannel {
 volatile LONG ready=0,expected=0,ack=0,stop=0;
 int64_t sent=0;
};
